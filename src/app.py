import json
import os
import random
import math
from collections import defaultdict
from uuid import uuid4
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
QUESTION_BANK_FILE = BASE_DIR.parent / "data" / "snowpro_core_questions.json"
RESULTS_FILE = BASE_DIR / "data" / "exam_results.json"
DRAFT_FILE = BASE_DIR / "data" / "exam_draft.json"
INCORRECT_FILE = BASE_DIR / "data" / "incorrect_questions.json"
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


def load_question_bank() -> dict:
    if not QUESTION_BANK_FILE.exists():
        raise FileNotFoundError(
            "snowpro_core_questions.json not found in /data."
        )
    with QUESTION_BANK_FILE.open("r", encoding="utf-8") as file:
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
        "exam_name": raw.get("examName", "SnowPro Core"),
        "question_count": len(normalized_questions),
        "questions": normalized_questions,
    }


def load_results() -> list[dict]:
    if not RESULTS_FILE.exists():
        return []
    with RESULTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results: list[dict]) -> None:
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)


def load_draft() -> dict | None:
    if not DRAFT_FILE.exists():
        return None
    with DRAFT_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_draft(state: dict) -> None:
    DRAFT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DRAFT_FILE.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)


def clear_draft() -> None:
    if DRAFT_FILE.exists():
        DRAFT_FILE.unlink()


def load_incorrect_bank() -> set[int]:
    if not INCORRECT_FILE.exists():
        return set()
    with INCORRECT_FILE.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    ids = payload.get("question_ids", [])
    return {int(qid) for qid in ids}


def save_incorrect_bank(question_ids: set[int]) -> None:
    INCORRECT_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "question_ids": sorted(question_ids),
        "count": len(question_ids),
    }
    with INCORRECT_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def build_question_lookup(questions: list[dict]) -> dict[int, dict]:
    return {q["id"]: q for q in questions}


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
    question_bank = load_question_bank()
    questions = question_bank["questions"]
    incorrect_bank = load_incorrect_bank()
    all_results = load_results()
    recent_results = list(reversed(all_results[-MAX_RECENT_RESULTS:]))
    available_domains = sorted({q["domain"] for q in questions})
    available_difficulties = sorted({q["difficulty"] for q in questions})
    available_origins = sorted({q["origin"] for q in questions})
    error_message = request.args.get("error")
    draft = load_draft()

    draft_summary = None
    if draft and draft.get("question_ids"):
        draft_total = len(draft.get("question_ids", []))
        draft_answers = draft.get("answers", {})
        draft_summary = {
            "mode": draft.get("mode", "exam"),
            "source": draft.get("source", "regular"),
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
        "incorrect_bank_count": len(incorrect_bank),
    }

    return render_template(
        "index.html",
        stats=stats,
        recent_results=recent_results,
        passing_percent=PASSING_PERCENT,
        exam_size=EXAM_SIZE,
        available_domains=available_domains,
        available_difficulties=available_difficulties,
        available_origins=available_origins,
        error_message=error_message,
        draft_summary=draft_summary,
    )


@app.post("/exam/start")
def start_exam():
    question_bank = load_question_bank()
    questions = question_bank["questions"]
    question_lookup = {q["id"]: q for q in questions}
    incorrect_bank = load_incorrect_bank()
    selected_domains = set(request.form.getlist("domains"))
    selected_difficulties = {d.lower() for d in request.form.getlist("difficulties")}
    selected_origins = set(request.form.getlist("origins"))
    mode = request.form.get("mode", "exam").strip().lower()
    source = request.form.get("source", "regular").strip().lower()
    if mode not in {"exam", "practice"}:
        mode = "exam"
    if source not in {"regular", "incorrect"}:
        source = "regular"

    base_questions = questions
    if source == "incorrect":
        if not incorrect_bank:
            return redirect(
                url_for(
                    "index",
                    error=(
                        "All questions are learned. There are no incorrectly answered "
                        "questions to review right now."
                    ),
                )
            )
        base_questions = [question_lookup[qid] for qid in sorted(incorrect_bank) if qid in question_lookup]

        if not base_questions:
            save_incorrect_bank(set())
            return redirect(
                url_for(
                    "index",
                    error=(
                        "All questions are learned. There are no incorrectly answered "
                        "questions to review right now."
                    ),
                )
            )

    filtered_questions = [
        q
        for q in base_questions
        if (not selected_domains or q["domain"] in selected_domains)
        and (not selected_difficulties or q["difficulty"] in selected_difficulties)
        and (not selected_origins or q["origin"] in selected_origins)
    ]

    if len(filtered_questions) == 0:
        return redirect(
            url_for(
                "index",
                error=(
                    "No questions found for the selected filters. "
                    "Please broaden your domain/difficulty selection."
                ),
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
        "finished": False,
        "mode": mode,
        "source": source,
        "current_index": 1,
        "settings": {
            "domains": sorted(selected_domains),
            "difficulties": sorted(selected_difficulties),
            "origins": sorted(selected_origins),
        },
    }
    set_exam_state(exam_state)
    save_draft(exam_state)

    return redirect(url_for("exam_question", index=1))


@app.get("/exam/resume")
def resume_exam():
    draft = load_draft()
    if not draft or not draft.get("question_ids"):
        return redirect(url_for("index", error="No saved draft exam found."))

    set_exam_state(draft)
    resume_index = int(draft.get("current_index") or compute_resume_index(draft["question_ids"], draft.get("answers", {})))
    resume_index = max(1, min(len(draft["question_ids"]), resume_index))
    return redirect(url_for("exam_question", index=resume_index))


@app.post("/exam/discard")
def discard_exam():
    clear_draft()
    session.pop("active_exam", None)
    return redirect(url_for("index"))


@app.route("/exam/<int:index>", methods=["GET", "POST"])
def exam_question(index: int):
    exam_state = get_exam_state()
    question_ids = exam_state.get("question_ids", [])

    if not question_ids:
        return redirect(url_for("index"))

    if exam_state.get("finished"):
        return redirect(url_for("exam_result"))

    if index < 1 or index > len(question_ids):
        return redirect(url_for("exam_question", index=1))

    question_bank = load_question_bank()
    lookup = build_question_lookup(question_bank["questions"])

    current_qid = question_ids[index - 1]
    current_question = lookup[current_qid]
    mode = exam_state.get("mode", "exam")
    source = exam_state.get("source", "regular")

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
            save_draft(exam_state)
            return redirect(url_for("exam_question", index=index))

        if action == "prev":
            prev_index = max(1, index - 1)
            exam_state["current_index"] = prev_index
            set_exam_state(exam_state)
            save_draft(exam_state)
            return redirect(url_for("exam_question", index=prev_index))

        if action == "submit":
            exam_state["current_index"] = index
            set_exam_state(exam_state)
            save_draft(exam_state)
            return redirect(url_for("submit_exam"))

        if mode == "practice" and not is_revealed:
            exam_state.setdefault("revealed", {})[str(current_qid)] = True
            exam_state["current_index"] = index
            set_exam_state(exam_state)
            save_draft(exam_state)
            return redirect(url_for("exam_question", index=index))

        next_index = min(len(question_ids), index + 1)
        exam_state["current_index"] = next_index
        set_exam_state(exam_state)
        save_draft(exam_state)
        return redirect(url_for("exam_question", index=next_index))

    selected_answer = exam_state.get("answers", {}).get(str(current_qid))
    answered_count = len(exam_state.get("answers", {}))
    is_revealed = bool(exam_state.get("revealed", {}).get(str(current_qid)))
    is_correct = selected_answer == current_question["correct_answer_key"] if selected_answer else False

    exam_state["current_index"] = index
    set_exam_state(exam_state)
    save_draft(exam_state)

    return render_template(
        "exam.html",
        question=current_question,
        index=index,
        total=len(question_ids),
        selected_answer=selected_answer,
        answered_count=answered_count,
        mode=mode,
        source=source,
        is_revealed=is_revealed,
        is_correct=is_correct,
    )


@app.get("/exam/submit")
def submit_exam():
    exam_state = get_exam_state()
    question_ids = exam_state.get("question_ids", [])

    if not question_ids:
        return redirect(url_for("index"))

    question_bank = load_question_bank()
    lookup = build_question_lookup(question_bank["questions"])

    score = 0
    review = []
    answers = exam_state.get("answers", {})
    source = exam_state.get("source", "regular")
    incorrect_bank = load_incorrect_bank()

    for qid in question_ids:
        question = lookup[qid]
        selected = answers.get(str(qid))
        is_correct = selected == question["correct_answer_key"]
        if is_correct:
            score += 1

        review.append(
            {
                "id": qid,
                "domain": question["domain"],
                "difficulty": question["difficulty"],
                "origin": question["origin"],
                "question": question["question"],
                "options": question["options"],
                "selected": selected,
                "selected_text": next(
                    (opt["text"] for opt in question["options"] if opt["key"] == selected),
                    None,
                ),
                "correct": question["correct_answer_key"],
                "correct_text": question["correct_answer_text"],
                "is_correct": is_correct,
                "explanation": question["explanation"],
            }
        )

        if source == "incorrect":
            if selected is None:
                continue
            if is_correct:
                incorrect_bank.discard(qid)
            else:
                incorrect_bank.add(qid)
        elif selected is not None and not is_correct:
            incorrect_bank.add(qid)

    save_incorrect_bank(incorrect_bank)

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
        "source": source,
        "review": review,
    }

    all_results = load_results()
    all_results.append(result_record)
    all_results = all_results[-MAX_RECENT_RESULTS:]
    save_results(all_results)
    clear_draft()

    exam_state["finished"] = True
    exam_state["result_id"] = result_record["id"]
    set_exam_state(exam_state)

    return redirect(url_for("exam_result"))


@app.get("/exam/result")
def exam_result():
    exam_state = get_exam_state()
    result_id = exam_state.get("result_id")
    result = None

    if result_id:
        all_results = load_results()
        for item in reversed(all_results):
            if item.get("id") == result_id:
                result = item
                break

    # Backward compatibility if an older session still has inline result data.
    if not result:
        result = exam_state.get("result")

    if not result:
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        result=result,
        passing_percent=PASSING_PERCENT,
    )


@app.post("/stats/reset")
def reset_stats():
    save_results([])
    clear_draft()
    session.pop("active_exam", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )
