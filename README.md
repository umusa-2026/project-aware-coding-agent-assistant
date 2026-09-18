# Project-Aware Coding Agent Assistant

## Goal

Build a local assistant that retrieves relevant engineering history, extracts verified lessons, and prepares actionable context for a coding agent. Improve its knowledge through user corrections and execution feedback before introducing reinforcement learning.

## Minimum Viable Features

* **Task understanding:** Identify the project, objective, relevant components, constraints, and completion criteria.
* **Accurate retrieval:** Find identical or highly relevant historical cases and cite their source passages. Explicitly report when no reliable match exists.
* **Evidence-based lessons:** Extract successful solutions, failed attempts, pitfalls, verification results, and applicability conditions.
* **Task guidance:** Explain how historical lessons apply to the current task, including differences and required checks.
* **Coding-agent handoff:** Generate a concise Markdown brief for user review and delivery to a coding agent.
* **Feedback and revision:** Record corrections and execution outcomes; revise lessons while preserving their sources and change history.

## Implementation Roadmap

### 1. Establish the Development Environment

Use the personal MacBook as the primary development environment for the public repository. Set up Python, Git, and one coding tool, initially Aider with Ollama.

Maintain environment-specific configuration and keep runtime data outside the source repository.

### 2. Build a Small Corpus and Evaluation Set

Start with local Markdown or text exports. Preserve document identifiers, dates, project labels, source links, and section references.

Create evaluation tasks covering exact matches, similar cases, misleading matches, and missing answers. Use personal or independently constructed examples for public tests.

### 3. Implement and Evaluate Retrieval

Establish a keyword-search baseline, then add semantic retrieval and candidate reranking. Return a small set of relevant passages with sources and relevance explanations.

Initial target: retrieve key evidence within the top three results for at least 80% of answerable evaluation tasks. Separately inspect irrelevant matches and unsupported answers.

### 4. Extract and Apply Lessons

Represent each lesson with:

* Problem and operating conditions.
* Failed attempts and final solution.
* Verification evidence and source references.
* Applicability limits and status.

Generate a task brief containing relevant lessons, current differences, recommended actions, and validation requirements.

### 5. Close the Feedback Loop

Follow this workflow:

**Task → retrieval → lesson extraction → user review → coding-agent execution → evidence collection → user feedback → knowledge revision.**

Track retrieval relevance, extraction accuracy, recommendation applicability, and execution outcomes separately. A proposed solution must remain unverified until supported by evidence.

### 6. Add Incremental Updates and Real-Task Validation

Process new or changed documents, detect duplicate or conflicting lessons, and rerun retrieval evaluations.

Pilot the assistant on 5–10 real tasks. Measure context-preparation time, useful lessons recovered, repeated mistakes avoided, and correction effort.

## Environment and Synchronization

Develop and publish generic code from the personal environment. Where permitted, install tagged releases in the work environment for internal evaluation.

Keep company documents, indexes, extracted lessons, credentials, and task logs within the approved work environment. Work-generated changes may enter the public repository only when authorized for release.

## Later Extensions

Add Google Docs ingestion, automated coding-agent handoff, and feedback-driven decision policies after the basic workflow is reliable. Introduce reinforcement learning only when a specific decision problem, sufficient feedback, and a measurable baseline exist.
