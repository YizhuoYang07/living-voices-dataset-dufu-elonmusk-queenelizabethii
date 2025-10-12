# Living Voices Dataset - Test Suite

## Overview

This directory contains comprehensive test suites for validating the Living Voices Dataset infrastructure. The test framework ensures data integrity, schema compliance, and quality metrics verification following best practices in dataset validation for Natural Language Processing research.

## Test Organization

### Test Modules

```
tests/
├── README.md                      # This file
├── conftest.py                    # pytest configuration and fixtures
├── test_data_integrity.py         # Data loading and format validation
├── test_metadata_schema.py        # Schema compliance verification
├── test_chunk_quality.py          # Chunk size and quality validation
├── test_statistics_accuracy.py    # Statistics verification
└── test_data_completeness.py      # Coverage and completeness checks
```

## Test Categories

### 1. Data Integrity Tests

**Purpose**: Verify that all data files load correctly and conform to expected formats.

**Coverage**:
- JSON file parsing and validation
- UTF-8 encoding verification
- File existence and accessibility
- Data structure consistency

**Test File**: `test_data_integrity.py`

### 2. Metadata Schema Tests

**Purpose**: Ensure all metadata records comply with defined schemas (Dublin Core, Schema.org, DataCite).

**Coverage**:
- Required field presence
- Field type validation
- ISO standard compliance (ISO 639-3, ISO 8601, SPDX)
- Hierarchical identifier consistency

**Test File**: `test_metadata_schema.py`

### 3. Chunk Quality Tests

**Purpose**: Validate that text chunks meet quality standards and size constraints.

**Coverage**:
- Chunk size distribution analysis
- Empty or malformed chunk detection
- Persona-specific chunking strategy verification
- Content-metadata linkage validation

**Test File**: `test_chunk_quality.py`

### 4. Statistics Accuracy Tests

**Purpose**: Verify that reported statistics match actual dataset contents.

**Coverage**:
- Document count verification
- Chunk count verification
- Content volume validation
- Persona-specific metric accuracy

**Test File**: `test_statistics_accuracy.py`

### 5. Data Completeness Tests

**Purpose**: Ensure comprehensive coverage and no missing data.

**Coverage**:
- Expected file presence
- Persona coverage verification
- Metadata field completeness
- Cross-reference integrity

**Test File**: `test_data_completeness.py`

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-json-report

# Install dataset dependencies
pip install -r requirements.txt
```

### Basic Test Execution

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_data_integrity.py

# Run with verbose output
pytest tests/ -v

# Run with detailed output
pytest tests/ -vv
```

### Coverage Analysis

```bash
# Generate coverage report
pytest tests/ --cov=datasets --cov-report=html

# Generate terminal coverage summary
pytest tests/ --cov=datasets --cov-report=term-missing

# Generate XML coverage report (for CI/CD)
pytest tests/ --cov=datasets --cov-report=xml
```

### JSON Report Generation

```bash
# Generate machine-readable test report
pytest tests/ --json-report --json-report-file=test_results.json
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Dataset Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=datasets --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Test Fixtures

### Available Fixtures (conftest.py)

- `dataset_root`: Path to dataset root directory
- `metadata_path`: Path to metadata directory
- `statistics_file`: Path to statistics.json
- `sample_personas`: List of persona identifiers
- `sample_chunks`: Sample chunk data for testing

## Expected Test Results

### Quality Metrics

- **Test Coverage**: Target 90%+ line coverage
- **Pass Rate**: All tests should pass (100%)
- **Execution Time**: Complete suite should run in under 30 seconds

### Known Test Conditions

**Du Fu (杜甫)**:
- Expected documents: 1,496
- Expected chunks: 3,449
- Content measured in characters (Classical Chinese)

**Elon Musk**:
- Expected documents: 48
- Expected chunks: 96
- Content measured in words (English)

**Queen Elizabeth II**:
- Expected documents: 22
- Expected chunks: 341
- Content measured in words (English)

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError` during tests
**Solution**: Ensure tests are run from repository root or set `PYTHONPATH` correctly

**Issue**: `UnicodeDecodeError` on JSON files
**Solution**: Verify all files are UTF-8 encoded without BOM

**Issue**: Statistics mismatch
**Solution**: Regenerate statistics.json if dataset has been updated

### Debugging Failed Tests

```bash
# Run with Python debugger
pytest tests/ --pdb

# Run with step-by-step execution
pytest tests/ -s

# Run single test with maximum verbosity
pytest tests/test_data_integrity.py::test_load_all_json_files -vv
```

## Test Maintenance

### Updating Tests

When dataset structure changes:
1. Update corresponding test module
2. Update expected values in conftest.py
3. Regenerate statistics if needed
4. Run full test suite to verify

### Adding New Tests

Follow existing patterns:
1. Create descriptive test function names
2. Use fixtures for common setup
3. Include docstrings explaining test purpose
4. Assert specific conditions with clear messages

## References

**Testing Best Practices**:
- Gebru, T., et al. (2021). "Datasheets for Datasets." Communications of the ACM.
- Bender, E. M., & Friedman, B. (2018). "Data Statements for Natural Language Processing."

**Testing Frameworks**:
- pytest documentation: https://docs.pytest.org/
- pytest-cov documentation: https://pytest-cov.readthedocs.io/

## Version History

- **v1.0.0** (2025-10-12): Initial test suite creation
  - Comprehensive coverage of five test categories
  - Integration with dataset v1.0.0
  - Documentation and CI/CD templates

## Contact

For questions about test suite implementation or failures, refer to the main project documentation or raise an issue in the repository.
