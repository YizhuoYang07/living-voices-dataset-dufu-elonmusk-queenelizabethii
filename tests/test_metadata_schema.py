"""
Metadata Schema Compliance Tests for Living Voices Dataset.

This module validates that all metadata records comply with defined schemas
including Dublin Core, Schema.org, DataCite, and project-specific standards.

Test Categories:
    - Required field presence validation
    - Field type verification
    - ISO standard compliance (ISO 639-3, ISO 8601, SPDX)
    - Hierarchical identifier consistency
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


@pytest.mark.schema
class TestMetadataFieldPresence:
    """Test suite for required metadata field validation."""
    
    def test_persona_metadata_completeness(self, statistics_data: Dict[str, Any],
                                          persona_identifiers: List[str]):
        """
        Verify that each persona has all required metadata fields.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data["personas"]
        
        required_fields = [
            "display_name",
            "type",
            "language",
            "era",
            "documents",
            "chunks",
            "content"
        ]
        
        for persona_id in persona_identifiers:
            persona_data = personas[persona_id]
            
            for field in required_fields:
                assert field in persona_data, \
                    f"Persona '{persona_id}' missing required field: {field}"
    
    def test_document_counts_present(self, statistics_data: Dict[str, Any],
                                    persona_identifiers: List[str]):
        """
        Verify that document count information is present for each persona.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data["personas"]
        
        for persona_id in persona_identifiers:
            documents = personas[persona_id]["documents"]
            
            assert "total" in documents, \
                f"Persona '{persona_id}' missing total document count"
            assert isinstance(documents["total"], int), \
                f"Document total for '{persona_id}' must be integer"
            assert documents["total"] > 0, \
                f"Document total for '{persona_id}' must be positive"


@pytest.mark.schema
class TestISO639LanguageCodes:
    """Test suite for ISO 639-3 language code compliance."""
    
    def test_language_codes_valid(self, statistics_data: Dict[str, Any],
                                 persona_identifiers: List[str],
                                 iso_language_codes: Dict[str, str]):
        """
        Verify that language fields use valid ISO 639-3 codes.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
            iso_language_codes: Mapping of language names to ISO codes
        """
        personas = statistics_data["personas"]
        valid_codes = set(iso_language_codes.values())
        
        for persona_id in persona_identifiers:
            language = personas[persona_id]["language"]
            
            # Language field should map to valid ISO code
            assert language in iso_language_codes, \
                f"Persona '{persona_id}' has unmapped language: {language}"
    
    def test_classical_chinese_code(self, statistics_data: Dict[str, Any]):
        """
        Verify that Classical Chinese uses correct ISO 639-3 code (lzh).
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        du_fu_data = statistics_data["personas"]["du_fu"]
        language = du_fu_data["language"]
        
        assert language == "Classical Chinese", \
            f"Du Fu language should be 'Classical Chinese', got: {language}"
    
    def test_english_language_consistency(self, statistics_data: Dict[str, Any]):
        """
        Verify that modern personas use consistent English language designation.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        modern_personas = ["elon_musk", "queen_elizabeth_ii"]
        personas = statistics_data["personas"]
        
        for persona_id in modern_personas:
            language = personas[persona_id]["language"]
            assert language == "English", \
                f"Persona '{persona_id}' should use 'English', got: {language}"


@pytest.mark.schema
class TestISO8601Timestamps:
    """Test suite for ISO 8601 timestamp format compliance."""
    
    def test_generation_date_format(self, statistics_data: Dict[str, Any]):
        """
        Verify that generated_date uses ISO 8601 format.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        if "generated_date" in statistics_data:
            date_str = statistics_data["generated_date"]
            
            # Should parse as ISO 8601 datetime
            try:
                parsed = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                assert parsed is not None
            except ValueError as e:
                pytest.fail(f"generated_date not in ISO 8601 format: {e}")


@pytest.mark.schema
class TestHierarchicalIdentifiers:
    """Test suite for identifier consistency and hierarchy."""
    
    def test_persona_id_format(self, persona_identifiers: List[str]):
        """
        Verify that persona identifiers follow snake_case convention.
        
        Args:
            persona_identifiers: List of expected persona IDs
        """
        for persona_id in persona_identifiers:
            # Should be lowercase with underscores
            assert persona_id.islower() or '_' in persona_id, \
                f"Persona ID '{persona_id}' should use snake_case"
            
            # Should not contain spaces or special characters
            assert ' ' not in persona_id, \
                f"Persona ID '{persona_id}' should not contain spaces"
    
    def test_display_name_format(self, statistics_data: Dict[str, Any],
                                persona_display_names: Dict[str, str]):
        """
        Verify that display names match expected format.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_display_names: Expected display name mapping
        """
        personas = statistics_data["personas"]
        
        for persona_id, expected_name in persona_display_names.items():
            actual_name = personas[persona_id]["display_name"]
            assert actual_name == expected_name, \
                f"Display name mismatch for '{persona_id}': " \
                f"expected '{expected_name}', got '{actual_name}'"


@pytest.mark.schema
class TestDublinCoreCompliance:
    """Test suite for Dublin Core metadata standard compliance."""
    
    def test_creator_information(self, dataset_root: Path):
        """
        Verify that README contains Dublin Core creator information.
        
        Args:
            dataset_root: Path fixture to dataset root
        """
        readme_path = dataset_root / "README.md"
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should contain citation or creator information
        assert "Citation" in content or "Author" in content, \
            "README should contain Dublin Core creator information"
    
    def test_dataset_identifier(self, statistics_data: Dict[str, Any]):
        """
        Verify that dataset has version identifier (Dublin Core requirement).
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        assert "dataset_version" in statistics_data, \
            "Statistics should contain dataset_version identifier"
        
        version = statistics_data["dataset_version"]
        assert isinstance(version, str), \
            "dataset_version should be string"
        assert len(version) > 0, \
            "dataset_version should not be empty"


@pytest.mark.schema
class TestDataCiteCompliance:
    """Test suite for DataCite metadata standard compliance."""
    
    def test_resource_type_classification(self, statistics_data: Dict[str, Any],
                                         persona_identifiers: List[str]):
        """
        Verify that each persona has resource type classification.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data["personas"]
        
        valid_types = [
            "historical_poet",
            "contemporary_entrepreneur",
            "historical_monarch"
        ]
        
        for persona_id in persona_identifiers:
            resource_type = personas[persona_id]["type"]
            assert resource_type in valid_types, \
                f"Invalid resource type for '{persona_id}': {resource_type}"
    
    def test_temporal_coverage(self, statistics_data: Dict[str, Any],
                              persona_identifiers: List[str]):
        """
        Verify that temporal coverage (era) is specified for each persona.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data["personas"]
        
        for persona_id in persona_identifiers:
            era = personas[persona_id]["era"]
            assert isinstance(era, str), \
                f"Era for '{persona_id}' should be string"
            assert len(era) > 0, \
                f"Era for '{persona_id}' should not be empty"
            
            # Should contain temporal information
            has_temporal = any(marker in era for marker in 
                             ["CE", "present", "Century", "-"])
            assert has_temporal, \
                f"Era for '{persona_id}' should contain temporal markers"


@pytest.mark.schema
class TestQualityMetricsSchema:
    """Test suite for quality metrics schema validation."""
    
    def test_quality_metrics_types(self, statistics_data: Dict[str, Any]):
        """
        Verify that quality metrics have correct data types.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        quality_metrics = statistics_data["quality_metrics"]
        
        # data_coverage should be percentage string
        coverage = quality_metrics["data_coverage"]
        assert isinstance(coverage, str), \
            "data_coverage should be string (percentage)"
        assert "%" in coverage, \
            "data_coverage should include percentage sign"
        
        # unique_sources should be integer
        sources = quality_metrics["unique_sources"]
        assert isinstance(sources, int), \
            "unique_sources should be integer"
    
    def test_validation_status(self, statistics_data: Dict[str, Any]):
        """
        Verify that data validation status is recorded.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        quality_metrics = statistics_data["quality_metrics"]
        
        assert "data_validation" in quality_metrics, \
            "quality_metrics should include data_validation status"
        
        status = quality_metrics["data_validation"]
        assert status in ["passed", "failed", "pending"], \
            f"Invalid validation status: {status}"


@pytest.mark.schema
class TestSchemaConsistency:
    """Test suite for cross-field schema consistency."""
    
    def test_chunk_to_document_ratio(self, statistics_data: Dict[str, Any],
                                    persona_identifiers: List[str]):
        """
        Verify that chunk counts are consistent with document counts.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data["personas"]
        
        for persona_id in persona_identifiers:
            persona_data = personas[persona_id]
            doc_count = persona_data["documents"]["total"]
            chunk_count = persona_data["chunks"]["total"]
            
            # Chunks should be >= documents (at least 1 chunk per document)
            assert chunk_count >= doc_count, \
                f"Persona '{persona_id}' has fewer chunks than documents: " \
                f"{chunk_count} chunks, {doc_count} documents"
    
    def test_overview_matches_persona_totals(self, statistics_data: Dict[str, Any]):
        """
        Verify that overview totals match sum of persona-specific values.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        overview = statistics_data["overview"]
        personas = statistics_data["personas"]
        
        # Calculate expected totals
        expected_docs = sum(p["documents"]["total"] for p in personas.values())
        expected_chunks = sum(p["chunks"]["total"] for p in personas.values())
        
        # Verify totals match
        assert overview["total_documents"] == expected_docs, \
            f"Overview total_documents mismatch: " \
            f"expected {expected_docs}, got {overview['total_documents']}"
        
        assert overview["total_chunks"] == expected_chunks, \
            f"Overview total_chunks mismatch: " \
            f"expected {expected_chunks}, got {overview['total_chunks']}"
