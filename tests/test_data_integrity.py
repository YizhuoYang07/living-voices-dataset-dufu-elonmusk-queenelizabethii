"""
Data Integrity Tests for Living Voices Dataset.

This module validates that all data files load correctly, conform to expected
formats, and maintain UTF-8 encoding consistency.

Test Categories:
    - JSON file parsing and validation
    - UTF-8 encoding verification
    - File existence checks
    - Data structure consistency
"""

import json
import pytest
from pathlib import Path
from typing import List, Dict, Any


@pytest.mark.integrity
class TestJSONFileIntegrity:
    """Test suite for JSON file loading and parsing."""
    
    def test_statistics_file_loads(self, statistics_file: Path):
        """
        Verify that statistics.json loads without errors.
        
        Args:
            statistics_file: Path fixture to statistics.json
        """
        assert statistics_file.exists(), f"Statistics file not found: {statistics_file}"
        
        with open(statistics_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "Statistics file must contain a JSON object"
        assert len(data) > 0, "Statistics file must not be empty"
    
    def test_statistics_has_required_keys(self, statistics_data: Dict[str, Any]):
        """
        Verify that statistics.json contains all required top-level keys.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        required_keys = [
            "dataset_version",
            "overview",
            "personas",
            "quality_metrics",
            "distribution"
        ]
        
        for key in required_keys:
            assert key in statistics_data, f"Missing required key in statistics: {key}"
    
    def test_all_metadata_files_load(self, metadata_path: Path):
        """
        Verify that all JSON files in metadata directory load successfully.
        
        Args:
            metadata_path: Path fixture to metadata directory
        """
        json_files = list(metadata_path.glob("*.json"))
        assert len(json_files) > 0, "No JSON files found in metadata directory"
        
        failed_files = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except Exception as e:
                failed_files.append((json_file.name, str(e)))
        
        assert len(failed_files) == 0, \
            f"Failed to load {len(failed_files)} JSON files: {failed_files}"
    
    def test_persona_directories_exist(self, datasets_dir: Path, 
                                      persona_identifiers: List[str]):
        """
        Verify that all expected persona directories exist.
        
        Args:
            datasets_dir: Path fixture to datasets directory
            persona_identifiers: List of expected persona IDs
        """
        for persona_id in persona_identifiers:
            persona_dir = datasets_dir / persona_id
            assert persona_dir.exists(), f"Persona directory not found: {persona_id}"
            assert persona_dir.is_dir(), f"Persona path is not a directory: {persona_id}"


@pytest.mark.integrity
class TestEncodingConsistency:
    """Test suite for UTF-8 encoding validation."""
    
    def test_statistics_utf8_encoding(self, statistics_file: Path):
        """
        Verify that statistics.json uses UTF-8 encoding.
        
        Args:
            statistics_file: Path fixture to statistics.json
        """
        # This test passes if file opens without UnicodeDecodeError
        with open(statistics_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content) > 0, "Statistics file is empty"
    
    def test_metadata_files_utf8_encoding(self, metadata_path: Path):
        """
        Verify that all metadata JSON files use UTF-8 encoding.
        
        Args:
            metadata_path: Path fixture to metadata directory
        """
        json_files = list(metadata_path.glob("*.json"))
        
        encoding_errors = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    f.read()
            except UnicodeDecodeError as e:
                encoding_errors.append((json_file.name, str(e)))
        
        assert len(encoding_errors) == 0, \
            f"UTF-8 encoding errors in {len(encoding_errors)} files: {encoding_errors}"
    
    def test_no_byte_order_mark(self, statistics_file: Path):
        """
        Verify that JSON files do not contain UTF-8 BOM.
        
        Args:
            statistics_file: Path fixture to statistics.json
        """
        with open(statistics_file, 'rb') as f:
            first_bytes = f.read(3)
        
        # UTF-8 BOM is EF BB BF
        assert first_bytes != b'\xef\xbb\xbf', \
            "File contains UTF-8 BOM, which should be removed"


@pytest.mark.integrity
class TestDataStructureConsistency:
    """Test suite for data structure validation."""
    
    def test_persona_data_structure(self, statistics_data: Dict[str, Any],
                                   persona_identifiers: List[str]):
        """
        Verify that each persona has consistent data structure.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data.get("personas", {})
        
        for persona_id in persona_identifiers:
            assert persona_id in personas, f"Missing persona in statistics: {persona_id}"
            
            persona_data = personas[persona_id]
            required_fields = ["display_name", "type", "language", "era", 
                             "documents", "chunks", "content"]
            
            for field in required_fields:
                assert field in persona_data, \
                    f"Missing field '{field}' in persona '{persona_id}'"
    
    def test_quality_metrics_structure(self, statistics_data: Dict[str, Any]):
        """
        Verify that quality_metrics section has expected structure.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        quality_metrics = statistics_data.get("quality_metrics", {})
        
        expected_metrics = ["data_coverage", "unique_sources", 
                          "data_validation", "format_consistency"]
        
        for metric in expected_metrics:
            assert metric in quality_metrics, \
                f"Missing quality metric: {metric}"
    
    def test_overview_totals_exist(self, statistics_data: Dict[str, Any]):
        """
        Verify that overview section contains total counts.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        overview = statistics_data.get("overview", {})
        
        required_totals = ["total_personas", "total_documents", 
                          "total_chunks", "total_words"]
        
        for total_key in required_totals:
            assert total_key in overview, f"Missing overview total: {total_key}"
            assert isinstance(overview[total_key], int), \
                f"Overview total '{total_key}' must be an integer"


@pytest.mark.integrity
class TestFileAccessibility:
    """Test suite for file system accessibility."""
    
    def test_readme_exists(self, dataset_root: Path):
        """
        Verify that main README.md exists and is readable.
        
        Args:
            dataset_root: Path fixture to dataset root
        """
        readme_path = dataset_root / "README.md"
        assert readme_path.exists(), "Main README.md not found"
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content) > 1000, "README.md appears to be too short or empty"
    
    def test_license_exists(self, dataset_root: Path):
        """
        Verify that LICENSE file exists and is readable.
        
        Args:
            dataset_root: Path fixture to dataset root
        """
        license_path = dataset_root / "LICENSE"
        assert license_path.exists(), "LICENSE file not found"
        
        with open(license_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content) > 100, "LICENSE file appears to be empty"
    
    def test_project_summary_exists(self, dataset_root: Path):
        """
        Verify that PROJECT_SUMMARY.md exists and is readable.
        
        Args:
            dataset_root: Path fixture to dataset root
        """
        summary_path = dataset_root / "PROJECT_SUMMARY.md"
        assert summary_path.exists(), "PROJECT_SUMMARY.md not found"
        
        with open(summary_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content) > 500, "PROJECT_SUMMARY.md appears to be too short"
    
    def test_metadata_directory_accessible(self, metadata_path: Path):
        """
        Verify that metadata directory is accessible.
        
        Args:
            metadata_path: Path fixture to metadata directory
        """
        assert metadata_path.exists(), "Metadata directory not found"
        assert metadata_path.is_dir(), "Metadata path is not a directory"
        
        # Check that directory is not empty
        contents = list(metadata_path.iterdir())
        assert len(contents) > 0, "Metadata directory is empty"


@pytest.mark.integrity
@pytest.mark.slow
class TestBulkDataLoading:
    """Test suite for bulk data loading operations."""
    
    def test_all_json_files_parseable(self, dataset_root: Path):
        """
        Verify that all JSON files in dataset are parseable.
        
        This is a comprehensive test that may take longer to execute.
        
        Args:
            dataset_root: Path fixture to dataset root
        """
        json_files = list(dataset_root.rglob("*.json"))
        assert len(json_files) > 0, "No JSON files found in dataset"
        
        parsing_errors = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except Exception as e:
                parsing_errors.append({
                    "file": str(json_file.relative_to(dataset_root)),
                    "error": str(e)
                })
        
        assert len(parsing_errors) == 0, \
            f"Failed to parse {len(parsing_errors)} JSON files: {parsing_errors[:5]}"
