import hashlib
import json
import random
import re
from pathlib import Path

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "used",
    "what",
    "which",
    "with",
    "snowflake",
}

TOPIC_KEYWORDS = {
    "architecture": {"architecture", "layer", "storage", "compute", "services"},
    "warehouse": {
        "warehouse",
        "warehouses",
        "auto-suspend",
        "auto-resume",
        "multi-cluster",
        "concurrency",
    },
    "recovery": {"time", "travel", "fail-safe", "failsafe", "undrop", "retention"},
    "loading": {
        "copy",
        "stage",
        "staged",
        "internal",
        "external",
        "put",
        "get",
        "snowpipe",
        "ingestion",
        "file",
        "format",
        "validation_mode",
        "on_error",
    },
    "semi_structured": {"variant", "json", "parse_json", "flatten", "array", "nested"},
    "pipelines": {"stream", "task", "tasks", "merge", "elt", "pipeline", "incremental"},
    "security": {
        "rbac",
        "role",
        "roles",
        "grant",
        "ownership",
        "policy",
        "masking",
        "row",
        "access",
        "network",
        "mfa",
        "encryption",
        "tri-secret",
        "public",
        "accountadmin",
        "securityadmin",
        "sysadmin",
        "useradmin",
    },
    "sharing": {"share", "sharing", "reader", "consumer", "provider", "live", "read-only"},
    "monitoring": {
        "query",
        "history",
        "account_usage",
        "warehouse_load_history",
        "copy_history",
        "resource",
        "monitor",
        "credits",
        "cost",
        "profile",
    },
    "sql_navigation": {
        "use role",
        "use warehouse",
        "use database",
        "use schema",
        "current schema",
        "active role",
        "active warehouse",
    },
}

TOPIC_DISTRACTOR_LIBRARY = {
    "architecture": [
        "Monolithic architecture where compute and storage scale together.",
        "A single shared compute node for all workloads.",
        "Client-side query execution with local metadata management.",
        "A tightly coupled data warehouse where services run in one layer.",
    ],
    "warehouse": [
        "Increase warehouse size to reduce storage costs.",
        "Disable auto-suspend to improve credit efficiency.",
        "Use one warehouse for all workloads to maximize isolation.",
        "Multi-cluster warehouses are primarily for data encryption.",
        "Warehouse resizing changes micro-partition structure permanently.",
    ],
    "recovery": [
        "Fail-safe can be queried directly by users with SQL.",
        "Time Travel is only available on external stages.",
        "UNDROP is used to resume suspended warehouses.",
        "Fail-safe retention is fully configurable per temporary table.",
    ],
    "loading": [
        "COPY INTO location is used to load files into a table.",
        "PUT uploads files directly into external cloud storage stages.",
        "GET is used to move local files into an internal stage.",
        "Snowpipe requires a running user-managed warehouse.",
        "FILE FORMAT objects are used to grant role privileges.",
    ],
    "semi_structured": [
        "FLATTEN converts VARIANT to encrypted binary only.",
        "PARSE_JSON exports table rows to cloud storage.",
        "VARIANT only supports CSV values and not nested structures.",
        "Semi-structured querying requires disabling micro-partition pruning.",
    ],
    "pipelines": [
        "Tasks capture changed rows while streams schedule cron execution.",
        "Streams duplicate full table data on each change.",
        "MERGE can only insert rows, not update or delete.",
        "Incremental ELT in Snowflake is done with result cache only.",
    ],
    "security": [
        "Grant privileges directly to users for easier governance at scale.",
        "ACCOUNTADMIN should be the default role for daily analytics.",
        "Masking policies control virtual warehouse auto-scaling.",
        "Network policies classify data sensitivity for governance.",
        "PUBLIC grants apply only to explicitly assigned users.",
    ],
    "sharing": [
        "Secure sharing copies data into the consumer account each hour.",
        "Reader accounts require consumers to own a Snowflake account.",
        "Shared data is writable by consumers with SYSADMIN role.",
        "A warehouse object is required to publish a data share.",
    ],
    "monitoring": [
        "QUERY_HISTORY only returns warehouse DDL statements.",
        "COPY_HISTORY is used to define file format parsing rules.",
        "Resource monitors govern row-level data access.",
        "ACCOUNT_USAGE views cannot be used for cost analysis.",
    ],
    "sql_navigation": [
        "USE ACCOUNT switches to account-level role hierarchy.",
        "USE TABLE sets both active database and schema.",
        "ALTER SESSION ROLE changes the object owner permanently.",
        "SET WAREHOUSE is required before any SELECT statement.",
    ],
    "general": [
        "Snowflake requires manual partition management for all tables.",
        "All Snowflake features require Business Critical edition.",
        "Query performance depends only on storage size, not compute.",
        "Data sharing requires ETL copy into consumer-managed schemas.",
    ],
}

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "exams" / "snowpro-core" / "questions.json"
SOURCE_FILES = sorted(DATA_DIR.glob("mock-exam-*.md"))

QUESTION_BLOCK_PATTERN = re.compile(
    r"^##\s+\d+\.\s+(.*?)\n\*\*Answer:\*\*\s+(.*?)(?=\n##\s+\d+\.|\Z)",
    re.MULTILINE | re.DOTALL,
)


def _clean_text(value: str) -> str:
    return " ".join(value.strip().split())


def _tokenize(value: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\-]+", value.lower())
    return {token for token in tokens if token not in STOPWORDS and len(token) > 1}


def _detect_topics(question: str, answer: str) -> set[str]:
    text = f"{question} {answer}".lower()
    text_tokens = _tokenize(text)
    topics = set()
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if " " in keyword:
                if re.search(rf"\b{re.escape(keyword)}\b", text):
                    topics.add(topic)
                    break
            elif keyword in text_tokens:
                topics.add(topic)
                break

    # Architecture terms are broad; prefer specific domains when available.
    if len(topics) > 1 and "architecture" in topics:
        topics.discard("architecture")

    if not topics:
        topics.add("general")
    return topics


def _is_yes_no(answer: str) -> bool:
    a = answer.strip().lower()
    return a.startswith("yes") or a.startswith("no")


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    intersect = len(a.intersection(b))
    union = len(a.union(b))
    return intersect / union if union else 0.0


def parse_source_file(path: Path) -> list[dict]:
    content = path.read_text(encoding="utf-8")
    parsed_questions = []

    for match in QUESTION_BLOCK_PATTERN.finditer(content):
        question = _clean_text(match.group(1))
        answer = _clean_text(match.group(2))

        if not question or not answer:
            continue

        parsed_questions.append(
            {
                "question": question,
                "answer": answer,
                "source_file": path.name,
                "question_tokens": _tokenize(question),
                "answer_tokens": _tokenize(answer),
                "topics": _detect_topics(question, answer),
            }
        )

    return parsed_questions


def build_distractors(current: dict, all_parsed: list[dict], seed: str) -> list[str]:
    correct_answer = current["answer"]
    correct_is_yes_no = _is_yes_no(correct_answer)

    scored_pool = []
    same_topic_pool = []
    for candidate in all_parsed:
        candidate_answer = candidate["answer"]
        if candidate_answer.lower() == correct_answer.lower():
            continue

        topic_overlap = len(current["topics"].intersection(candidate["topics"]))
        question_similarity = _jaccard(current["question_tokens"], candidate["question_tokens"])
        answer_similarity = _jaccard(current["answer_tokens"], candidate["answer_tokens"])

        # Keep distractor answer style close to the correct answer style.
        yes_no_bonus = 0.2 if correct_is_yes_no == _is_yes_no(candidate_answer) else -0.1

        score = topic_overlap * 2.0 + question_similarity * 1.6 + answer_similarity * 1.2 + yes_no_bonus
        scored_pool.append((score, candidate_answer))
        if topic_overlap > 0:
            same_topic_pool.append((score, candidate_answer))

    if len(scored_pool) < 3:
        raise ValueError("Not enough answer choices to build distractors.")

    scored_pool.sort(key=lambda item: item[0], reverse=True)
    same_topic_pool.sort(key=lambda item: item[0], reverse=True)

    synthetic_candidates = []
    for topic in current["topics"]:
        synthetic_candidates.extend(TOPIC_DISTRACTOR_LIBRARY.get(topic, []))
    if not synthetic_candidates:
        synthetic_candidates = TOPIC_DISTRACTOR_LIBRARY["general"]

    ranked_synthetic = []
    for candidate in synthetic_candidates:
        if candidate.lower() == correct_answer.lower():
            continue
        sim_q = _jaccard(current["question_tokens"], _tokenize(candidate))
        sim_a = _jaccard(current["answer_tokens"], _tokenize(candidate))
        score = sim_q * 1.4 + sim_a * 0.9
        ranked_synthetic.append((score, candidate))
    ranked_synthetic.sort(key=lambda item: item[0], reverse=True)

    # Prefer curated topic distractors first, then fallback to real same-topic answers.
    top_pool = []
    seen = set()
    if len(ranked_synthetic) >= 3:
        preferred_pool = ranked_synthetic
    elif len(same_topic_pool) >= 3:
        preferred_pool = same_topic_pool
    else:
        preferred_pool = scored_pool
    for score, answer in preferred_pool:
        key = answer.lower()
        if key in seen:
            continue
        seen.add(key)
        top_pool.append(answer)
        if len(top_pool) >= 20:
            break

    if len(top_pool) < 3:
        top_pool = [answer for _, answer in scored_pool[:20]]

    rng = random.Random(seed)
    distractors = []
    attempts = 0

    while len(distractors) < 3 and attempts < 5000:
        candidate = rng.choice(top_pool)
        attempts += 1
        if candidate.lower() in {opt.lower() for opt in distractors}:
            continue
        distractors.append(candidate)

    if len(distractors) < 3:
        for candidate in top_pool:
            if candidate.lower() in {opt.lower() for opt in distractors}:
                continue
            distractors.append(candidate)
            if len(distractors) == 3:
                break

    return distractors[:3]


def build_question_bank() -> dict:
    all_parsed = []

    for source in SOURCE_FILES:
        all_parsed.extend(parse_source_file(source))

    if len(all_parsed) == 0:
        raise RuntimeError("No questions found in source markdown files.")

    questions = []
    for idx, item in enumerate(all_parsed, start=1):
        seed_material = f"{item['question']}::{item['answer']}::{item['source_file']}"
        seed = hashlib.sha256(seed_material.encode("utf-8")).hexdigest()

        distractors = build_distractors(item, all_parsed, seed)
        options = [item["answer"], *distractors]

        rng = random.Random(seed)
        rng.shuffle(options)

        question_obj = {
            "id": idx,
            "question": item["question"],
            "options": options,
            "correct_answer": item["answer"],
            "correct_option_index": options.index(item["answer"]),
            "source": {
                "file": item["source_file"],
            },
            "metadata": {
                "version": 1,
            },
        }
        questions.append(question_obj)

    return {
        "schema_version": 1,
        "title": "SnowPro Core Combined Mock Bank",
        "description": "Generated from all mock-exam markdown files.",
        "question_count": len(questions),
        "questions": questions,
    }


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = build_question_bank()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {payload['question_count']} questions to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
