#!/usr/bin/env python3
"""
Validate Du Fu dataset for RAG system readiness.
Calculate token counts and verify data quality.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import json
import os


def estimate_tokens(text, language='zh'):
    """
    Estimate token count for text.
    
    For Classical Chinese:
    - Each character is roughly 1 token
    - Punctuation adds minimal tokens
    
    Args:
        text: Text to count
        language: Language code ('zh' for Chinese)
    
    Returns:
        Estimated token count
    """
    if language == 'zh':
        # For Chinese, character count approximates token count
        # Add small overhead for punctuation and formatting
        char_count = len(text)
        return int(char_count * 1.1)  # 10% overhead
    else:
        # For other languages, rough approximation
        return len(text.split()) * 1.3


def validate_dataset(processed_data_dir):
    """
    Validate the processed Du Fu dataset.
    
    Args:
        processed_data_dir: Directory containing processed data files
    """
    print("=" * 80)
    print("Du Fu Dataset Validation and Token Count")
    print("=" * 80)
    print()
    
    # Load processed files
    structured_docs_file = os.path.join(processed_data_dir, 'structured_documents.json')
    training_chunks_file = os.path.join(processed_data_dir, 'training_chunks.json')
    metadata_file = os.path.join(processed_data_dir, 'dataset_metadata.json')
    processing_report_file = os.path.join(processed_data_dir, 'processing_report.json')
    
    # Check file existence
    required_files = {
        'structured_documents.json': structured_docs_file,
        'training_chunks.json': training_chunks_file,
        'dataset_metadata.json': metadata_file,
        'processing_report.json': processing_report_file
    }
    
    print("File Existence Check:")
    all_files_exist = True
    for name, path in required_files.items():
        exists = os.path.exists(path)
        status = "✓" if exists else "✗"
        print(f"  {status} {name}")
        if not exists:
            all_files_exist = False
    print()
    
    if not all_files_exist:
        print("Error: Some required files are missing!")
        return
    
    # Load data
    with open(structured_docs_file, 'r', encoding='utf-8') as f:
        structured_docs = json.load(f)
    
    with open(training_chunks_file, 'r', encoding='utf-8') as f:
        training_chunks = json.load(f)
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    with open(processing_report_file, 'r', encoding='utf-8') as f:
        processing_report = json.load(f)
    
    # Calculate statistics
    print("Dataset Statistics:")
    print(f"  Total Documents: {len(structured_docs):,}")
    print(f"  Total Training Chunks: {len(training_chunks):,}")
    print()
    
    # Token count estimation
    print("Token Count Estimation:")
    print()
    
    # Calculate tokens from structured documents
    total_doc_tokens = 0
    for doc in structured_docs:
        text = doc['content']['full_text']
        tokens = estimate_tokens(text, language='zh')
        total_doc_tokens += tokens
    
    print(f"  Structured Documents:")
    print(f"    Total tokens: {total_doc_tokens:,}")
    print(f"    Average tokens per document: {total_doc_tokens // len(structured_docs):,}")
    print()
    
    # Calculate tokens from training chunks
    total_chunk_tokens = 0
    chunk_token_counts = []
    for chunk in training_chunks:
        text = chunk['content']
        tokens = estimate_tokens(text, language='zh')
        total_chunk_tokens += tokens
        chunk_token_counts.append(tokens)
    
    avg_chunk_tokens = total_chunk_tokens // len(training_chunks)
    min_chunk_tokens = min(chunk_token_counts)
    max_chunk_tokens = max(chunk_token_counts)
    
    print(f"  Training Chunks:")
    print(f"    Total tokens: {total_chunk_tokens:,}")
    print(f"    Average tokens per chunk: {avg_chunk_tokens:,}")
    print(f"    Min chunk tokens: {min_chunk_tokens:,}")
    print(f"    Max chunk tokens: {max_chunk_tokens:,}")
    print()
    
    # Target assessment
    target_tokens = 100000
    achievement_percentage = (total_chunk_tokens / target_tokens) * 100
    
    print("Target Assessment:")
    print(f"  Target: {target_tokens:,} tokens")
    print(f"  Actual: {total_chunk_tokens:,} tokens")
    print(f"  Achievement: {achievement_percentage:.2f}%")
    
    if total_chunk_tokens >= target_tokens:
        print(f"  Status: ✓ TARGET ACHIEVED (exceeded by {total_chunk_tokens - target_tokens:,} tokens)")
    else:
        shortfall = target_tokens - total_chunk_tokens
        print(f"  Status: ✗ Below target (need {shortfall:,} more tokens)")
    print()
    
    # Quality checks
    print("Quality Checks:")
    print()
    
    # Check 1: All documents have IDs
    docs_with_ids = sum(1 for doc in structured_docs if doc.get('id'))
    print(f"  1. Documents with IDs: {docs_with_ids}/{len(structured_docs)} "
          f"({'✓ PASS' if docs_with_ids == len(structured_docs) else '✗ FAIL'})")
    
    # Check 2: All chunks have source document IDs
    chunks_with_source = sum(1 for chunk in training_chunks if chunk.get('source_document_id'))
    print(f"  2. Chunks with source IDs: {chunks_with_source}/{len(training_chunks)} "
          f"({'✓ PASS' if chunks_with_source == len(training_chunks) else '✗ FAIL'})")
    
    # Check 3: All chunks have content
    chunks_with_content = sum(1 for chunk in training_chunks if chunk.get('content'))
    print(f"  3. Chunks with content: {chunks_with_content}/{len(training_chunks)} "
          f"({'✓ PASS' if chunks_with_content == len(training_chunks) else '✗ FAIL'})")
    
    # Check 4: Documents have proper metadata
    docs_with_metadata = sum(1 for doc in structured_docs 
                             if doc.get('metadata') and doc['metadata'].get('persona'))
    print(f"  4. Documents with metadata: {docs_with_metadata}/{len(structured_docs)} "
          f"({'✓ PASS' if docs_with_metadata == len(structured_docs) else '✗ FAIL'})")
    
    # Check 5: Chunk diversity (multiple chunk types)
    chunk_types = set(chunk.get('chunk_type', '') for chunk in training_chunks)
    print(f"  5. Chunk type diversity: {len(chunk_types)} types "
          f"({'✓ PASS' if len(chunk_types) >= 2 else '✗ FAIL'})")
    print(f"     Types: {', '.join(chunk_types)}")
    
    # Check 6: Temporal coverage
    time_periods = set(doc['metadata'].get('time_period', '') 
                      for doc in structured_docs if doc['metadata'].get('time_period'))
    print(f"  6. Temporal coverage: {len(time_periods)} time periods "
          f"({'✓ PASS' if len(time_periods) >= 10 else '✗ FAIL'})")
    
    print()
    
    # Content distribution
    print("Content Distribution:")
    print()
    
    # Poem types
    poem_types = processing_report['content_distribution']['poem_types']
    print("  Top Poem Types:")
    for poem_type, count in sorted(poem_types.items(), key=lambda x: x[1], reverse=True)[:5]:
        percentage = (count / len(structured_docs)) * 100
        print(f"    {poem_type}: {count} ({percentage:.1f}%)")
    print()
    
    # Chunk types
    chunk_type_counts = {}
    for chunk in training_chunks:
        chunk_type = chunk.get('chunk_type', 'unknown')
        chunk_type_counts[chunk_type] = chunk_type_counts.get(chunk_type, 0) + 1
    
    print("  Chunk Type Distribution:")
    for chunk_type, count in sorted(chunk_type_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(training_chunks)) * 100
        print(f"    {chunk_type}: {count} ({percentage:.1f}%)")
    print()
    
    # Language and cultural features
    print("Language and Cultural Features:")
    docs_with_allusions = sum(1 for doc in structured_docs 
                              if doc['metadata'].get('has_allusions'))
    docs_with_annotations = sum(1 for doc in structured_docs 
                               if doc['metadata'].get('has_annotations'))
    
    print(f"  Poems with allusions: {docs_with_allusions} ({(docs_with_allusions/len(structured_docs)*100):.1f}%)")
    print(f"  Poems with annotations: {docs_with_annotations} ({(docs_with_annotations/len(structured_docs)*100):.1f}%)")
    print()
    
    # Overall assessment
    print("=" * 80)
    print("Overall Assessment")
    print("=" * 80)
    
    if total_chunk_tokens >= target_tokens:
        print("✓ DATASET READY FOR RAG TRAINING")
        print()
        print(f"  Total tokens: {total_chunk_tokens:,}")
        print(f"  Target achievement: {achievement_percentage:.2f}%")
        print(f"  Documents: {len(structured_docs):,}")
        print(f"  Training chunks: {len(training_chunks):,}")
        print(f"  Temporal coverage: {len(time_periods)} periods (712-770 CE)")
        print(f"  Literary richness: {docs_with_allusions} poems with allusions")
        print(f"  Scholarly depth: {docs_with_annotations} poems with annotations")
    else:
        print("⚠ DATASET BELOW TARGET")
        print()
        print(f"  Current tokens: {total_chunk_tokens:,}")
        print(f"  Target tokens: {target_tokens:,}")
        print(f"  Shortfall: {target_tokens - total_chunk_tokens:,}")
    
    print()
    print("=" * 80)
    
    # Save validation report
    validation_report = {
        "validation_date": metadata['processing_date'],
        "dataset_name": metadata['dataset_name'],
        "author": metadata['author'],
        
        "file_checks": {
            "all_files_present": all_files_exist,
            "files_checked": list(required_files.keys())
        },
        
        "token_counts": {
            "structured_documents_tokens": total_doc_tokens,
            "training_chunks_tokens": total_chunk_tokens,
            "average_tokens_per_chunk": avg_chunk_tokens,
            "min_chunk_tokens": min_chunk_tokens,
            "max_chunk_tokens": max_chunk_tokens
        },
        
        "target_assessment": {
            "target_tokens": target_tokens,
            "actual_tokens": total_chunk_tokens,
            "achievement_percentage": round(achievement_percentage, 2),
            "target_achieved": total_chunk_tokens >= target_tokens
        },
        
        "quality_checks": {
            "documents_with_ids": docs_with_ids == len(structured_docs),
            "chunks_with_source_ids": chunks_with_source == len(training_chunks),
            "chunks_with_content": chunks_with_content == len(training_chunks),
            "documents_with_metadata": docs_with_metadata == len(structured_docs),
            "chunk_type_diversity": len(chunk_types) >= 2,
            "temporal_coverage": len(time_periods) >= 10
        },
        
        "content_statistics": {
            "total_documents": len(structured_docs),
            "total_chunks": len(training_chunks),
            "chunk_types": chunk_type_counts,
            "temporal_periods": len(time_periods),
            "poems_with_allusions": docs_with_allusions,
            "poems_with_annotations": docs_with_annotations
        }
    }
    
    output_path = os.path.join(processed_data_dir, 'validation_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, ensure_ascii=False, indent=2)
    
    print(f"Validation report saved to: validation_report.json")
    print()


def main():
    """Main execution function."""
    
    processed_data_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/du_fu/processed_data"
    
    validate_dataset(processed_data_dir)


if __name__ == "__main__":
    main()
