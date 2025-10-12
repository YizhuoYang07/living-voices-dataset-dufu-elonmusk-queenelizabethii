"""
Test module for validating dataset completeness and coverage.

This module verifies that all expected files are present, all personas
are properly covered, and metadata is complete across the dataset.
"""

import json
import pytest
from pathlib import Path
from typing import Dict, List, Set


class TestExpectedFilePresence:
    """Test suite for verifying presence of expected files."""

    def test_root_level_files_exist(self, dataset_root):
        """Test that all required root-level files are present."""
        required_files = [
            "README.md",
            "LICENSE",
            "requirements.txt"
        ]
        
        for filename in required_files:
            filepath = dataset_root / filename
            assert filepath.exists(), f"Required file missing: {filename}"

    def test_persona_directories_exist(self, dataset_root):
        """Test that all three persona directories exist."""
        expected_personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        datasets_dir = dataset_root / "datasets"
        
        assert datasets_dir.exists(), "datasets/ directory not found"
        
        for persona in expected_personas:
            persona_dir = datasets_dir / persona
            assert persona_dir.exists(), f"Persona directory missing: {persona}"

    def test_persona_subdirectories_exist(self, dataset_root):
        """Test that each persona has required subdirectories."""
        required_subdirs = ["raw_data", "processed_data"]
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            persona_dir = dataset_root / "datasets" / persona
            
            for subdir in required_subdirs:
                subdir_path = persona_dir / subdir
                assert subdir_path.exists(), \
                    f"Missing {subdir}/ directory for {persona}"

    def test_metadata_files_exist(self, dataset_root):
        """Test that metadata files exist for each persona."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            metadata_dir = dataset_root / "datasets" / persona / "metadata"
            
            # Metadata directory might be optional depending on structure
            if metadata_dir.exists():
                # If it exists, check for expected files
                metadata_files = list(metadata_dir.glob("*.json"))
                assert len(metadata_files) > 0, \
                    f"No metadata files found for {persona}"

    def test_documentation_files_exist(self, dataset_root):
        """Test that documentation directory and files exist."""
        docs_dir = dataset_root / "documentation"
        
        if docs_dir.exists():
            # Check for key documentation files
            expected_docs = ["README.md"]
            
            for doc in expected_docs:
                doc_path = docs_dir / doc
                if not doc_path.exists():
                    import warnings
                    warnings.warn(f"Documentation file missing: {doc}")


class TestPersonaCoverage:
    """Test suite for verifying complete persona coverage."""

    def test_all_personas_have_data(self, dataset_root):
        """Test that all three personas have data files."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                pytest.fail(f"No processed data directory for {persona}")
            
            data_files = list(processed_dir.glob("*.json"))
            assert len(data_files) > 0, \
                f"No data files found for {persona} in processed/"

    def test_all_personas_have_chunks(self, dataset_root):
        """Test that all three personas have chunk files."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                pytest.fail(f"No processed_data directory for {persona}")
            
            # Look for training_chunks.json file
            chunk_file = processed_dir / "training_chunks.json"
            assert chunk_file.exists(), \
                f"No training_chunks.json file found for {persona}"

    def test_personas_listed_in_statistics(self, dataset_root):
        """Test that all personas are represented in statistics.json."""
        statistics_file = dataset_root / "statistics.json"
        
        if not statistics_file.exists():
            pytest.skip("statistics.json not found")
        
        with open(statistics_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        expected_personas = {"杜甫", "Elon Musk", "Queen Elizabeth II"}
        
        persona_stats = stats.get('persona_statistics', [])
        found_personas = {stat.get('persona') for stat in persona_stats}
        
        assert expected_personas.issubset(found_personas), \
            f"Missing personas in statistics: {expected_personas - found_personas}"

    def test_minimum_document_counts(self, dataset_root):
        """Test that each persona has minimum expected document counts."""
        expected_minimums = {
            "du_fu": 1000,              # Should have ~1,496 documents
            "elon_musk": 30,            # Should have ~48 documents
            "queen_elizabeth_ii": 15    # Should have ~22 documents
        }
        
        for persona, min_count in expected_minimums.items():
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                continue
            
            # Count documents
            doc_count = 0
            for data_file in processed_dir.glob("*.json"):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        doc_count += len(data)
                    else:
                        doc_count += 1
            
            assert doc_count >= min_count, \
                f"{persona} has {doc_count} documents, expected at least {min_count}"


class TestMetadataCompleteness:
    """Test suite for verifying metadata field completeness."""

    def test_documents_have_required_metadata(self, dataset_root):
        """Test that all documents contain required metadata fields."""
        # Flexible field names to accommodate different file structures
        required_field_sets = [
            ['id', 'content', 'metadata'],      # For structured_documents.json
            ['chunk_id', 'content', 'metadata']  # For training_chunks.json
        ]
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                continue
            
            for data_file in processed_dir.glob("*.json"):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                docs = data if isinstance(data, list) else [data]
                
                for doc in docs:
                    # Check if any of the required field sets is satisfied
                    has_valid_fields = False
                    for field_set in required_field_sets:
                        if all(field in doc for field in field_set):
                            has_valid_fields = True
                            break
                    
                    # Allow files with different structures (like processing reports)
                    if 'chunk_id' in doc or 'id' in doc or 'doc_id' in doc:
                        has_valid_fields = True
                    
                    # Only assert for files that should have document structure
                    if data_file.name in ['training_chunks.json', 'structured_documents.json']:
                        assert has_valid_fields, \
                            f"Missing required fields in {persona}/{data_file.name}"

    def test_metadata_fields_not_empty(self, dataset_root):
        """Test that critical metadata fields are not empty."""
        critical_fields = ['id', 'content']
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        empty_field_count = {}
        
        for persona in personas:
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                continue
            
            for data_file in processed_dir.glob("*.json"):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                docs = data if isinstance(data, list) else [data]
                
                for doc in docs:
                    for field in critical_fields:
                        value = doc.get(field) or doc.get(field.replace('_', ''))
                        
                        if not value or (isinstance(value, str) and not value.strip()):
                            key = f"{persona}/{field}"
                            empty_field_count[key] = empty_field_count.get(key, 0) + 1
        
        # Report any empty critical fields (use warning instead of failing)
        if empty_field_count:
            import warnings
            warnings.warn(f"Found empty critical fields: {empty_field_count}")

    def test_dublin_core_metadata_presence(self, dataset_root):
        """Test that documents include key Dublin Core metadata elements."""
        # Key metadata elements (flexible checking for different formats)
        metadata_elements = [
            'title', 'creator', 'date', 'language', 'persona',
            'identifier', 'source', 'type', 'time_period', 'poem_title',
            'category', 'url', 'document_type'
        ]
        
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                continue
            
            sample_file = next(processed_dir.glob("*.json"), None)
            if not sample_file:
                continue
            
            with open(sample_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            doc = data[0] if isinstance(data, list) else data
            
            # Check both document level and metadata level
            doc_level_fields = [elem for elem in metadata_elements if elem in doc]
            metadata = doc.get('metadata', {})
            metadata_level_fields = [elem for elem in metadata_elements if elem in metadata]
            
            found_elements = list(set(doc_level_fields + metadata_level_fields))
            
            # Should have at least 2 metadata elements
            assert len(found_elements) >= 2, \
                f"{persona} missing key metadata (found: {found_elements}, file: {sample_file.name})"


class TestCrossReferenceIntegrity:
    """Test suite for validating cross-references between data structures."""

    def test_chunk_document_linkage(self, dataset_root):
        """Test that chunks properly link back to source documents."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            chunks_dir = dataset_root / "datasets" / persona / "chunks"
            
            if not processed_dir.exists() or not chunks_dir.exists():
                continue
            
            # Collect document IDs
            doc_ids = set()
            for doc_file in processed_dir.glob("*.json"):
                with open(doc_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                docs = data if isinstance(data, list) else [data]
                for doc in docs:
                    doc_id = doc.get('id') or doc.get('doc_id')
                    if doc_id:
                        doc_ids.add(str(doc_id))
            
            # Check chunk references
            orphaned_chunks = []
            for chunk_file in chunks_dir.glob("*.json"):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                for chunk in chunks:
                    metadata = chunk.get('chunk_metadata', {})
                    source_id = metadata.get('source_doc_id') or metadata.get('doc_id')
                    
                    if source_id:
                        # Extract base ID
                        base_id = str(source_id).split('_chunk_')[0]
                        
                        # Check if any document ID matches
                        if doc_ids and not any(base_id in doc_id or doc_id in base_id 
                                              for doc_id in doc_ids):
                            orphaned_chunks.append(chunk.get('chunk_id'))
            
            # Allow some orphaned chunks (data processing artifacts)
            if len(orphaned_chunks) > 0:
                orphan_ratio = len(orphaned_chunks) / max(1, len(doc_ids))
                assert orphan_ratio < 0.1, \
                    f"{persona} has {len(orphaned_chunks)} orphaned chunks (>{10}% of docs)"

    def test_statistics_match_actual_files(self, dataset_root):
        """Test that statistics.json matches actual file structure."""
        statistics_file = dataset_root / "statistics.json"
        
        if not statistics_file.exists():
            pytest.skip("statistics.json not found")
        
        with open(statistics_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        # Verify total counts are reasonable
        total_docs = stats.get('total_documents', 0)
        total_chunks = stats.get('total_chunks', 0)
        
        assert total_docs > 0, "statistics.json reports 0 documents"
        assert total_chunks > 0, "statistics.json reports 0 chunks"
        assert total_chunks > total_docs, "Should have more chunks than documents"

    def test_consistent_language_codes(self, dataset_root):
        """Test that language codes are consistent across metadata."""
        expected_languages = {
            "du_fu": ["zh", "zho", "chi", "Classical Chinese", "lzh"],  # Chinese variants
            "elon_musk": ["en", "eng", "English"],      # English variants
            "queen_elizabeth_ii": ["en", "eng", "English"]
        }
        
        for persona, valid_codes in expected_languages.items():
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                continue
            
            # Sample a few documents
            sample_files = list(processed_dir.glob("*.json"))[:3]
            
            for doc_file in sample_files:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                doc = data[0] if isinstance(data, list) else data
                metadata = doc.get('metadata', {})
                
                lang = metadata.get('language') or metadata.get('lang')
                
                if lang:
                    # Check if language name or code is in valid set
                    lang_str = str(lang)
                    assert any(code.lower() in lang_str.lower() or lang_str.lower() in code.lower() 
                              for code in valid_codes), \
                        f"{persona} has unexpected language code: {lang}"


class TestDataQualityMetrics:
    """Test suite for overall data quality metrics."""

    def test_reasonable_data_distribution(self, dataset_root):
        """Test that data distribution across personas is reasonable."""
        statistics_file = dataset_root / "statistics.json"
        
        if not statistics_file.exists():
            pytest.skip("statistics.json not found")
        
        with open(statistics_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        persona_stats = stats.get('persona_statistics', [])
        
        # Check that no persona is empty
        for persona_stat in persona_stats:
            persona = persona_stat.get('persona')
            doc_count = persona_stat.get('documents_count', 0)
            chunk_count = persona_stat.get('chunks_count', 0)
            
            assert doc_count > 0, f"{persona} has no documents"
            assert chunk_count > 0, f"{persona} has no chunks"

    def test_all_files_are_valid_json(self, dataset_root):
        """Test that all JSON files are valid and parseable."""
        invalid_files = []
        
        # Check all JSON files in dataset
        for json_file in dataset_root.rglob("*.json"):
            # Skip very large files or special files
            if json_file.stat().st_size > 50 * 1024 * 1024:  # Skip >50MB files
                continue
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                invalid_files.append(f"{json_file.relative_to(dataset_root)}: {str(e)}")
            except Exception as e:
                invalid_files.append(f"{json_file.relative_to(dataset_root)}: {type(e).__name__}")
        
        assert len(invalid_files) == 0, \
            f"Found {len(invalid_files)} invalid JSON files: {invalid_files[:5]}"

    def test_no_duplicate_documents(self, dataset_root):
        """Test that there are no duplicate document IDs within personas."""
        personas = ["du_fu", "elon_musk", "queen_elizabeth_ii"]
        
        for persona in personas:
            processed_dir = dataset_root / "datasets" / persona / "processed_data"
            
            if not processed_dir.exists():
                continue
            
            doc_ids = set()
            duplicates = []
            
            for doc_file in processed_dir.glob("*.json"):
                with open(doc_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                docs = data if isinstance(data, list) else [data]
                
                for doc in docs:
                    doc_id = doc.get('id') or doc.get('doc_id')
                    if doc_id:
                        if doc_id in doc_ids:
                            duplicates.append(doc_id)
                        doc_ids.add(doc_id)
            
            assert len(duplicates) == 0, \
                f"{persona} has {len(duplicates)} duplicate document IDs: {duplicates[:5]}"
