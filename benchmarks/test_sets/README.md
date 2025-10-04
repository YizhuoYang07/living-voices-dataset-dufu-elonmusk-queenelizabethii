# Test Sets

This directory contains standardized test sets for evaluation.

## Test Set Categories

### 1. Factual Questions
Test the system's ability to retrieve and present accurate factual information.

### 2. Opinion Questions
Test persona-specific viewpoints and perspectives.

### 3. Temporal Questions
Test understanding of chronological context.

### 4. Cross-lingual Questions
Test Chinese-English capability (for Du Fu persona).

### 5. Style Questions
Test maintenance of persona-specific communication style.

## Test Set Format

```json
{
  "test_id": "unique_id",
  "persona": "persona_name",
  "question": "test question",
  "expected_topics": ["topic1", "topic2"],
  "evaluation_criteria": {
    "factual_accuracy": true,
    "style_consistency": true,
    "response_relevance": true
  }
}
```

---

**Status**: Structure established, test sets to be developed