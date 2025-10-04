#!/usr/bin/env python3
"""
Process Du Fu poems for RAG training.
Transforms extracted JSON data into structured documents and training chunks
suitable for retrieval-augmented generation systems.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import json
import os
from datetime import datetime
from collections import defaultdict


class DuFuRAGProcessor:
    """
    Process Du Fu poetry data for RAG system training.
    Creates structured documents and optimized chunks from raw poem data.
    """
    
    def __init__(self, json_file_path, output_dir):
        """
        Initialize the processor.
        
        Args:
            json_file_path: Path to dufu_poems_full.json
            output_dir: Directory for processed output
        """
        self.json_file_path = json_file_path
        self.output_dir = output_dir
        
        # Load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.poems = self.data['poems']
        self.metadata = self.data['metadata']
        
        # Storage for processed data
        self.structured_documents = []
        self.training_chunks = []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def process_all(self):
        """
        Main processing method - execute all processing steps.
        """
        print("=" * 80)
        print("Du Fu Poetry RAG Processing")
        print("=" * 80)
        print(f"Input: {self.json_file_path}")
        print(f"Total poems: {len(self.poems)}")
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Step 1: Create structured documents
        print("Step 1: Creating structured documents...")
        self._create_structured_documents()
        print(f"  Created {len(self.structured_documents)} documents")
        
        # Step 2: Generate training chunks
        print("Step 2: Generating training chunks...")
        self._generate_training_chunks()
        print(f"  Created {len(self.training_chunks)} chunks")
        
        # Step 3: Save outputs
        print()
        print("Step 3: Saving processed data...")
        self._save_structured_documents()
        self._save_training_chunks()
        self._save_dataset_metadata()
        self._save_processing_report()
        
        print()
        print("=" * 80)
        print("Processing Complete!")
        print("=" * 80)
    
    def _create_structured_documents(self):
        """
        Create structured documents from raw poem data.
        Each poem becomes a structured document with metadata.
        """
        for poem in self.poems:
            # Create full text
            full_text_parts = []
            
            # Title
            if poem['title']:
                full_text_parts.append(f"Title: {poem['title']}")
                full_text_parts.append("")
            
            # Poem lines
            if poem['lines']:
                full_text_parts.append("Poem:")
                full_text_parts.extend(poem['lines'])
                full_text_parts.append("")
            
            # Creation information
            creation_info = []
            if poem['creation_date']:
                creation_info.append(f"Date: {poem['creation_date']}")
            if poem['place_code']:
                creation_info.append(f"Place: {poem['place_code']}")
            if creation_info:
                full_text_parts.append("Creation Information:")
                full_text_parts.extend(creation_info)
                full_text_parts.append("")
            
            # Literary characteristics
            lit_info = []
            if poem['poem_type']:
                lit_info.append(f"Type: {poem['poem_type']}")
            if poem['rhyme_category']:
                lit_info.append(f"Rhyme: {poem['rhyme_category']}")
            if lit_info:
                full_text_parts.append("Literary Characteristics:")
                full_text_parts.extend(lit_info)
                full_text_parts.append("")
            
            # Allusions
            if poem['allusions']:
                full_text_parts.append("Allusions:")
                for allusion in poem['allusions']:
                    if allusion['text']:
                        full_text_parts.append(f"  - {allusion['text']}")
                full_text_parts.append("")
            
            # Annotations
            if poem['text_annotations']:
                full_text_parts.append("Annotations:")
                for ann in poem['text_annotations'][:5]:  # Limit to first 5
                    if ann['content']:
                        full_text_parts.append(f"  - {ann['content']}")
                if len(poem['text_annotations']) > 5:
                    full_text_parts.append(f"  ... and {len(poem['text_annotations']) - 5} more")
                full_text_parts.append("")
            
            full_text = "\n".join(full_text_parts)
            
            # Character count (for Classical Chinese, character count is more relevant than word count)
            char_count = sum(len(line) for line in poem['lines'])
            
            # Create structured document
            doc = {
                "id": f"dufu_{poem['poem_id']}",
                "type": "poem",
                "title": poem['title'] or "Untitled",
                "source": {
                    "database": "CNKGraph.Writings.xml",
                    "author": "杜甫",
                    "author_id": poem['author_id'],
                    "poem_id": poem['poem_id'],
                    "collected": self.metadata['extraction_date'],
                    "processed": datetime.now().isoformat()
                },
                "content": {
                    "full_text": full_text,
                    "poem_lines": poem['lines'],
                    "line_count": len(poem['lines']),
                    "char_count": char_count
                },
                "metadata": {
                    "persona": "Du Fu (杜甫)",
                    "time_period": poem['creation_date'] or "Unknown",
                    "place": poem['place_code'] or "Unknown",
                    "poem_type": poem['poem_type'] or "Unknown",
                    "poem_type_detail": poem['poem_type_detail'] or "Unknown",
                    "rhyme_category": poem['rhyme_category'] or "Unknown",
                    "has_allusions": len(poem['allusions']) > 0,
                    "allusion_count": len(poem['allusions']),
                    "has_annotations": len(poem['text_annotations']) > 0,
                    "annotation_count": len(poem['text_annotations']),
                    "language": "Classical Chinese",
                    "formality": "Formal",
                    "content_category": "poetry"
                }
            }
            
            self.structured_documents.append(doc)
    
    def _generate_training_chunks(self):
        """
        Generate training chunks from structured documents.
        Each chunk is optimized for RAG retrieval.
        """
        chunk_id = 1
        
        for doc in self.structured_documents:
            # Strategy: For poems, create chunks based on content structure
            
            # Chunk 1: Basic poem content (title + text + creation info)
            chunk_parts = []
            
            if doc['title']:
                chunk_parts.append(f"Poem Title: {doc['title']}")
            
            if doc['content']['poem_lines']:
                chunk_parts.append("\nPoem Text:")
                chunk_parts.extend(doc['content']['poem_lines'])
            
            # Add creation context
            if doc['metadata']['time_period'] != "Unknown":
                chunk_parts.append(f"\nCreation Date: {doc['metadata']['time_period']}")
            if doc['metadata']['place'] != "Unknown":
                chunk_parts.append(f"Location: {doc['metadata']['place']}")
            if doc['metadata']['poem_type'] != "Unknown":
                chunk_parts.append(f"Poem Type: {doc['metadata']['poem_type']}")
            
            # Create first chunk (basic content)
            chunk1_text = "\n".join(chunk_parts)
            chunk1 = {
                "chunk_id": f"dufu_chunk_{chunk_id:04d}",
                "source_document_id": doc['id'],
                "chunk_type": "poem_content",
                "content": chunk1_text,
                "char_count": len(chunk1_text),
                "metadata": {
                    "persona": doc['metadata']['persona'],
                    "time_period": doc['metadata']['time_period'],
                    "poem_title": doc['title'],
                    "poem_type": doc['metadata']['poem_type'],
                    "language": doc['metadata']['language'],
                    "has_allusions": doc['metadata']['has_allusions'],
                    "has_annotations": doc['metadata']['has_annotations']
                }
            }
            self.training_chunks.append(chunk1)
            chunk_id += 1
            
            # Chunk 2: If poem has allusions, create a separate context chunk
            # Find allusions in original poem data
            poem = next((p for p in self.poems if p['poem_id'] == doc['source']['poem_id']), None)
            
            if poem and poem['allusions'] and len(poem['allusions']) > 0:
                allusion_parts = [f"Poem: {doc['title']}", ""]
                allusion_parts.append("Literary Allusions and References:")
                
                for allusion in poem['allusions']:
                    if allusion['text']:
                        allusion_parts.append(f"  {allusion['text']}")
                
                chunk2_text = "\n".join(allusion_parts)
                chunk2 = {
                    "chunk_id": f"dufu_chunk_{chunk_id:04d}",
                    "source_document_id": doc['id'],
                    "chunk_type": "allusions_context",
                    "content": chunk2_text,
                    "char_count": len(chunk2_text),
                    "metadata": {
                        "persona": doc['metadata']['persona'],
                        "time_period": doc['metadata']['time_period'],
                        "poem_title": doc['title'],
                        "poem_type": doc['metadata']['poem_type'],
                        "language": doc['metadata']['language'],
                        "allusion_count": len(poem['allusions'])
                    }
                }
                self.training_chunks.append(chunk2)
                chunk_id += 1
            
            # Chunk 3: If poem has substantial annotations, create annotation chunk
            if poem and poem['text_annotations'] and len(poem['text_annotations']) > 0:
                ann_parts = [f"Poem: {doc['title']}", ""]
                ann_parts.append("Scholarly Annotations:")
                
                for ann in poem['text_annotations'][:10]:  # Limit to 10 most important
                    if ann['content']:
                        ann_parts.append(f"  {ann['content']}")
                
                if len(poem['text_annotations']) > 10:
                    ann_parts.append(f"\n... and {len(poem['text_annotations']) - 10} more annotations")
                
                chunk3_text = "\n".join(ann_parts)
                chunk3 = {
                    "chunk_id": f"dufu_chunk_{chunk_id:04d}",
                    "source_document_id": doc['id'],
                    "chunk_type": "annotations_context",
                    "content": chunk3_text,
                    "char_count": len(chunk3_text),
                    "metadata": {
                        "persona": doc['metadata']['persona'],
                        "time_period": doc['metadata']['time_period'],
                        "poem_title": doc['title'],
                        "poem_type": doc['metadata']['poem_type'],
                        "language": doc['metadata']['language'],
                        "annotation_count": len(poem['text_annotations'])
                    }
                }
                self.training_chunks.append(chunk3)
                chunk_id += 1
    
    def _save_structured_documents(self):
        """Save structured documents to JSON file."""
        output_path = os.path.join(self.output_dir, 'structured_documents.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.structured_documents, f, ensure_ascii=False, indent=2)
        
        print(f"  Saved: structured_documents.json ({len(self.structured_documents)} documents)")
    
    def _save_training_chunks(self):
        """Save training chunks to JSON file."""
        output_path = os.path.join(self.output_dir, 'training_chunks.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.training_chunks, f, ensure_ascii=False, indent=2)
        
        print(f"  Saved: training_chunks.json ({len(self.training_chunks)} chunks)")
    
    def _save_dataset_metadata(self):
        """Save dataset metadata."""
        metadata = {
            "dataset_name": "Du Fu Poetry Collection",
            "author": "杜甫 (Du Fu)",
            "author_id": self.metadata['author_id'],
            "total_poems": len(self.poems),
            "total_documents": len(self.structured_documents),
            "total_chunks": len(self.training_chunks),
            "language": "Classical Chinese",
            "time_period": "712-770 CE",
            "dynasty": "Tang Dynasty",
            "extraction_date": self.metadata['extraction_date'],
            "processing_date": datetime.now().isoformat(),
            "source_database": "CNKGraph.Writings.xml",
            "project": "Living Voices - RAG-based Dialogue System"
        }
        
        output_path = os.path.join(self.output_dir, 'dataset_metadata.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"  Saved: dataset_metadata.json")
    
    def _save_processing_report(self):
        """Generate and save processing report."""
        # Calculate statistics
        total_chars = sum(doc['content']['char_count'] for doc in self.structured_documents)
        avg_chars_per_poem = total_chars / len(self.structured_documents) if self.structured_documents else 0
        
        # Analyze poem types
        poem_type_dist = defaultdict(int)
        time_period_dist = defaultdict(int)
        place_dist = defaultdict(int)
        
        for doc in self.structured_documents:
            poem_type_dist[doc['metadata']['poem_type']] += 1
            time_period_dist[doc['metadata']['time_period']] += 1
            place_dist[doc['metadata']['place']] += 1
        
        # Count poems with allusions and annotations
        poems_with_allusions = sum(1 for doc in self.structured_documents if doc['metadata']['has_allusions'])
        poems_with_annotations = sum(1 for doc in self.structured_documents if doc['metadata']['has_annotations'])
        
        # Chunk statistics
        chunk_type_dist = defaultdict(int)
        for chunk in self.training_chunks:
            chunk_type_dist[chunk['chunk_type']] += 1
        
        report = {
            "processing_date": datetime.now().isoformat(),
            "input_file": os.path.basename(self.json_file_path),
            "output_directory": self.output_dir,
            
            "source_statistics": {
                "total_poems": len(self.poems),
                "author": "杜甫",
                "author_id": self.metadata['author_id']
            },
            
            "document_statistics": {
                "total_documents": len(self.structured_documents),
                "total_characters": total_chars,
                "average_characters_per_poem": round(avg_chars_per_poem, 2),
                "poems_with_allusions": poems_with_allusions,
                "poems_with_allusions_percentage": round((poems_with_allusions / len(self.structured_documents)) * 100, 2),
                "poems_with_annotations": poems_with_annotations,
                "poems_with_annotations_percentage": round((poems_with_annotations / len(self.structured_documents)) * 100, 2)
            },
            
            "content_distribution": {
                "poem_types": dict(poem_type_dist),
                "top_5_poem_types": sorted(poem_type_dist.items(), key=lambda x: x[1], reverse=True)[:5],
                "time_periods": len(time_period_dist),
                "unique_places": len(place_dist)
            },
            
            "chunk_statistics": {
                "total_chunks": len(self.training_chunks),
                "chunk_types": dict(chunk_type_dist),
                "average_chunks_per_poem": round(len(self.training_chunks) / len(self.structured_documents), 2)
            }
        }
        
        output_path = os.path.join(self.output_dir, 'processing_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"  Saved: processing_report.json")
        
        # Print summary
        print()
        print("=" * 80)
        print("Processing Report Summary")
        print("=" * 80)
        print(f"Total Poems: {report['source_statistics']['total_poems']}")
        print(f"Total Characters: {report['document_statistics']['total_characters']:,}")
        print(f"Average Characters per Poem: {report['document_statistics']['average_characters_per_poem']}")
        print()
        print(f"Poems with Allusions: {report['document_statistics']['poems_with_allusions']} "
              f"({report['document_statistics']['poems_with_allusions_percentage']}%)")
        print(f"Poems with Annotations: {report['document_statistics']['poems_with_annotations']} "
              f"({report['document_statistics']['poems_with_annotations_percentage']}%)")
        print()
        print("Top 5 Poem Types:")
        for poem_type, count in report['content_distribution']['top_5_poem_types']:
            print(f"  {poem_type}: {count}")
        print()
        print(f"Total Training Chunks: {report['chunk_statistics']['total_chunks']}")
        print("Chunk Types:")
        for chunk_type, count in report['chunk_statistics']['chunk_types'].items():
            print(f"  {chunk_type}: {count}")
        print("=" * 80)


def main():
    """Main execution function."""
    
    # Configuration
    json_file = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/du_fu/raw_data/dufu_poems_full.json"
    output_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/du_fu/processed_data"
    
    # Create processor
    processor = DuFuRAGProcessor(json_file, output_dir)
    
    # Process all data
    processor.process_all()


if __name__ == "__main__":
    main()
