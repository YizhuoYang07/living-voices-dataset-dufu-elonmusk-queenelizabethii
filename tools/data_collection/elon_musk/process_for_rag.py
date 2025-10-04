#!/usr/bin/env python3
"""
Process Elon Musk raw data for RAG training.
Converts raw Wikipedia articles into structured documents and training chunks.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import json
import os
from datetime import datetime


class ElonMuskDataProcessor:
    """
    Processes Elon Musk raw data into RAG-optimized format.
    """
    
    def __init__(self, raw_data_dir, output_dir):
        """
        Initialize the processor.
        
        Args:
            raw_data_dir: Directory containing raw JSON files
            output_dir: Directory for processed output files
        """
        self.raw_data_dir = raw_data_dir
        self.output_dir = output_dir
        
        os.makedirs(output_dir, exist_ok=True)
        
        self.documents = []
        self.chunks = []
        
    def process_all(self):
        """
        Main processing method.
        """
        print("=" * 80)
        print("Elon Musk Dataset - RAG Processing")
        print("=" * 80)
        print(f"Raw data: {self.raw_data_dir}")
        print(f"Output: {self.output_dir}")
        print()
        
        # Step 1: Load and process biography
        print("Step 1: Processing biography...")
        self._process_biography()
        
        # Step 2: Load and process related articles
        print("\nStep 2: Processing related articles...")
        self._process_related_articles()
        
        # Step 3: Load and process supplementary materials
        print("\nStep 3: Processing supplementary materials...")
        self._process_supplementary_materials()
        
        # Step 4: Generate training chunks
        print("\nStep 4: Generating training chunks...")
        self._generate_training_chunks()
        
        # Step 5: Save all data
        print("\nStep 5: Saving processed data...")
        self._save_all_data()
        
        print("\n" + "=" * 80)
        print("Processing Complete!")
        print("=" * 80)
        
    def _process_biography(self):
        """Process main biography."""
        bio_file = os.path.join(self.raw_data_dir, 'wikipedia', 'biography.json')
        
        if not os.path.exists(bio_file):
            print("  ⚠️  Biography file not found")
            return
            
        with open(bio_file, 'r', encoding='utf-8') as f:
            bio_data = json.load(f)
        
        doc = {
            'id': 'musk_bio_001',
            'title': bio_data.get('title', 'Elon Musk'),
            'type': 'biography',
            'category': 'main_biography',
            'content': bio_data.get('content', ''),
            'summary': bio_data.get('summary', ''),
            'url': bio_data.get('url', ''),
            'word_count': bio_data.get('word_count', 0),
            'char_count': bio_data.get('char_count', 0),
            'collected': bio_data.get('collected', datetime.now().isoformat()),
            'processed': datetime.now().isoformat()
        }
        
        self.documents.append(doc)
        print(f"  ✓ Processed: {doc['title']} ({doc['word_count']} words)")
        
    def _process_related_articles(self):
        """Process related Wikipedia articles."""
        articles_file = os.path.join(self.raw_data_dir, 'wikipedia', 'related_articles.json')
        
        if not os.path.exists(articles_file):
            print("  ⚠️  Related articles file not found")
            return
            
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        for i, article in enumerate(articles, 1):
            doc = {
                'id': f'musk_related_{i:03d}',
                'title': article.get('title', ''),
                'type': 'context',
                'category': article.get('category', 'general'),
                'content': article.get('content', ''),
                'summary': article.get('summary', ''),
                'url': article.get('url', ''),
                'word_count': article.get('word_count', 0),
                'char_count': article.get('char_count', 0),
                'collected': article.get('collected', datetime.now().isoformat()),
                'processed': datetime.now().isoformat()
            }
            
            self.documents.append(doc)
            print(f"  ✓ Processed ({i}/{len(articles)}): {doc['title']} ({doc['word_count']} words)")
    
    def _process_supplementary_materials(self):
        """Process supplementary materials."""
        supp_file = os.path.join(self.raw_data_dir, 'supplementary_materials', 'supplementary_materials.json')
        
        if not os.path.exists(supp_file):
            print("  ⚠️  Supplementary materials file not found")
            return
            
        with open(supp_file, 'r', encoding='utf-8') as f:
            materials = json.load(f)
        
        for i, material in enumerate(materials, 1):
            doc = {
                'id': f'musk_supp_{i:03d}',
                'title': material.get('title', ''),
                'type': 'supplementary',
                'category': material.get('category', 'general'),
                'content': material.get('content', ''),
                'summary': material.get('summary', ''),
                'url': material.get('url', ''),
                'word_count': material.get('word_count', 0),
                'char_count': material.get('char_count', 0),
                'description': material.get('description', ''),
                'collected': material.get('collected', datetime.now().isoformat()),
                'processed': datetime.now().isoformat()
            }
            
            self.documents.append(doc)
            print(f"  ✓ Processed ({i}/{len(materials)}): {doc['title']} ({doc['word_count']} words)")
    
    def _generate_training_chunks(self):
        """Generate training chunks from documents."""
        chunk_id = 1
        
        for doc in self.documents:
            # Create main content chunk
            main_chunk = {
                'id': f'musk_chunk_{chunk_id:04d}',
                'source_document_id': doc['id'],
                'type': 'full_article',
                'title': doc['title'],
                'content': doc['content'],
                'summary': doc.get('summary', ''),
                'category': doc.get('category', 'general'),
                'metadata': {
                    'document_type': doc['type'],
                    'word_count': doc['word_count'],
                    'char_count': doc['char_count'],
                    'url': doc.get('url', '')
                },
                'tokens': int(doc['char_count'] * 1.1)  # Estimate tokens
            }
            
            self.chunks.append(main_chunk)
            chunk_id += 1
            
            # Create summary chunk if available
            if doc.get('summary') and len(doc['summary']) > 100:
                summary_chunk = {
                    'id': f'musk_chunk_{chunk_id:04d}',
                    'source_document_id': doc['id'],
                    'type': 'summary',
                    'title': f"{doc['title']} - Summary",
                    'content': doc['summary'],
                    'category': doc.get('category', 'general'),
                    'metadata': {
                        'document_type': doc['type'],
                        'is_summary': True,
                        'url': doc.get('url', '')
                    },
                    'tokens': int(len(doc['summary']) * 1.1)
                }
                
                self.chunks.append(summary_chunk)
                chunk_id += 1
        
        print(f"  ✓ Generated {len(self.chunks)} training chunks")
    
    def _save_all_data(self):
        """Save all processed data."""
        # Save structured documents
        docs_file = os.path.join(self.output_dir, 'structured_documents.json')
        with open(docs_file, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: structured_documents.json ({len(self.documents)} documents)")
        
        # Save training chunks
        chunks_file = os.path.join(self.output_dir, 'training_chunks.json')
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: training_chunks.json ({len(self.chunks)} chunks)")
        
        # Generate metadata
        metadata = {
            'dataset_name': 'Elon Musk',
            'person': 'Elon Musk',
            'processing_date': datetime.now().isoformat(),
            'total_documents': len(self.documents),
            'total_chunks': len(self.chunks),
            'total_words': sum(doc['word_count'] for doc in self.documents),
            'total_characters': sum(doc['char_count'] for doc in self.documents),
            'estimated_tokens': int(sum(doc['char_count'] for doc in self.documents) * 1.1),
            'document_types': {},
            'categories': {}
        }
        
        # Count by type
        for doc in self.documents:
            doc_type = doc['type']
            metadata['document_types'][doc_type] = metadata['document_types'].get(doc_type, 0) + 1
            
            category = doc.get('category', 'general')
            metadata['categories'][category] = metadata['categories'].get(category, 0) + 1
        
        metadata_file = os.path.join(self.output_dir, 'dataset_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: dataset_metadata.json")
        
        # Generate processing report
        report = {
            'processing_date': datetime.now().isoformat(),
            'dataset': 'Elon Musk',
            'status': 'complete',
            'statistics': {
                'total_documents': len(self.documents),
                'total_chunks': len(self.chunks),
                'total_words': metadata['total_words'],
                'total_characters': metadata['total_characters'],
                'estimated_tokens': metadata['estimated_tokens']
            },
            'document_breakdown': metadata['document_types'],
            'category_breakdown': metadata['categories'],
            'processing_steps': [
                'Loaded main biography',
                'Loaded related articles',
                'Loaded supplementary materials',
                'Generated training chunks',
                'Saved all processed data'
            ]
        }
        
        report_file = os.path.join(self.output_dir, 'processing_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: processing_report.json")
        
        # Print summary
        print()
        print("=" * 80)
        print("Processing Summary")
        print("=" * 80)
        print(f"Documents processed: {len(self.documents)}")
        print(f"Training chunks created: {len(self.chunks)}")
        print(f"Total words: {metadata['total_words']:,}")
        print(f"Total characters: {metadata['total_characters']:,}")
        print(f"Estimated tokens: {metadata['estimated_tokens']:,}")
        print()
        print("Document types:")
        for doc_type, count in metadata['document_types'].items():
            print(f"  - {doc_type}: {count}")
        print()
        print("Categories:")
        for category, count in sorted(metadata['categories'].items()):
            print(f"  - {category}: {count}")
        print("=" * 80)


def main():
    """Main execution function."""
    
    # Configuration
    raw_data_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/elon_musk/raw_data"
    output_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/elon_musk/processed_data"
    
    # Create processor
    processor = ElonMuskDataProcessor(raw_data_dir, output_dir)
    
    # Process all data
    processor.process_all()


if __name__ == "__main__":
    main()
