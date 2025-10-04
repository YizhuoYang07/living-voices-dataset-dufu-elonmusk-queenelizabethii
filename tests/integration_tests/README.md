# Integration Tests

This directory contains integration tests for end-to-end workflows.

## Test Scenarios

1. **Data Pipeline**: Collection → Processing → Validation
2. **RAG Pipeline**: Query → Retrieval → Generation → Response
3. **Multi-persona**: Handling multiple personas simultaneously
4. **Cross-lingual**: Chinese-English data handling

## Test Structure

```
integration_tests/
├── test_data_pipeline/      # Full data processing pipeline
├── test_rag_pipeline/       # Complete RAG workflow
├── test_api_endpoints/      # API integration tests
└── test_performance/        # Performance and stress tests
```

## Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration_tests/

# Run specific test suite
pytest tests/integration_tests/test_rag_pipeline/
```

---

**Status**: Structure established, tests to be implemented