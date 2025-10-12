"""
pytest configuration and shared fixtures for Living Voices Dataset tests.

This module provides reusable fixtures and configuration for the test suite,
following pytest best practices for NLP dataset validation.
"""

import json
import pytest
from pathlib import Path
from typing import Dict, List, Any


# Test configuration
pytest_plugins = []


@pytest.fixture(scope="session")
def dataset_root() -> Path:
    """
    Fixture providing path to dataset root directory.
    
    Returns:
        Path: Absolute path to dataset root
    """
    current_file = Path(__file__).resolve()
    tests_dir = current_file.parent
    dataset_root_path = tests_dir.parent
    return dataset_root_path


@pytest.fixture(scope="session")
def datasets_dir(dataset_root: Path) -> Path:
    """
    Fixture providing path to datasets directory.
    
    Args:
        dataset_root: Root directory fixture
        
    Returns:
        Path: Path to datasets/ directory
    """
    return dataset_root / "datasets"


@pytest.fixture(scope="session")
def metadata_path(datasets_dir: Path) -> Path:
    """
    Fixture providing path to metadata directory.
    
    Args:
        datasets_dir: Datasets directory fixture
        
    Returns:
        Path: Path to datasets/metadata/ directory
    """
    return datasets_dir / "metadata"


@pytest.fixture(scope="session")
def statistics_file(metadata_path: Path) -> Path:
    """
    Fixture providing path to statistics.json file.
    
    Args:
        metadata_path: Metadata directory fixture
        
    Returns:
        Path: Path to statistics.json
    """
    return metadata_path / "statistics.json"


@pytest.fixture(scope="session")
def statistics_data(statistics_file: Path) -> Dict[str, Any]:
    """
    Fixture providing loaded statistics data.
    
    Args:
        statistics_file: Statistics file path fixture
        
    Returns:
        dict: Parsed statistics data
    """
    with open(statistics_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def persona_identifiers() -> List[str]:
    """
    Fixture providing list of expected persona identifiers.
    
    Returns:
        list: Persona identifier strings
    """
    return ["du_fu", "elon_musk", "queen_elizabeth_ii"]


@pytest.fixture(scope="session")
def persona_display_names() -> Dict[str, str]:
    """
    Fixture providing mapping of persona IDs to display names.
    
    Returns:
        dict: Mapping of persona_id -> display_name
    """
    return {
        "du_fu": "Du Fu (杜甫)",
        "elon_musk": "Elon Musk",
        "queen_elizabeth_ii": "Queen Elizabeth II"
    }


@pytest.fixture(scope="session")
def expected_document_counts() -> Dict[str, int]:
    """
    Fixture providing expected document counts per persona.
    
    Returns:
        dict: Mapping of persona_id -> expected_document_count
    """
    return {
        "du_fu": 1496,
        "elon_musk": 48,
        "queen_elizabeth_ii": 22
    }


@pytest.fixture(scope="session")
def expected_chunk_counts() -> Dict[str, int]:
    """
    Fixture providing expected chunk counts per persona.
    
    Returns:
        dict: Mapping of persona_id -> expected_chunk_count
    """
    return {
        "du_fu": 3449,
        "elon_musk": 96,
        "queen_elizabeth_ii": 341
    }


@pytest.fixture(scope="session")
def required_metadata_fields() -> List[str]:
    """
    Fixture providing list of required metadata fields.
    
    Returns:
        list: Required field names
    """
    return [
        "chunk_id",
        "document_id",
        "persona_id",
        "text",
        "language",
        "source",
        "timestamp"
    ]


@pytest.fixture(scope="session")
def iso_language_codes() -> Dict[str, str]:
    """
    Fixture providing expected ISO 639-3 language codes.
    
    Returns:
        dict: Mapping of language_name -> ISO_639_3_code
    """
    return {
        "Classical Chinese": "lzh",
        "English": "eng"
    }


@pytest.fixture
def sample_chunk_schema() -> Dict[str, Any]:
    """
    Fixture providing example chunk schema for validation.
    
    Returns:
        dict: Example chunk data structure
    """
    return {
        "chunk_id": "du_fu_poem_0001_chunk_001",
        "document_id": "du_fu_poem_0001",
        "persona_id": "du_fu",
        "text": "春望\n國破山河在，城春草木深。",
        "language": "lzh",
        "source": "Quan Tang Shi",
        "timestamp": "2024-10-04T00:00:00Z",
        "metadata": {
            "title": "春望",
            "composition_date": "757 CE",
            "genre": "regulated_verse"
        }
    }


@pytest.fixture
def persona_directories(datasets_dir: Path, persona_identifiers: List[str]) -> Dict[str, Path]:
    """
    Fixture providing paths to persona-specific directories.
    
    Args:
        datasets_dir: Datasets directory fixture
        persona_identifiers: List of persona IDs
        
    Returns:
        dict: Mapping of persona_id -> directory_path
    """
    return {
        persona_id: datasets_dir / persona_id
        for persona_id in persona_identifiers
    }


def pytest_configure(config):
    """
    pytest configuration hook.
    
    Registers custom markers for test categorization.
    """
    config.addinivalue_line(
        "markers", "integrity: marks tests for data integrity validation"
    )
    config.addinivalue_line(
        "markers", "schema: marks tests for schema compliance"
    )
    config.addinivalue_line(
        "markers", "quality: marks tests for data quality metrics"
    )
    config.addinivalue_line(
        "markers", "statistics: marks tests for statistics verification"
    )
    config.addinivalue_line(
        "markers", "completeness: marks tests for data completeness"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests that are slow to execute"
    )


def pytest_collection_modifyitems(config, items):
    """
    pytest hook to modify test collection.
    
    Automatically marks slow tests based on execution patterns.
    """
    for item in items:
        # Mark tests that iterate over all files as potentially slow
        if "all_json" in item.nodeid or "all_chunks" in item.nodeid:
            item.add_marker(pytest.mark.slow)
