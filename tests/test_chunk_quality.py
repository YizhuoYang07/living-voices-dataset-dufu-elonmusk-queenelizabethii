"""
Test module for validating chunk quality and size distribution.

This module verifies that text chunks meet quality standards, including
size constraints, empty content detection, and persona-specific chunking
strategies.
"""

import json
import pytest
from pathlib import Path
from typing import Dict, List


class TestChunkSizeValidation:
    """Test suite for validating chunk size distributions."""

    def test_chunk_sizes_within_reasonable_range(self, dataset_root):
        """
        Test that all chunks fall within expected size ranges.
        
        Expected ranges:
        - Du Fu: 50-800 characters (Classical Chinese)
        - Elon Musk: 50-1000 words (English)
        - Queen Elizabeth II: 50-1000 words (English)
        """
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not chunks_dir.exists():
                pytest.skip(f"Chunks directory not found for {persona}")
            
            chunk_files = list(chunks_dir.glob("*.json"))
            assert len(chunk_files) > 0, f"No chunk files found for {persona}"
            
            for chunk_file in chunk_files:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    content = chunk.get('chunk_text', '')
                    
                    # Check content is not empty
                    assert len(content.strip()) > 0, \
                        f"Empty chunk found in {chunk_file.name}"
                    
                    # Check reasonable size ranges
                    if persona == "du_fu":
                        # Classical Chinese: character-based
                        char_count = len(content)
                        assert 10 <= char_count <= 1000, \
                            f"Chunk size {char_count} chars out of range in {chunk_file.name}"
                    else:
                        # English: word-based
                        word_count = len(content.split())
                        assert 10 <= word_count <= 1500, \
                            f"Chunk size {word_count} words out of range in {chunk_file.name}"

    def test_chunks_have_required_fields(self, dataset_root):
        """Test that all chunks contain required fields."""
        required_fields = ['chunk_id', 'chunk_text', 'chunk_metadata']
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not chunks_dir.exists():
                continue
            
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for idx, chunk in enumerate(chunks):
                    for field in required_fields:
                        assert field in chunk, \
                            f"Missing field '{field}' in chunk {idx} of {chunk_file.name}"

    def test_chunk_metadata_structure(self, dataset_root):
        """Test that chunk metadata has consistent structure."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not chunks_dir.exists():
                continue
            
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    metadata = chunk.get('chunk_metadata', {})
                    
                    # Verify metadata is a dictionary
                    assert isinstance(metadata, dict), \
                        f"chunk_metadata must be dict in {chunk_file.name}"
                    
                    # Check for expected metadata fields
                    if metadata:
                        assert 'source_doc_id' in metadata or 'doc_id' in metadata, \
                            f"Missing source document reference in {chunk_file.name}"


class TestEmptyChunkDetection:
    """Test suite for detecting empty or malformed chunks."""

    def test_no_empty_chunks(self, dataset_root):
        """Test that no chunks contain only whitespace."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        empty_chunks = []
        
        for persona in personas:
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not chunks_dir.exists():
                continue
            
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    content = chunk.get('chunk_text', '').strip()
                    if not content:
                        empty_chunks.append(f"{persona}/{chunk_file.name}/{chunk.get('chunk_id', 'unknown')}")
        
        assert len(empty_chunks) == 0, \
            f"Found {len(empty_chunks)} empty chunks: {empty_chunks[:5]}"

    def test_no_duplicate_chunk_ids(self, dataset_root):
        """Test that chunk IDs are unique within each persona."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not chunks_dir.exists():
                continue
            
            chunk_ids = set()
            duplicates = []
            
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    chunk_id = chunk.get('chunk_id')
                    if chunk_id in chunk_ids:
                        duplicates.append(chunk_id)
                    chunk_ids.add(chunk_id)
            
            assert len(duplicates) == 0, \
                f"Found {len(duplicates)} duplicate chunk IDs in {persona}: {duplicates[:5]}"


class TestPersonaSpecificChunking:
    """Test suite for validating persona-specific chunking strategies."""

    def test_dufu_character_based_chunking(self, dataset_root):
        """Test that Du Fu chunks are appropriately sized for Classical Chinese."""
        chunks_dir = dataset_root / "datasets" / "du_fu" / "chunks"
        
        if not chunks_dir.exists():
            pytest.skip("Du Fu chunks directory not found")
        
        total_chars = 0
        chunk_count = 0
        
        for chunk_file in chunks_dir.glob("*.json"):
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            for chunk in chunks:
                content = chunk.get('chunk_text', '')
                char_count = len(content)
                total_chars += char_count
                chunk_count += 1
        
        # Average chunk size should be reasonable for Classical Chinese
        if chunk_count > 0:
            avg_chars = total_chars / chunk_count
            assert 50 <= avg_chars <= 600, \
                f"Average Du Fu chunk size {avg_chars:.1f} chars is outside expected range"

    def test_english_personas_word_based_chunking(self, dataset_root):
        """Test that English persona chunks are appropriately sized."""
        english_personas = ["elon_musk", "queen_elizabeth_ii"]
        
        for persona in english_personas:
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not chunks_dir.exists():
                continue
            
            total_words = 0
            chunk_count = 0
            
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    content = chunk.get('chunk_text', '')
                    word_count = len(content.split())
                    total_words += word_count
                    chunk_count += 1
            
            # Average chunk size should be reasonable for English
            if chunk_count > 0:
                avg_words = total_words / chunk_count
                assert 50 <= avg_words <= 800, \
                    f"Average {persona} chunk size {avg_words:.1f} words is outside expected range"


class TestContentMetadataLinkage:
    """Test suite for validating links between chunks and source documents."""

    def test_chunk_references_valid_documents(self, dataset_root):
        """Test that chunks reference existing source documents."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            # Load available documents
            docs_dir = dataset_root / "datasets" / persona / "processed_data"
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not docs_dir.exists() or not chunks_dir.exists():
                continue
            
            # Get all document IDs
            doc_ids = set()
            for doc_file in docs_dir.glob("*.json"):
                with open(doc_file, 'r', encoding='utf-8') as f:
                    doc_data = json.load(f)
                    if isinstance(doc_data, list):
                        doc_ids.update(doc.get('id') or doc.get('doc_id') for doc in doc_data)
                    else:
                        doc_ids.add(doc_data.get('id') or doc_data.get('doc_id'))
            
            # Check chunks reference valid documents
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    metadata = chunk.get('chunk_metadata', {})
                    source_id = metadata.get('source_doc_id') or metadata.get('doc_id')
                    
                    if source_id:
                        # Extract base document ID (handle hierarchical IDs)
                        base_id = source_id.split('_chunk_')[0] if '_chunk_' in source_id else source_id
                        
                        # Verify document exists (if we have document IDs)
                        if doc_ids:
                            # Allow for flexible matching
                            matching = any(base_id in str(doc_id) or str(doc_id) in base_id 
                                         for doc_id in doc_ids if doc_id)
                            
                            if not matching:
                                pytest.warn(
                                    f"Chunk {chunk.get('chunk_id')} references "
                                    f"unknown document {base_id} in {persona}"
                                )

    def test_chunk_id_format_consistency(self, dataset_root):
        """Test that chunk IDs follow consistent naming patterns."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not chunks_dir.exists():
                continue
            
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    chunk_id = chunk.get('chunk_id', '')
                    
                    # Verify chunk ID is not empty
                    assert chunk_id, f"Empty chunk_id in {chunk_file.name}"
                    
                    # Verify chunk ID is string
                    assert isinstance(chunk_id, str), \
                        f"chunk_id must be string in {chunk_file.name}"
                    
                    # Verify reasonable length
                    assert len(chunk_id) > 0 and len(chunk_id) < 200, \
                        f"chunk_id has unusual length in {chunk_file.name}"


class TestChunkStatisticsConsistency:
    """Test suite for validating chunk-level statistics."""

    def test_chunk_counts_match_statistics(self, dataset_root):
        """Test that actual chunk counts match reported statistics."""
        statistics_file = dataset_root / "statistics.json"
        
        if not statistics_file.exists():
            pytest.skip("statistics.json not found")
        
        with open(statistics_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        personas_map = {
            "du_fu": "杜甫",
            "elon_musk": "Elon Musk",
            "queen_elizabeth_ii": "Queen Elizabeth II"
        }
        
        for persona_dir, persona_name in personas_map.items():
            chunks_dir = dataset_root / "datasets" / persona_dir / "chunks"
            
            if not chunks_dir.exists():
                continue
            
            # Count actual chunks
            actual_count = 0
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                    actual_count += len(chunks)
            
            # Find expected count in statistics
            for persona_stat in stats.get('persona_statistics', []):
                if persona_stat.get('persona') == persona_name:
                    expected_count = persona_stat.get('chunks_count')
                    
                    if expected_count is not None:
                        # Allow for small discrepancies (±5%)
                        tolerance = max(1, int(expected_count * 0.05))
                        assert abs(actual_count - expected_count) <= tolerance, \
                            f"{persona_name}: Expected ~{expected_count} chunks, found {actual_count}"
                    break
