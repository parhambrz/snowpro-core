# Multi-Course Mock Exam App

A Flask web app for practicing multiple certification mock exams (currently SnowPro Core and Azure DP-900 sample questions).

## Features

- Switchable exam catalog from the dashboard
- Random mock exams from the selected question bank (up to 100 questions per attempt)
- Domain and difficulty filters
- Two study sources:
  - Full Bank
  - Incorrect Review (questions previously answered incorrectly)
- Two exam modes:
  - Exam Mode (standard flow)
  - Practice Mode (check answer + explanation before moving on)
- Finish exam confirmation
- Review page with correct/wrong highlighting and explanations
- Persistent draft (single active draft, resumable)
- Recent attempts and reset statistics

## Project Structure

- `data/exams/<exam-id>/questions.json`: read-only question banks per exam
- `src/app.py`: Flask app
- `src/templates/`: HTML templates
- `src/static/`: CSS
- `src/requirements.txt`: Python dependencies

## Prerequisites

- Python 3.12+ (recommended)
- `python3-venv` installed on Linux

If `venv` creation fails on Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y python3.12-venv
```

## Setup

From repository root:

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the App

From `src` directory with venv active:

```bash
python app.py
```

Open in browser:

- Local: `http://127.0.0.1:5000`
- LAN (same Wi-Fi): `http://<your-laptop-ip>:5000`

## Optional Environment Variables

- `FLASK_HOST` (default: `0.0.0.0`)
- `FLASK_PORT` (default: `5000`)
- `FLASK_DEBUG` (default: `1`)
- `FLASK_SECRET_KEY` (recommended to set for non-dev use)

Example:

```bash
FLASK_HOST=0.0.0.0 FLASK_PORT=5000 FLASK_DEBUG=1 python app.py
```

## Notes About App Data

These files are generated at runtime inside `src/data/exams/<exam-id>/`:

- `exam_results.json`
- `exam_draft.json`
- `incorrect_questions.json`
- `question_pots.json`

They are ignored by Git via `.gitignore`.

## Adding Another Course

1. Create a new folder: `data/exams/<new-exam-id>/`
2. Add `questions.json` in the same format as existing exams.
3. Start the app and select the new exam from the dashboard dropdown.

Runtime state for that course will be isolated under `src/data/exams/<new-exam-id>/`.

## Rebuild SnowPro Question Bank (Optional)

From `src` directory:

```bash
python build_question_bank.py
```

This writes to `data/exams/snowpro-core/questions.json`.

## Quick GitHub Commit Flow

From repository root:

```bash
git add .
git commit -m "Add SnowPro Core mock exam app"
```
