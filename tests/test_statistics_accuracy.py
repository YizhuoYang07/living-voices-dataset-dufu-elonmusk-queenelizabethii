"""
Statistics Accuracy Verification Tests for Living Voices Dataset.

This module validates that reported statistics in statistics.json accurately
reflect the actual dataset contents.

Test Categories:
    - Document count verification
    - Chunk count verification
    - Content volume validation
    - Persona-specific metric accuracy
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any, List


@pytest.mark.statistics
class TestDocumentCounts:
    """Test suite for document count accuracy."""
    
    def test_du_fu_document_count(self, statistics_data: Dict[str, Any],
                                  expected_document_counts: Dict[str, int]):
        """
        Verify that Du Fu document count matches expected value.
        
        Args:
            statistics_data: Loaded statistics data fixture
            expected_document_counts: Expected counts fixture
        """
        actual_count = statistics_data["personas"]["du_fu"]["documents"]["total"]
        expected_count = expected_document_counts["du_fu"]
        
        assert actual_count == expected_count, \
            f"Du Fu document count mismatch: " \
            f"expected {expected_count}, got {actual_count}"
    
    def test_elon_musk_document_count(self, statistics_data: Dict[str, Any],
                                     expected_document_counts: Dict[str, int]):
        """
        Verify that Elon Musk document count matches expected value.
        
        Args:
            statistics_data: Loaded statistics data fixture
            expected_document_counts: Expected counts fixture
        """
        actual_count = statistics_data["personas"]["elon_musk"]["documents"]["total"]
        expected_count = expected_document_counts["elon_musk"]
        
        assert actual_count == expected_count, \
            f"Elon Musk document count mismatch: " \
            f"expected {expected_count}, got {actual_count}"
    
    def test_queen_elizabeth_document_count(self, statistics_data: Dict[str, Any],
                                           expected_document_counts: Dict[str, int]):
        """
        Verify that Queen Elizabeth II document count matches expected value.
        
        Args:
            statistics_data: Loaded statistics data fixture
            expected_document_counts: Expected counts fixture
        """
        actual_count = statistics_data["personas"]["queen_elizabeth_ii"]["documents"]["total"]
        expected_count = expected_document_counts["queen_elizabeth_ii"]
        
        assert actual_count == expected_count, \
            f"Queen Elizabeth II document count mismatch: " \
            f"expected {expected_count}, got {actual_count}"
    
    def test_total_document_count(self, statistics_data: Dict[str, Any]):
        """
        Verify that total document count equals sum of persona counts.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        overview_total = statistics_data["overview"]["total_documents"]
        personas = statistics_data["personas"]
        
        calculated_total = sum(
            p["documents"]["total"] for p in personas.values()
        )
        
        assert overview_total == calculated_total, \
            f"Total document count mismatch: " \
            f"overview shows {overview_total}, " \
            f"persona sum is {calculated_total}"


@pytest.mark.statistics
class TestChunkCounts:
    """Test suite for chunk count accuracy."""
    
    def test_du_fu_chunk_count(self, statistics_data: Dict[str, Any],
                              expected_chunk_counts: Dict[str, int]):
        """
        Verify that Du Fu chunk count matches expected value.
        
        Args:
            statistics_data: Loaded statistics data fixture
            expected_chunk_counts: Expected counts fixture
        """
        actual_count = statistics_data["personas"]["du_fu"]["chunks"]["total"]
        expected_count = expected_chunk_counts["du_fu"]
        
        assert actual_count == expected_count, \
            f"Du Fu chunk count mismatch: " \
            f"expected {expected_count}, got {actual_count}"
    
    def test_elon_musk_chunk_count(self, statistics_data: Dict[str, Any],
                                  expected_chunk_counts: Dict[str, int]):
        """
        Verify that Elon Musk chunk count matches expected value.
        
        Args:
            statistics_data: Loaded statistics data fixture
            expected_chunk_counts: Expected counts fixture
        """
        actual_count = statistics_data["personas"]["elon_musk"]["chunks"]["total"]
        expected_count = expected_chunk_counts["elon_musk"]
        
        assert actual_count == expected_count, \
            f"Elon Musk chunk count mismatch: " \
            f"expected {expected_count}, got {actual_count}"
    
    def test_queen_elizabeth_chunk_count(self, statistics_data: Dict[str, Any],
                                        expected_chunk_counts: Dict[str, int]):
        """
        Verify that Queen Elizabeth II chunk count matches expected value.
        
        Args:
            statistics_data: Loaded statistics data fixture
            expected_chunk_counts: Expected counts fixture
        """
        actual_count = statistics_data["personas"]["queen_elizabeth_ii"]["chunks"]["total"]
        expected_count = expected_chunk_counts["queen_elizabeth_ii"]
        
        assert actual_count == expected_count, \
            f"Queen Elizabeth II chunk count mismatch: " \
            f"expected {expected_count}, got {actual_count}"
    
    def test_total_chunk_count(self, statistics_data: Dict[str, Any]):
        """
        Verify that total chunk count equals sum of persona counts.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        overview_total = statistics_data["overview"]["total_chunks"]
        personas = statistics_data["personas"]
        
        calculated_total = sum(
            p["chunks"]["total"] for p in personas.values()
        )
        
        assert overview_total == calculated_total, \
            f"Total chunk count mismatch: " \
            f"overview shows {overview_total}, " \
            f"persona sum is {calculated_total}"


@pytest.mark.statistics
class TestContentVolume:
    """Test suite for content volume metrics."""
    
    def test_content_volume_positive(self, statistics_data: Dict[str, Any],
                                    persona_identifiers: List[str]):
        """
        Verify that all personas have positive content volume.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data["personas"]
        
        for persona_id in persona_identifiers:
            total_words = personas[persona_id]["content"]["total_words"]
            
            assert total_words > 0, \
                f"Persona '{persona_id}' has zero or negative content volume"
            assert isinstance(total_words, int), \
                f"Content volume for '{persona_id}' must be integer"
    
    def test_average_chunk_size_reasonable(self, statistics_data: Dict[str, Any],
                                          persona_identifiers: List[str]):
        """
        Verify that average chunk sizes are within reasonable ranges.
        
        Args:
            statistics_data: Loaded statistics data fixture
            persona_identifiers: List of expected persona IDs
        """
        personas = statistics_data["personas"]
        
        for persona_id in persona_identifiers:
            avg_size = personas[persona_id]["content"]["average_words_per_chunk"]
            
            # Average chunk size should be positive
            assert avg_size > 0, \
                f"Persona '{persona_id}' has non-positive average chunk size"
            
            # Should be reasonable (between 1 and 10000 words/chars)
            assert 1 <= avg_size <= 10000, \
                f"Persona '{persona_id}' has unreasonable average chunk size: {avg_size}"


@pytest.mark.statistics
class TestPersonaSpecificMetrics:
    """Test suite for persona-specific metric validation."""
    
    def test_du_fu_metrics_match_classical_chinese(self, statistics_data: Dict[str, Any]):
        """
        Verify that Du Fu metrics reflect Classical Chinese characteristics.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        du_fu = statistics_data["personas"]["du_fu"]
        
        # Should have high document count (all poems)
        assert du_fu["documents"]["total"] > 1000, \
            "Du Fu should have over 1000 poems"
        
        # Should have character-based content measurement
        note = du_fu["content"].get("note", "")
        assert "character" in note.lower() or "Character" in note, \
            "Du Fu content should note character-based counting"
    
    def test_modern_personas_word_based(self, statistics_data: Dict[str, Any]):
        """
        Verify that modern personas use word-based counting.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        modern_personas = ["elon_musk", "queen_elizabeth_ii"]
        personas = statistics_data["personas"]
        
        for persona_id in modern_personas:
            content = personas[persona_id]["content"]
            
            # Should have "total_words" field
            assert "total_words" in content, \
                f"Persona '{persona_id}' missing total_words field"
            
            # Average should be reasonable for English text
            avg = content["average_words_per_chunk"]
            # English chunks typically range from 10 to 5000 words
            assert 10 <= avg <= 5000, \
                f"Persona '{persona_id}' has unusual word count average: {avg}"


@pytest.mark.statistics
class TestDistributionMetrics:
    """Test suite for distribution metrics validation."""
    
    def test_language_distribution_exists(self, statistics_data: Dict[str, Any]):
        """
        Verify that language distribution is documented.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        distribution = statistics_data.get("distribution", {})
        
        assert "by_language" in distribution, \
            "Distribution should include by_language breakdown"
        
        by_language = distribution["by_language"]
        assert "Classical Chinese" in by_language, \
            "Distribution should include Classical Chinese"
        assert "English" in by_language, \
            "Distribution should include English"
    
    def test_era_distribution_exists(self, statistics_data: Dict[str, Any]):
        """
        Verify that temporal era distribution is documented.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        distribution = statistics_data.get("distribution", {})
        
        assert "by_era" in distribution, \
            "Distribution should include by_era breakdown"
        
        by_era = distribution["by_era"]
        # Should have at least two eras
        assert len(by_era) >= 2, \
            "Distribution should include multiple eras"
    
    def test_distribution_percentages_valid(self, statistics_data: Dict[str, Any]):
        """
        Verify that distribution percentages are valid.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        distribution = statistics_data.get("distribution", {})
        by_language = distribution.get("by_language", {})
        
        for language, data in by_language.items():
            if "percentage" in data:
                percentage = data["percentage"]
                
                assert 0 <= percentage <= 100, \
                    f"Language '{language}' has invalid percentage: {percentage}"


@pytest.mark.statistics
class TestQualityMetricsValidation:
    """Test suite for quality metrics validation."""
    
    def test_data_coverage_complete(self, statistics_data: Dict[str, Any]):
        """
        Verify that data coverage is reported as complete.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        quality_metrics = statistics_data["quality_metrics"]
        coverage = quality_metrics["data_coverage"]
        
        assert coverage == "100%", \
            f"Expected 100% data coverage, got: {coverage}"
    
    def test_validation_passed(self, statistics_data: Dict[str, Any]):
        """
        Verify that data validation status is passed.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        quality_metrics = statistics_data["quality_metrics"]
        validation = quality_metrics["data_validation"]
        
        assert validation == "passed", \
            f"Expected validation to pass, got: {validation}"
    
    def test_unique_sources_match_documents(self, statistics_data: Dict[str, Any]):
        """
        Verify that unique sources count matches total documents.
        
        Args:
            statistics_data: Loaded statistics data fixture
        """
        quality_metrics = statistics_data["quality_metrics"]
        overview = statistics_data["overview"]
        
        unique_sources = quality_metrics["unique_sources"]
        total_documents = overview["total_documents"]
        
        assert unique_sources == total_documents, \
            f"Unique sources ({unique_sources}) should match " \
            f"total documents ({total_documents})"
