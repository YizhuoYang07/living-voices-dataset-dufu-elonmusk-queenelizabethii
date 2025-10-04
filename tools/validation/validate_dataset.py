#!/usr/bin/env python3
"""
Dataset validation script for Living Voices project.
Validates processed datasets and generates validation reports.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import json
import os
import sys
from datetime import datetime
from collections import Counter


class DatasetValidator:
    """
    Validates processed dataset for RAG training.
    """
    
    def __init__(self, dataset_name, processed_dir):
        """
        Initialize validator.
        
        Args:
            dataset_name: Name of the dataset (e.g., "Elon Musk")
            processed_dir: Directory containing processed data
        """
        self.dataset_name = dataset_name
        self.processed_dir = processed_dir
        
        self.issues = []
        self.warnings = []
        self.stats = {}
        
    def validate(self):
        """
        Main validation method.
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        print("=" * 80)
        print(f"{self.dataset_name} Dataset - Validation")
        print("=" * 80)
        print(f"Directory: {self.processed_dir}")
        print()
        
        # Check required files
        print("Step 1: Checking required files...")
        if not self._check_required_files():
            return False
        
        # Validate structured documents
        print("\nStep 2: Validating structured documents...")
        if not self._validate_documents():
            return False
        
        # Validate training chunks
        print("\nStep 3: Validating training chunks...")
        if not self._validate_chunks():
            return False
        
        # Cross-validate
        print("\nStep 4: Cross-validating data...")
        self._cross_validate()
        
        # Generate statistics
        print("\nStep 5: Generating statistics...")
        self._generate_statistics()
        
        # Save validation report
        print("\nStep 6: Saving validation report...")
        self._save_report()
        
        # Print summary
        self._print_summary()
        
        return len(self.issues) == 0
    
    def _check_required_files(self):
        """Check if required files exist."""
        required_files = [
            'structured_documents.json',
            'training_chunks.json',
            'dataset_metadata.json'
        ]
        
        all_exist = True
        for filename in required_files:
            filepath = os.path.join(self.processed_dir, filename)
            if os.path.exists(filepath):
                print(f"  ✓ Found: {filename}")
            else:
                print(f"  ✗ Missing: {filename}")
                self.issues.append(f"Required file missing: {filename}")
                all_exist = False
        
        return all_exist
    
    def _validate_documents(self):
        """Validate structured documents."""
        filepath = os.path.join(self.processed_dir, 'structured_documents.json')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
        except Exception as e:
            self.issues.append(f"Failed to load structured_documents.json: {e}")
            return False
        
        if not isinstance(self.documents, list):
            self.issues.append("structured_documents.json must contain a list")
            return False
        
        if len(self.documents) == 0:
            self.issues.append("structured_documents.json is empty")
            return False
        
        print(f"  ✓ Loaded {len(self.documents)} documents")
        
        # Validate each document
        required_fields = ['id', 'title', 'type', 'content']
        doc_ids = set()
        
        for i, doc in enumerate(self.documents):
            # Check required fields
            for field in required_fields:
                if field not in doc:
                    self.issues.append(f"Document {i} missing field: {field}")
            
            # Check unique IDs
            doc_id = doc.get('id')
            if doc_id:
                if doc_id in doc_ids:
                    self.issues.append(f"Duplicate document ID: {doc_id}")
                doc_ids.add(doc_id)
            
            # Check content
            if not doc.get('content'):
                self.warnings.append(f"Document {doc_id} has empty content")
        
        print(f"  ✓ Validated {len(self.documents)} documents")
        if self.warnings:
            print(f"  ⚠️  {len(self.warnings)} warnings")
        
        return len(self.issues) == 0
    
    def _validate_chunks(self):
        """Validate training chunks."""
        filepath = os.path.join(self.processed_dir, 'training_chunks.json')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
        except Exception as e:
            self.issues.append(f"Failed to load training_chunks.json: {e}")
            return False
        
        if not isinstance(self.chunks, list):
            self.issues.append("training_chunks.json must contain a list")
            return False
        
        if len(self.chunks) == 0:
            self.issues.append("training_chunks.json is empty")
            return False
        
        print(f"  ✓ Loaded {len(self.chunks)} chunks")
        
        # Validate each chunk - support both 'id' and 'chunk_id', 'source_document_id' and 'document_id'
        chunk_ids = set()
        
        for i, chunk in enumerate(self.chunks):
            # Check ID field (either 'id' or 'chunk_id')
            chunk_id = chunk.get('id') or chunk.get('chunk_id')
            if not chunk_id:
                self.issues.append(f"Chunk {i} missing ID field (id or chunk_id)")
            else:
                if chunk_id in chunk_ids:
                    self.issues.append(f"Duplicate chunk ID: {chunk_id}")
                chunk_ids.add(chunk_id)
            
            # Check source document field (either 'source_document_id' or 'document_id')
            source_id = chunk.get('source_document_id') or chunk.get('document_id')
            if not source_id:
                self.issues.append(f"Chunk {i} missing source document field")
            
            # Check content
            if not chunk.get('content'):
                self.warnings.append(f"Chunk {chunk_id} has empty content")
        
        print(f"  ✓ Validated {len(self.chunks)} chunks")
        
        return len(self.issues) == 0
    
    def _cross_validate(self):
        """Cross-validate documents and chunks."""
        # Check that all chunks reference valid documents
        doc_ids = {doc['id'] for doc in self.documents}
        
        orphan_chunks = []
        for chunk in self.chunks:
            # Support both 'source_document_id' and 'document_id'
            source_id = chunk.get('source_document_id') or chunk.get('document_id')
            if source_id and source_id not in doc_ids:
                chunk_id = chunk.get('id') or chunk.get('chunk_id')
                orphan_chunks.append(chunk_id)
        
        if orphan_chunks:
            self.warnings.append(f"{len(orphan_chunks)} chunks reference non-existent documents")
        else:
            print("  ✓ All chunks reference valid documents")
    
    def _generate_statistics(self):
        """Generate dataset statistics."""
        # Document statistics
        self.stats['total_documents'] = len(self.documents)
        self.stats['total_chunks'] = len(self.chunks)
        
        # Word counts - support multiple field names
        total_words = 0
        for doc in self.documents:
            word_count = doc.get('word_count', 0) or doc.get('wordCount', 0)
            if not word_count:
                content = doc.get('content', '')
                if isinstance(content, str):
                    word_count = len(content.split())
            total_words += word_count
        self.stats['total_words'] = total_words
        
        # Character counts - support multiple field names
        total_chars = 0
        for doc in self.documents:
            char_count = doc.get('char_count', 0) or doc.get('charCount', 0)
            if not char_count:
                content = doc.get('content', '')
                if isinstance(content, str):
                    char_count = len(content)
            total_chars += char_count
        self.stats['total_characters'] = total_chars
        
        # Token estimates - support multiple field names
        total_tokens = 0
        for chunk in self.chunks:
            token_count = chunk.get('tokens', 0) or chunk.get('token_count', 0) or chunk.get('word_count', 0)
            if not token_count:
                # Try to get from char_count in chunk
                char_count = chunk.get('char_count', 0)
                if char_count:
                    token_count = int(char_count * 1.3)  # Chinese characters estimate
            total_tokens += token_count
        
        if total_tokens == 0:
            # Estimate from total characters
            total_tokens = int(total_chars * 1.1)
        self.stats['total_tokens'] = total_tokens
        
        # Document types
        doc_types = Counter(doc.get('type', 'unknown') for doc in self.documents)
        self.stats['document_types'] = dict(doc_types)
        
        # Categories
        categories = Counter(doc.get('category', 'general') for doc in self.documents)
        self.stats['categories'] = dict(categories)
        
        # Chunk types
        chunk_types = Counter(chunk.get('type', 'unknown') for chunk in self.chunks)
        self.stats['chunk_types'] = dict(chunk_types)
        
        print(f"  ✓ Generated statistics")
        print(f"    - Documents: {self.stats['total_documents']}")
        print(f"    - Chunks: {self.stats['total_chunks']}")
        print(f"    - Words: {self.stats['total_words']:,}")
        print(f"    - Tokens: {self.stats['total_tokens']:,}")
    
    def _save_report(self):
        """Save validation report."""
        report = {
            'dataset_name': self.dataset_name,
            'validation_date': datetime.now().isoformat(),
            'status': 'passed' if len(self.issues) == 0 else 'failed',
            'statistics': self.stats,
            'issues': self.issues,
            'warnings': self.warnings,
            'summary': {
                'total_issues': len(self.issues),
                'total_warnings': len(self.warnings),
                'validation_passed': len(self.issues) == 0
            }
        }
        
        report_file = os.path.join(self.processed_dir, 'validation_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ Saved: validation_report.json")
    
    def _print_summary(self):
        """Print validation summary."""
        print()
        print("=" * 80)
        print("Validation Summary")
        print("=" * 80)
        
        if len(self.issues) == 0:
            print("✅ VALIDATION PASSED")
        else:
            print("❌ VALIDATION FAILED")
            print()
            print("Issues:")
            for issue in self.issues:
                print(f"  - {issue}")
        
        if self.warnings:
            print()
            print(f"⚠️  {len(self.warnings)} Warning(s):")
            for warning in self.warnings[:5]:  # Show first 5
                print(f"  - {warning}")
            if len(self.warnings) > 5:
                print(f"  ... and {len(self.warnings) - 5} more")
        
        print()
        print("Statistics:")
        print(f"  Documents: {self.stats.get('total_documents', 0)}")
        print(f"  Chunks: {self.stats.get('total_chunks', 0)}")
        print(f"  Words: {self.stats.get('total_words', 0):,}")
        print(f"  Characters: {self.stats.get('total_characters', 0):,}")
        print(f"  Tokens (estimated): {self.stats.get('total_tokens', 0):,}")
        print("=" * 80)


def main():
    """Main execution function."""
    if len(sys.argv) < 3:
        print("Usage: python validate_dataset.py <dataset_name> <processed_dir>")
        print()
        print("Examples:")
        print("  python validate_dataset.py 'Elon Musk' datasets/elon_musk/processed_data")
        print("  python validate_dataset.py 'Queen Elizabeth II' datasets/queen_elizabeth_ii/processed_data")
        sys.exit(1)
    
    dataset_name = sys.argv[1]
    processed_dir = sys.argv[2]
    
    # Create validator
    validator = DatasetValidator(dataset_name, processed_dir)
    
    # Run validation
    success = validator.validate()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
