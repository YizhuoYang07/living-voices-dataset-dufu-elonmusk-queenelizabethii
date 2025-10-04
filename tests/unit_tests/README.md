# Unit Tests

This directory contains unit tests for individual components.

## Test Structure

```
unit_tests/
├── test_data_collection/    # Tests for data collection utilities
├── test_data_processing/    # Tests for processing functions
├── test_validation/         # Tests for validation logic
└── test_utils/              # Tests for utility functions
```

## Testing Framework

- **Framework**: pytest
- **Coverage Target**: >80%
- **Style**: pytest conventions

## Running Tests

```bash
# Run all unit tests
pytest tests/unit_tests/

# Run with coverage
pytest --cov=living_voices_dataset tests/unit_tests/

# Run specific test file
pytest tests/unit_tests/test_data_collection/test_wikipedia.py
```

---

**Status**: Structure established, tests to be implemented