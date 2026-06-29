import json
import os
import random
import math
from collections import Counter, defaultdict
from uuid import uuid4
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
QUESTION_BANKS_DIR = BASE_DIR.parent / "data" / "exams"
EXAM_STATE_DIR = BASE_DIR / "data" / "exams"
DEFAULT_EXAM_ID = "snowpro-core"

# Legacy single-exam files kept for backward compatibility.
LEGACY_QUESTION_BANK_FILE = BASE_DIR.parent / "data" / "snowpro_core_questions.json"
LEGACY_RESULTS_FILE = BASE_DIR / "data" / "exam_results.json"
LEGACY_DRAFT_FILE = BASE_DIR / "data" / "exam_draft.json"
LEGACY_INCORRECT_FILE = BASE_DIR / "data" / "incorrect_questions.json"
LEGACY_POTS_FILE = BASE_DIR / "data" / "question_pots.json"

RESULTS_FILENAME = "exam_results.json"
DRAFT_FILENAME = "exam_draft.json"
INCORRECT_FILENAME = "incorrect_questions.json"
POTS_FILENAME = "question_pots.json"
EXAM_SIZE = 100
PASSING_PERCENT = 75.0
MAX_RECENT_RESULTS = 5
DIFFICULTY_WEIGHTS = {
    "basic": 0.4,
    "intermediate": 0.4,
    "advanced": 0.2,
}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "snowpro-core-dev-secret")


def discover_exams() -> dict[str, dict]:
    exams: dict[str, dict] = {}

    if QUESTION_BANKS_DIR.exists():
        for exam_dir in sorted(QUESTION_BANKS_DIR.iterdir()):
            if not exam_dir.is_dir():
                continue
            question_file = exam_dir / "questions.json"
            if not question_file.exists():
                continue
            with question_file.open("r", encoding="utf-8") as file:
                payload = json.load(file)
            exams[exam_dir.name] = {
                "id": exam_dir.name,
                "exam_name": payload.get("examName", exam_dir.name),
                "question_file": question_file,
                "question_count": len(payload.get("questions", [])),
            }

    if not exams and LEGACY_QUESTION_BANK_FILE.exists():
        with LEGACY_QUESTION_BANK_FILE.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        exams[DEFAULT_EXAM_ID] = {
            "id": DEFAULT_EXAM_ID,
            "exam_name": payload.get("examName", "SnowPro Core"),
            "question_file": LEGACY_QUESTION_BANK_FILE,
            "question_count": len(payload.get("questions", [])),
        }

    return exams


def resolve_exam_id(exams: dict[str, dict]) -> str:
    requested_exam_id = (
        request.values.get("exam_id")
        or request.args.get("exam")
        or session.get("selected_exam_id")
    )

    if requested_exam_id in exams:
        session["selected_exam_id"] = requested_exam_id
        return requested_exam_id

    if DEFAULT_EXAM_ID in exams:
        session["selected_exam_id"] = DEFAULT_EXAM_ID
        return DEFAULT_EXAM_ID

    first_exam_id = next(iter(exams.keys()), "")
    if first_exam_id:
        session["selected_exam_id"] = first_exam_id
    return first_exam_id


def resolve_state_file(exam_id: str, filename: str) -> Path:
    modern_path = EXAM_STATE_DIR / exam_id / filename

    if filename == RESULTS_FILENAME and exam_id == DEFAULT_EXAM_ID and not modern_path.exists() and LEGACY_RESULTS_FILE.exists():
        return LEGACY_RESULTS_FILE
    if filename == DRAFT_FILENAME and exam_id == DEFAULT_EXAM_ID and not modern_path.exists() and LEGACY_DRAFT_FILE.exists():
        return LEGACY_DRAFT_FILE
    if filename == INCORRECT_FILENAME and exam_id == DEFAULT_EXAM_ID and not modern_path.exists() and LEGACY_INCORRECT_FILE.exists():
        return LEGACY_INCORRECT_FILE
    if filename == POTS_FILENAME and exam_id == DEFAULT_EXAM_ID and not modern_path.exists() and LEGACY_POTS_FILE.exists():
        return LEGACY_POTS_FILE

    return modern_path


def load_question_bank(exam_id: str, exams: dict[str, dict]) -> dict:
    exam = exams.get(exam_id)
    if not exam:
        raise FileNotFoundError("No exam definitions found in /data/exams.")

    question_file = exam["question_file"]
    with question_file.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    normalized_questions = []
    for item in raw.get("questions", []):
        choices = item.get("choices", {})
        choice_keys = sorted(choices.keys())
        options = [{"key": key, "text": choices[key]} for key in choice_keys]
        correct_key = item.get("correctAnswer")

        normalized_questions.append(
            {
                "id": item.get("id"),
                "domain": item.get("domain", "Unknown"),
                "difficulty": str(item.get("difficulty", "basic")).lower(),
                "origin": item.get("origin", "AI generated"),
                "question": item.get("question", ""),
                "options": options,
                "correct_answer_key": correct_key,
                "correct_answer_text": choices.get(correct_key, ""),
                "explanation": item.get("explanation", ""),
            }
        )

    return {
        "exam_id": exam_id,
        "exam_name": raw.get("examName", "SnowPro Core"),
        "question_count": len(normalized_questions),
        "questions": normalized_questions,
    }


def load_results(exam_id: str) -> list[dict]:
    results_file = resolve_state_file(exam_id, RESULTS_FILENAME)
    if not results_file.exists():
        return []
    with results_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_results(exam_id: str, results: list[dict]) -> None:
    results_file = resolve_state_file(exam_id, RESULTS_FILENAME)
    results_file.parent.mkdir(parents=True, exist_ok=True)
    with results_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)


def load_draft(exam_id: str) -> dict | None:
    draft_file = resolve_state_file(exam_id, DRAFT_FILENAME)
    if not draft_file.exists():
        return None
    with draft_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_draft(exam_id: str, state: dict) -> None:
    draft_file = resolve_state_file(exam_id, DRAFT_FILENAME)
    draft_file.parent.mkdir(parents=True, exist_ok=True)
    with draft_file.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)


def clear_draft(exam_id: str) -> None:
    draft_file = resolve_state_file(exam_id, DRAFT_FILENAME)
    if draft_file.exists():
        draft_file.unlink()


def load_question_pots(exam_id: str, all_question_ids: set[int]) -> dict[str, set[int]]:
    correct_ids: set[int] = set()
    incorrect_ids: set[int] = set()

    pots_file = resolve_state_file(exam_id, POTS_FILENAME)
    incorrect_file = resolve_state_file(exam_id, INCORRECT_FILENAME)

    if pots_file.exists():
        with pots_file.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        correct_ids = {int(qid) for qid in payload.get("correct_ids", [])}
        incorrect_ids = {int(qid) for qid in payload.get("incorrect_ids", [])}
    elif incorrect_file.exists():
        # Backward compatibility: bootstrap pots from legacy incorrect bank.
        with incorrect_file.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        incorrect_ids = {int(qid) for qid in payload.get("question_ids", [])}

    # Keep only valid IDs and ensure a question cannot exist in both pots.
    correct_ids = {qid for qid in correct_ids if qid in all_question_ids}
    incorrect_ids = {qid for qid in incorrect_ids if qid in all_question_ids}
    overlap = correct_ids.intersection(incorrect_ids)
    if overlap:
        incorrect_ids -= overlap

    return {
        "correct": correct_ids,
        "incorrect": incorrect_ids,
    }


def save_question_pots(exam_id: str, pots: dict[str, set[int]]) -> None:
    pots_file = resolve_state_file(exam_id, POTS_FILENAME)
    pots_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "correct_ids": sorted(pots.get("correct", set())),
        "incorrect_ids": sorted(pots.get("incorrect", set())),
        "correct_count": len(pots.get("correct", set())),
        "incorrect_count": len(pots.get("incorrect", set())),
    }
    with pots_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def get_pot_membership(all_question_ids: set[int], pots: dict[str, set[int]]) -> dict[str, set[int]]:
    correct = set(pots.get("correct", set()))
    incorrect = set(pots.get("incorrect", set()))
    unseen = set(all_question_ids) - correct - incorrect
    return {
        "unseen": unseen,
        "correct": correct,
        "incorrect": incorrect,
    }


def build_question_lookup(questions: list[dict]) -> dict[int, dict]:
    return {q["id"]: q for q in questions}


DISPLAY_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]


def shuffle_option_order(question: dict) -> list[str]:
    keys = [opt["key"] for opt in question["options"]]
    random.shuffle(keys)
    return keys


def build_display_options(question: dict, order: list[str]) -> tuple[list[dict], str | None]:
    by_key = {opt["key"]: opt for opt in question["options"]}
    if not order or sorted(order) != sorted(by_key.keys()):
        order = [opt["key"] for opt in question["options"]]

    display_options = []
    correct_display_key = None
    for i, key in enumerate(order):
        opt = by_key.get(key)
        if opt is None:
            continue
        display_key = DISPLAY_LETTERS[i] if i < len(DISPLAY_LETTERS) else str(i + 1)
        is_correct = key == question["correct_answer_key"]
        if is_correct:
            correct_display_key = display_key
        display_options.append(
            {
                "display_key": display_key,
                "key": key,
                "text": opt["text"],
                "is_correct": is_correct,
            }
        )
    return display_options, correct_display_key


def get_option_order(exam_state: dict, question: dict) -> list[str]:
    orders = exam_state.setdefault("option_orders", {})
    key = str(question["id"])
    order = orders.get(key)
    if not order:
        order = shuffle_option_order(question)
        orders[key] = order
    return order


def get_exam_state() -> dict:
    return session.get("active_exam", {})


def set_exam_state(state: dict) -> None:
    session["active_exam"] = state
    session.modified = True


def compute_resume_index(question_ids: list[int], answers: dict[str, str]) -> int:
    for i, qid in enumerate(question_ids, start=1):
        if not answers.get(str(qid)):
            return i
    return len(question_ids)


def compute_practice_progress(exam_state: dict, lookup: dict[int, dict]) -> dict:
    question_ids = exam_state.get("question_ids", [])
    answers = exam_state.get("answers", {})
    revealed = exam_state.get("revealed", {})

    overall = {"correct": 0, "wrong": 0, "skipped": 0, "total": len(question_ids)}
    breakdowns: dict[str, dict[str, dict]] = {"domain": {}, "difficulty": {}, "origin": {}}

    for qid in question_ids:
        question = lookup.get(qid)
        if not question:
            continue

        is_revealed = bool(revealed.get(str(qid)))
        answer = answers.get(str(qid))
        if is_revealed and answer:
            status = "correct" if answer == question["correct_answer_key"] else "wrong"
        else:
            status = "skipped"

        overall[status] += 1

        dimensions = (
            ("domain", question["domain"]),
            ("difficulty", question["difficulty"]),
            ("origin", question["origin"]),
        )
        for dimension, key in dimensions:
            bucket = breakdowns[dimension].setdefault(
                key, {"label": key, "correct": 0, "wrong": 0, "skipped": 0, "total": 0}
            )
            bucket[status] += 1
            bucket["total"] += 1

    def summarize(node: dict) -> dict:
        answered = node["correct"] + node["wrong"]
        accuracy = round(node["correct"] / answered * 100, 1) if answered else 0.0
        total = node["total"] or 1
        node["answered"] = answered
        node["accuracy"] = accuracy
        node["correct_pct"] = round(node["correct"] / total * 100, 1)
        node["wrong_pct"] = round(node["wrong"] / total * 100, 1)
        node["skipped_pct"] = round(node["skipped"] / total * 100, 1)
        return node

    summarize(overall)
    predicted_percent = overall["accuracy"]
    overall["predicted_percent"] = predicted_percent
    overall["predicted_pass"] = predicted_percent >= PASSING_PERCENT
    overall["passing_percent"] = PASSING_PERCENT

    grouped = {}
    for dimension, buckets in breakdowns.items():
        grouped[dimension] = [
            summarize(bucket) for _, bucket in sorted(buckets.items(), key=lambda kv: kv[0])
        ]

    return {"overall": overall, "breakdowns": grouped}


def allocate_by_capacity(total: int, capacities: dict[str, int], min_each: int = 0) -> dict[str, int]:
    keys = [key for key, cap in capacities.items() if cap > 0]
    allocation = {key: 0 for key in capacities}

    if total <= 0 or not keys:
        return allocation

    if min_each > 0:
        guaranteed = min_each * len(keys)
        if guaranteed <= total:
            for key in keys:
                allocation[key] = min(min_each, capacities[key])

    assigned = sum(allocation.values())
    remaining = max(0, total - assigned)
    if remaining == 0:
        return allocation

    residual_caps = {key: capacities[key] - allocation[key] for key in keys}
    total_residual = sum(residual_caps.values())
    if total_residual == 0:
        return allocation

    fractional = []
    for key in keys:
        share = remaining * (residual_caps[key] / total_residual)
        whole = int(share)
        allocation[key] += min(whole, residual_caps[key])
        fractional.append((share - whole, key))

    assigned = sum(allocation.values())
    left = total - assigned
    if left > 0:
        fractional.sort(reverse=True)
        for _, key in fractional:
            room = capacities[key] - allocation[key]
            if room <= 0:
                continue
            add = min(room, left)
            allocation[key] += add
            left -= add
            if left == 0:
                break

    return allocation


def allocate_difficulty(total: int, capacities: dict[str, int]) -> dict[str, int]:
    keys = [key for key, cap in capacities.items() if cap > 0]
    allocation = {key: 0 for key in capacities}
    if total <= 0 or not keys:
        return allocation

    weighted = []
    for key in keys:
        weight = DIFFICULTY_WEIGHTS.get(key, 0.0)
        weighted.append((key, weight))

    weight_sum = sum(weight for _, weight in weighted)
    if weight_sum <= 0:
        return allocate_by_capacity(total, capacities)

    fractional = []
    for key, weight in weighted:
        share = total * (weight / weight_sum)
        whole = int(share)
        allocation[key] = min(whole, capacities[key])
        fractional.append((share - whole, key))

    assigned = sum(allocation.values())
    left = total - assigned
    if left > 0:
        fractional.sort(reverse=True)
        for _, key in fractional:
            room = capacities[key] - allocation[key]
            if room <= 0:
                continue
            add = min(room, left)
            allocation[key] += add
            left -= add
            if left == 0:
                break

    if left > 0:
        for key in keys:
            room = capacities[key] - allocation[key]
            if room <= 0:
                continue
            add = min(room, left)
            allocation[key] += add
            left -= add
            if left == 0:
                break

    return allocation


def build_balanced_exam_questions(questions: list[dict], exam_size: int) -> list[dict]:
    if len(questions) < exam_size:
        raise ValueError("Not enough questions to build exam.")

    by_domain = defaultdict(list)
    for q in questions:
        by_domain[q["domain"]].append(q)

    domain_caps = {domain: len(items) for domain, items in by_domain.items()}
    domain_targets = allocate_by_capacity(exam_size, domain_caps, min_each=1)

    selected_ids = set()
    selected = []

    for domain, target_count in domain_targets.items():
        if target_count <= 0:
            continue

        domain_questions = by_domain[domain]
        by_diff = defaultdict(list)
        for q in domain_questions:
            by_diff[q["difficulty"]].append(q)

        diff_caps = {diff: len(items) for diff, items in by_diff.items()}
        diff_targets = allocate_difficulty(target_count, diff_caps)

        domain_selected = []
        for diff, diff_target in diff_targets.items():
            if diff_target <= 0:
                continue
            picks = random.sample(by_diff[diff], min(diff_target, len(by_diff[diff])))
            domain_selected.extend(picks)

        if len(domain_selected) < target_count:
            remaining_pool = [q for q in domain_questions if q["id"] not in {x["id"] for x in domain_selected}]
            needed = target_count - len(domain_selected)
            if remaining_pool and needed > 0:
                domain_selected.extend(random.sample(remaining_pool, min(needed, len(remaining_pool))))

        for q in domain_selected:
            if q["id"] in selected_ids:
                continue
            selected.append(q)
            selected_ids.add(q["id"])

    if len(selected) < exam_size:
        pool = [q for q in questions if q["id"] not in selected_ids]
        needed = exam_size - len(selected)
        selected.extend(random.sample(pool, needed))

    random.shuffle(selected)
    return selected[:exam_size]


@app.route("/")
def index():
    exams = discover_exams()
    if not exams:
        raise FileNotFoundError("No exam definitions found. Add data/exams/<exam-id>/questions.json.")

    exam_id = resolve_exam_id(exams)
    question_bank = load_question_bank(exam_id, exams)
    questions = question_bank["questions"]
    all_ids = {q["id"] for q in questions}
    pots = load_question_pots(exam_id, all_ids)
    pot_membership = get_pot_membership(all_ids, pots)
    all_results = load_results(exam_id)
    recent_results = list(reversed(all_results[-MAX_RECENT_RESULTS:]))
    available_domains = sorted({q["domain"] for q in questions})
    available_difficulties = sorted({q["difficulty"] for q in questions})
    origin_counts = Counter(q["origin"] for q in questions)
    origin_priority = {
        "AI generated": 0,
        "From Aditya": 1,
        "From Github": 2,
    }
    available_origins = sorted(
        origin_counts.keys(),
        key=lambda origin: (origin_priority.get(origin, 99), origin),
    )
    error_message = request.args.get("error")
    draft = load_draft(exam_id)

    exam_options = [
        {
            "id": item["id"],
            "title": item["exam_name"],
            "question_count": item["question_count"],
        }
        for item in exams.values()
    ]

    draft_summary = None
    if draft and draft.get("question_ids"):
        draft_total = len(draft.get("question_ids", []))
        draft_answers = draft.get("answers", {})
        draft_summary = {
            "mode": draft.get("mode", "exam"),
            "pots": draft.get("pots", ["unseen", "correct", "incorrect"]),
            "answered": sum(1 for answer in draft_answers.values() if answer),
            "total": draft_total,
            "started_at": draft.get("started_at"),
            "settings": draft.get("settings", {}),
        }

    stats = {
        "total_questions": question_bank.get("question_count", 0),
        "attempts": len(all_results),
        "best_score": max((r["score"] for r in all_results), default=0),
        "pass_rate": round(
            (sum(1 for r in all_results if r.get("passed")) / len(all_results) * 100),
            1,
        )
        if all_results
        else 0.0,
        "unseen_count": len(pot_membership["unseen"]),
        "correct_pot_count": len(pot_membership["correct"]),
        "incorrect_pot_count": len(pot_membership["incorrect"]),
    }

    return render_template(
        "index.html",
        page_title=f"{question_bank['exam_name']} Mock Exam",
        selected_exam_id=exam_id,
        selected_exam_name=question_bank["exam_name"],
        exam_options=exam_options,
        stats=stats,
        recent_results=recent_results,
        passing_percent=PASSING_PERCENT,
        exam_size=EXAM_SIZE,
        available_domains=available_domains,
        available_difficulties=available_difficulties,
        available_origins=available_origins,
        origin_counts=origin_counts,
        error_message=error_message,
        draft_summary=draft_summary,
    )


@app.post("/exam/start")
def start_exam():
    exams = discover_exams()
    if not exams:
        return redirect(url_for("index", error="No exams configured."))

    exam_id = resolve_exam_id(exams)
    question_bank = load_question_bank(exam_id, exams)
    questions = question_bank["questions"]
    question_lookup = {q["id"]: q for q in questions}
    all_ids = {q["id"] for q in questions}
    pots = load_question_pots(exam_id, all_ids)
    pot_membership = get_pot_membership(all_ids, pots)
    selected_pots = {p.lower() for p in request.form.getlist("pots")}
    allowed_pots = {"unseen", "correct", "incorrect"}
    selected_pots = selected_pots.intersection(allowed_pots)
    if not selected_pots:
        selected_pots = set(allowed_pots)

    selected_ids: set[int] = set()
    for pot_name in selected_pots:
        selected_ids |= pot_membership[pot_name]

    selected_domains = set(request.form.getlist("domains"))
    selected_difficulties = {d.lower() for d in request.form.getlist("difficulties")}
    selected_origins = set(request.form.getlist("origins"))
    mode = request.form.get("mode", "exam").strip().lower()
    if mode not in {"exam", "practice"}:
        mode = "exam"

    base_questions = [question_lookup[qid] for qid in sorted(selected_ids) if qid in question_lookup]

    filtered_questions = [
        q
        for q in base_questions
        if (not selected_domains or q["domain"] in selected_domains)
        and (not selected_difficulties or q["difficulty"] in selected_difficulties)
        and (not selected_origins or q["origin"] in selected_origins)
    ]

    if len(filtered_questions) == 0:
        if selected_pots == {"incorrect"} and len(pot_membership["incorrect"]) == 0:
            message = "All questions are learned. There are no incorrectly answered questions to review right now."
        else:
            message = (
                "No questions found for the selected filters. "
                "Please broaden your domain/difficulty/origin/pot selection."
            )
        return redirect(
            url_for(
                "index",
                error=message,
                exam=exam_id,
            )
        )

    selected_count = min(EXAM_SIZE, len(filtered_questions))
    selected = build_balanced_exam_questions(filtered_questions, selected_count)
    question_ids = [q["id"] for q in selected]

    exam_state = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "question_ids": question_ids,
        "answers": {},
        "revealed": {},
        "option_orders": {str(q["id"]): shuffle_option_order(q) for q in selected},
        "finished": False,
        "mode": mode,
        "pots": sorted(selected_pots),
        "current_index": 1,
        "settings": {
            "domains": sorted(selected_domains),
            "difficulties": sorted(selected_difficulties),
            "origins": sorted(selected_origins),
        },
        "exam_id": exam_id,
        "exam_name": question_bank["exam_name"],
    }
    set_exam_state(exam_state)
    save_draft(exam_id, exam_state)

    return redirect(url_for("exam_question", index=1))


@app.get("/exam/resume")
def resume_exam():
    exams = discover_exams()
    if not exams:
        return redirect(url_for("index", error="No exams configured."))

    exam_id = resolve_exam_id(exams)
    draft = load_draft(exam_id)
    if not draft or not draft.get("question_ids"):
        return redirect(url_for("index", error="No saved draft exam found.", exam=exam_id))

    set_exam_state(draft)
    resume_index = int(draft.get("current_index") or compute_resume_index(draft["question_ids"], draft.get("answers", {})))
    resume_index = max(1, min(len(draft["question_ids"]), resume_index))
    return redirect(url_for("exam_question", index=resume_index))


@app.post("/exam/discard")
def discard_exam():
    exams = discover_exams()
    exam_id = resolve_exam_id(exams) if exams else DEFAULT_EXAM_ID
    clear_draft(exam_id)
    session.pop("active_exam", None)
    return redirect(url_for("index", exam=exam_id))


@app.route("/exam/<int:index>", methods=["GET", "POST"])
def exam_question(index: int):
    exam_state = get_exam_state()
    exam_id = exam_state.get("exam_id", session.get("selected_exam_id", DEFAULT_EXAM_ID))
    question_ids = exam_state.get("question_ids", [])

    if not question_ids:
        return redirect(url_for("index", exam=exam_id))

    if exam_state.get("finished"):
        return redirect(url_for("exam_result"))

    if index < 1 or index > len(question_ids):
        return redirect(url_for("exam_question", index=1))

    exams = discover_exams()
    if exam_id not in exams:
        return redirect(url_for("index", error="Selected exam no longer exists."))

    question_bank = load_question_bank(exam_id, exams)
    lookup = build_question_lookup(question_bank["questions"])

    current_qid = question_ids[index - 1]
    current_question = lookup[current_qid]
    mode = exam_state.get("mode", "exam")
    selected_pots = exam_state.get("pots", ["unseen", "correct", "incorrect"])

    if request.method == "POST":
        selected_option = request.form.get("selected_option")
        if selected_option:
            exam_state["answers"][str(current_qid)] = selected_option

        action = request.form.get("action", "next")
        is_revealed = bool(exam_state.get("revealed", {}).get(str(current_qid)))

        if mode == "practice" and action == "check":
            if selected_option:
                exam_state.setdefault("revealed", {})[str(current_qid)] = True
            exam_state["current_index"] = index
            set_exam_state(exam_state)
            save_draft(exam_id, exam_state)
            return redirect(url_for("exam_question", index=index))

        if action == "prev":
            prev_index = max(1, index - 1)
            exam_state["current_index"] = prev_index
            set_exam_state(exam_state)
            save_draft(exam_id, exam_state)
            return redirect(url_for("exam_question", index=prev_index))

        if action == "submit":
            exam_state["current_index"] = index
            set_exam_state(exam_state)
            save_draft(exam_id, exam_state)
            return redirect(url_for("submit_exam"))

        if mode == "practice" and not is_revealed:
            exam_state.setdefault("revealed", {})[str(current_qid)] = True
            exam_state["current_index"] = index
            set_exam_state(exam_state)
            save_draft(exam_id, exam_state)
            return redirect(url_for("exam_question", index=index))

        next_index = min(len(question_ids), index + 1)
        exam_state["current_index"] = next_index
        set_exam_state(exam_state)
        save_draft(exam_id, exam_state)
        return redirect(url_for("exam_question", index=next_index))

    selected_answer = exam_state.get("answers", {}).get(str(current_qid))
    answered_count = len(exam_state.get("answers", {}))
    is_revealed = bool(exam_state.get("revealed", {}).get(str(current_qid)))
    is_correct = selected_answer == current_question["correct_answer_key"] if selected_answer else False

    option_order = get_option_order(exam_state, current_question)
    display_options, correct_display_key = build_display_options(current_question, option_order)

    exam_state["current_index"] = index
    set_exam_state(exam_state)
    save_draft(exam_id, exam_state)

    practice_progress = (
        compute_practice_progress(exam_state, lookup) if mode == "practice" else None
    )

    return render_template(
        "exam.html",
        page_title=f"{question_bank['exam_name']} Mock Exam",
        selected_exam_id=exam_id,
        selected_exam_name=question_bank["exam_name"],
        question=current_question,
        index=index,
        total=len(question_ids),
        selected_answer=selected_answer,
        answered_count=answered_count,
        mode=mode,
        selected_pots=selected_pots,
        is_revealed=is_revealed,
        is_correct=is_correct,
        practice_progress=practice_progress,
        display_options=display_options,
        correct_display_key=correct_display_key,
    )


@app.get("/exam/submit")
def submit_exam():
    exam_state = get_exam_state()
    exam_id = exam_state.get("exam_id", session.get("selected_exam_id", DEFAULT_EXAM_ID))
    question_ids = exam_state.get("question_ids", [])

    if not question_ids:
        return redirect(url_for("index", exam=exam_id))

    exams = discover_exams()
    if exam_id not in exams:
        return redirect(url_for("index", error="Selected exam no longer exists."))

    question_bank = load_question_bank(exam_id, exams)
    lookup = build_question_lookup(question_bank["questions"])

    score = 0
    review = []
    answers = exam_state.get("answers", {})
    all_ids = {q["id"] for q in question_bank["questions"]}
    pots = load_question_pots(exam_id, all_ids)
    selected_pots = exam_state.get("pots", ["unseen", "correct", "incorrect"])

    for qid in question_ids:
        question = lookup[qid]
        selected = answers.get(str(qid))
        is_correct = selected == question["correct_answer_key"]
        if is_correct:
            score += 1

        option_order = get_option_order(exam_state, question)
        display_options, correct_display_key = build_display_options(question, option_order)

        review.append(
            {
                "id": qid,
                "domain": question["domain"],
                "difficulty": question["difficulty"],
                "origin": question["origin"],
                "question": question["question"],
                "options": display_options,
                "selected": selected,
                "selected_text": next(
                    (opt["text"] for opt in question["options"] if opt["key"] == selected),
                    None,
                ),
                "correct": correct_display_key,
                "correct_text": question["correct_answer_text"],
                "is_correct": is_correct,
                "explanation": question["explanation"],
            }
        )

        if selected is None:
            # Skipped questions keep their current pot membership.
            pass
        elif is_correct:
            pots["correct"].add(qid)
            pots["incorrect"].discard(qid)
        else:
            pots["incorrect"].add(qid)
            pots["correct"].discard(qid)

    save_question_pots(exam_id, pots)

    total_questions = len(question_ids)
    score_percent = (score / total_questions * 100) if total_questions else 0.0
    passing_required = math.ceil((PASSING_PERCENT / 100) * total_questions) if total_questions else 0
    passed = score_percent >= PASSING_PERCENT
    finished_at = datetime.now(timezone.utc)

    result_record = {
        "id": str(uuid4()),
        "finished_at": finished_at.isoformat(),
        "score": score,
        "total": total_questions,
        "answered": sum(1 for answer in answers.values() if answer),
        "score_percent": round(score_percent, 1),
        "passing_percent": PASSING_PERCENT,
        "passing_required": passing_required,
        "passed": passed,
        "settings": exam_state.get("settings", {}),
        "pots": selected_pots,
        "exam_id": exam_id,
        "exam_name": question_bank["exam_name"],
        "review": review,
    }

    all_results = load_results(exam_id)
    all_results.append(result_record)
    all_results = all_results[-MAX_RECENT_RESULTS:]
    save_results(exam_id, all_results)
    clear_draft(exam_id)

    exam_state["finished"] = True
    exam_state["result_id"] = result_record["id"]
    set_exam_state(exam_state)

    return redirect(url_for("exam_result"))


@app.get("/exam/result")
def exam_result():
    exam_state = get_exam_state()
    exam_id = exam_state.get("exam_id", session.get("selected_exam_id", DEFAULT_EXAM_ID))
    result_id = exam_state.get("result_id")
    result = None

    if result_id:
        all_results = load_results(exam_id)
        for item in reversed(all_results):
            if item.get("id") == result_id:
                result = item
                break

    # Backward compatibility if an older session still has inline result data.
    if not result:
        result = exam_state.get("result")

    if not result:
        return redirect(url_for("index", exam=exam_id))

    return render_template(
        "result.html",
        page_title=f"{result.get('exam_name', 'Mock Exam')} Result",
        selected_exam_id=exam_id,
        selected_exam_name=result.get("exam_name", "Mock Exam"),
        result=result,
        passing_percent=PASSING_PERCENT,
    )


@app.post("/stats/reset")
def reset_stats():
    exams = discover_exams()
    exam_id = resolve_exam_id(exams) if exams else DEFAULT_EXAM_ID
    save_results(exam_id, [])
    clear_draft(exam_id)
    session.pop("active_exam", None)
    return redirect(url_for("index", exam=exam_id))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )
