---
name: create-exam-question-bank
description: 'Create, expand, or review AI-generated certification mock-exam question banks. Use when researching an exam blueprint, generating realistic questions and distractors, matching official domain weights and difficulty, or validating question-bank quality.'
---

# Create an Exam Question Bank

Build a fair practice bank that resembles the current official exam in scope, wording, reasoning, and difficulty without copying real exam questions or using exam dumps.

## 1. Establish the Exam Contract

Before writing questions:

1. Use current, authoritative sources: the exam provider's skills outline, exam guide, product documentation, and published sample questions.
2. Record the exam code and version, domain names and weights, question formats, exam size, and expected difficulty.
3. Note the source date. Do not rely on obsolete product behavior or undocumented claims.
4. Inspect `data/exams/snowpro-core/questions.json` and `data/exams/azure-dp-900/questions.json` as repository quality and schema references.
5. Convert domain weights into question-count targets. Include enough extra questions in each domain to support randomized attempts without excessive repetition.

If official details are unavailable, state the assumptions instead of inventing exam rules.

## 2. Write Realistic Questions

- Test one blueprint objective per question.
- Match the official style: concise knowledge checks for fundamentals and short scenarios for applied decisions.
- Prefer questions that require understanding, comparison, or selecting the best solution. Do not rely mostly on trivia or term recall.
- Include all facts needed to answer. Remove irrelevant story details and accidental ambiguity.
- Use the provider's current terminology and technically accurate behavior.
- Keep difficulty labels meaningful: `basic` tests core recognition, `intermediate` tests application or comparison, and `advanced` tests tradeoffs or multi-step reasoning.
- Do not use trick wording. Use `NOT`, `EXCEPT`, or absolute terms only when the official exam uses them and emphasize them clearly.
- Never copy leaked, memorized, or proprietary live-exam items.

## 3. Design Choices Without Answer Leakage

- Provide exactly one unambiguously best answer unless the application schema explicitly supports multiple answers.
- Make every distractor relevant to the same product, concept, and scenario. A distractor should be plausible to a learner with a specific misconception.
- Keep choices grammatically parallel and similar in specificity, tone, and length.
- Do not make the correct answer consistently longer, more detailed, more qualified, or better written than the distractors.
- Do not reveal the answer through repeated words from the stem, unique jargon, category mismatch, or one choice containing all other choices.
- Avoid joke, absurd, impossible, and unrelated options. For example, a cloud-services question must contain only credible cloud-related choices.
- Avoid overlapping choices unless the overlap itself is what the question tests.
- Distribute correct positions approximately evenly across `A`, `B`, `C`, and `D`; never use a predictable sequence.
- Do not use `All of the above` or `None of the above` unless required by the official exam style.

## 4. Explain the Answer

Every question needs a concise explanation that:

- states why the correct choice is correct;
- identifies the deciding fact or tradeoff;
- clarifies why close distractors fail when that is not obvious;
- teaches the concept without merely repeating the answer text;
- does not introduce claims unsupported by authoritative documentation.

## 5. Preserve the Repository Schema

Follow the existing `questions.json` structure:

```json
{
  "id": 1,
  "domain": "Official domain name",
  "difficulty": "intermediate",
  "origin": "AI generated",
  "question": "Question text",
  "choices": {
    "A": "Plausible choice",
    "B": "Plausible choice",
    "C": "Plausible choice",
    "D": "Plausible choice"
  },
  "correctAnswer": "B",
  "explanation": "Why B is correct and the relevant distinction."
}
```

Keep IDs unique and stable. Ensure top-level `examName`, `version`, `examSize`, `totalQuestions`, and `domains` agree with the question data. Use exact official domain names consistently.

## 6. Validate Before Delivery

Reject or revise any item that fails one of these checks:

- **Correctness:** The keyed answer and explanation agree with current authoritative sources.
- **Blueprint fit:** The item maps clearly to an official objective and domain.
- **Single best answer:** No distractor is also correct under a reasonable reading.
- **Plausibility:** Every choice belongs in the scenario and represents a credible misconception or alternative.
- **No leakage:** The answer cannot be guessed from length, detail, grammar, formatting, or vocabulary alone.
- **Clarity:** The stem is self-contained and has only the ambiguity intended by the exam.
- **Originality:** The item is newly written, not copied from a live exam or dump.
- **Coverage:** Counts approximately match official domain weights, with a deliberate mix of difficulty and scenario types.
- **Distribution:** Correct-answer letters are balanced overall and within large domains.
- **Integrity:** IDs are unique, answer keys exist in `choices`, JSON is valid, and `totalQuestions` equals the array length.

Review questions individually and review the bank statistically. In particular, compare correct-answer length with distractor lengths by domain; investigate any strong pattern even if each question seems acceptable in isolation.