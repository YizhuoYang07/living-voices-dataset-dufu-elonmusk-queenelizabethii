"""
Queen Elizabeth II Data Processing Pipeline

This script processes raw Wikipedia data and creates structured datasets
suitable for RAG system integration.

Author: Living Voices Project
Date: 2024-10-04
Phase: 2 - Data Processing
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class QueenElizabethDataProcessor:
    """
    Processor for Queen Elizabeth II raw data to create structured training datasets.
    """
    
    def __init__(self, raw_data_dir: str, processed_data_dir: str):
        """
        Initialize the processor.
        
        Args:
            raw_data_dir: Directory containing raw data
            processed_data_dir: Directory to save processed data
        """
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        
        self.processing_log = []
        self.statistics = {
            "start_time": datetime.now().isoformat(),
            "raw_sources": 0,
            "processed_documents": 0,
            "total_chunks": 0,
            "total_tokens": 0
        }
    
    def process_all(self):
        """
        Main processing pipeline.
        """
        print("="*70)
        print("Queen Elizabeth II Data Processing Pipeline")
        print("="*70)
        print()
        
        # Step 1: Load raw data
        print("Step 1: Loading raw data...")
        biography, articles = self._load_raw_data()
        
        # Step 2: Clean and normalize text
        print("\nStep 2: Cleaning and normalizing text...")
        biography_clean = self._clean_text(biography)
        articles_clean = [self._clean_text(article) for article in articles]
        
        # Step 3: Add metadata and structure
        print("\nStep 3: Adding metadata and structure...")
        biography_structured = self._structure_document(biography_clean, "biography")
        articles_structured = [
            self._structure_document(article, "related_article") 
            for article in articles_clean
        ]
        
        # Step 4: Create training chunks
        print("\nStep 4: Creating training chunks...")
        all_chunks = self._create_chunks(biography_structured, articles_structured)
        
        # Step 5: Save processed data
        print("\nStep 5: Saving processed datasets...")
        self._save_processed_data(biography_structured, articles_structured, all_chunks)
        
        # Step 6: Generate statistics
        print("\nStep 6: Generating statistics and report...")
        self._generate_processing_report()
        
        print("\n" + "="*70)
        print("Processing Complete!")
        print("="*70)
    
    def _load_raw_data(self) -> Tuple[Dict, List[Dict]]:
        """
        Load raw data from JSON files.
        
        Returns:
            Tuple of (biography, list of articles)
        """
        # Load biography
        biography_file = self.raw_data_dir / "wikipedia" / "biography.json"
        with open(biography_file, 'r', encoding='utf-8') as f:
            biography = json.load(f)
        print(f"  ✓ Loaded biography: {biography.get('word_count', 0):,} words")
        self.statistics["raw_sources"] += 1
        
        # Load related articles
        articles_file = self.raw_data_dir / "wikipedia" / "related_articles.json"
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        print(f"  ✓ Loaded {len(articles)} related articles")
        self.statistics["raw_sources"] += len(articles)
        
        return biography, articles
    
    def _clean_text(self, document: Dict) -> Dict:
        """
        Clean and normalize text content.
        
        Args:
            document: Document dictionary with content
            
        Returns:
            Cleaned document dictionary
        """
        content = document.get("content", "")
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove Wikipedia-specific markers
        content = re.sub(r'\[\d+\]', '', content)  # Citation markers [1], [2]
        content = re.sub(r'==\s*(.+?)\s*==', r'\n\n\1\n\n', content)  # Section headers
        
        # Fix common issues
        content = content.replace(' ,', ',')
        content = content.replace(' .', '.')
        content = content.strip()
        
        # Create cleaned document
        cleaned = document.copy()
        cleaned["content"] = content
        cleaned["content_cleaned"] = True
        cleaned["cleaned_timestamp"] = datetime.now().isoformat()
        
        return cleaned
    
    def _structure_document(self, document: Dict, doc_type: str) -> Dict:
        """
        Add structure and metadata to document.
        
        Args:
            document: Cleaned document
            doc_type: Type of document (biography, related_article)
            
        Returns:
            Structured document with metadata
        """
        structured = {
            "id": self._generate_doc_id(document),
            "type": doc_type,
            "title": document.get("title", "Unknown"),
            "source": {
                "url": document.get("url", ""),
                "wikipedia_page": document.get("title", ""),
                "collected": document.get("collection_timestamp", ""),
                "processed": datetime.now().isoformat()
            },
            "content": {
                "full_text": document.get("content", ""),
                "summary": document.get("summary", ""),
                "word_count": len(document.get("content", "").split()),
                "char_count": len(document.get("content", ""))
            },
            "metadata": {
                "persona": "Queen Elizabeth II",
                "time_period": self._determine_time_period(document),
                "content_category": self._categorize_content(document),
                "language": "English",
                "formality": "Formal"
            }
        }
        
        self.statistics["processed_documents"] += 1
        return structured
    
    def _generate_doc_id(self, document: Dict) -> str:
        """
        Generate unique document ID.
        
        Args:
            document: Document dictionary
            
        Returns:
            Unique ID string
        """
        title = document.get("title", "unknown")
        # Create ID from title
        doc_id = re.sub(r'[^\w\s-]', '', title.lower())
        doc_id = re.sub(r'[\s_]+', '_', doc_id)
        return f"qe2_{doc_id}"
    
    def _determine_time_period(self, document: Dict) -> str:
        """
        Determine the time period covered by document.
        
        Args:
            document: Document dictionary
            
        Returns:
            Time period label
        """
        title = document.get("title", "").lower()
        
        # Check for specific periods
        if "silver jubilee" in title or "1977" in title:
            return "1970s"
        elif "golden jubilee" in title or "2002" in title:
            return "2000s"
        elif "diamond jubilee" in title or "2012" in title:
            return "2010s"
        elif "platinum jubilee" in title or "2022" in title:
            return "2020s"
        elif "coronation" in title or "1952" in title or "1953" in title:
            return "1950s"
        elif "death" in title or "funeral" in title:
            return "2020s"
        elif "george vi" in title:
            return "1930s-1950s"
        elif "churchill" in title:
            return "1940s-1960s"
        elif "annus horribilis" in title or "1992" in title:
            return "1990s"
        else:
            return "1952-2022"  # Full reign
    
    def _categorize_content(self, document: Dict) -> str:
        """
        Categorize document content.
        
        Args:
            document: Document dictionary
            
        Returns:
            Content category
        """
        title = document.get("title", "").lower()
        
        if "elizabeth ii" in title and "death" not in title:
            return "biography"
        elif "jubilee" in title:
            return "celebration"
        elif "coronation" in title:
            return "ceremony"
        elif "death" in title or "funeral" in title:
            return "historical_event"
        elif "family" in title or "philip" in title or "george vi" in title:
            return "family"
        elif "christmas" in title:
            return "tradition"
        elif "commonwealth" in title:
            return "political"
        elif "jewels" in title or "flag" in title or "residences" in title:
            return "royal_symbols"
        elif "churchill" in title:
            return "political_figures"
        else:
            return "general"
    
    def _create_chunks(self, biography: Dict, articles: List[Dict]) -> List[Dict]:
        """
        Create training chunks from documents.
        
        Args:
            biography: Structured biography
            articles: List of structured articles
            
        Returns:
            List of chunk dictionaries
        """
        chunks = []
        
        # Chunk size parameters (in words)
        chunk_size = 500
        overlap = 100
        
        # Process biography
        bio_chunks = self._chunk_document(biography, chunk_size, overlap)
        chunks.extend(bio_chunks)
        print(f"  ✓ Created {len(bio_chunks)} chunks from biography")
        
        # Process each article
        for article in articles:
            article_chunks = self._chunk_document(article, chunk_size, overlap)
            chunks.extend(article_chunks)
        print(f"  ✓ Created {len(chunks) - len(bio_chunks)} chunks from articles")
        print(f"  ✓ Total chunks: {len(chunks)}")
        
        self.statistics["total_chunks"] = len(chunks)
        return chunks
    
    def _chunk_document(self, document: Dict, chunk_size: int, overlap: int) -> List[Dict]:
        """
        Split document into overlapping chunks.
        
        Args:
            document: Structured document
            chunk_size: Size of chunks in words
            overlap: Overlap between chunks in words
            
        Returns:
            List of chunk dictionaries
        """
        content = document["content"]["full_text"]
        words = content.split()
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_text = ' '.join(words[start:end])
            
            chunk = {
                "chunk_id": f"{document['id']}_chunk_{chunk_id}",
                "document_id": document["id"],
                "document_title": document["title"],
                "chunk_index": chunk_id,
                "content": chunk_text,
                "word_count": len(chunk_text.split()),
                "metadata": document["metadata"],
                "source": document["source"]
            }
            
            chunks.append(chunk)
            chunk_id += 1
            start += (chunk_size - overlap)
            
            if start >= len(words):
                break
        
        return chunks
    
    def _save_processed_data(self, biography: Dict, articles: List[Dict], chunks: List[Dict]):
        """
        Save processed data to files.
        
        Args:
            biography: Structured biography
            articles: List of structured articles
            chunks: List of chunks
        """
        # Save structured documents
        documents_file = self.processed_data_dir / "structured_documents.json"
        all_documents = [biography] + articles
        with open(documents_file, 'w', encoding='utf-8') as f:
            json.dump(all_documents, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved {len(all_documents)} structured documents to: {documents_file.name}")
        
        # Save chunks
        chunks_file = self.processed_data_dir / "training_chunks.json"
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved {len(chunks)} training chunks to: {chunks_file.name}")
        
        # Save metadata
        metadata = {
            "persona": "Queen Elizabeth II",
            "processing_date": datetime.now().isoformat(),
            "documents_count": len(all_documents),
            "chunks_count": len(chunks),
            "total_words": sum(doc["content"]["word_count"] for doc in all_documents),
            "average_chunk_size": sum(chunk["word_count"] for chunk in chunks) / len(chunks),
            "time_periods_covered": list(set(doc["metadata"]["time_period"] for doc in all_documents)),
            "content_categories": list(set(doc["metadata"]["content_category"] for doc in all_documents))
        }
        
        metadata_file = self.processed_data_dir / "dataset_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved dataset metadata to: {metadata_file.name}")
    
    def _generate_processing_report(self):
        """
        Generate and save processing report.
        """
        self.statistics["end_time"] = datetime.now().isoformat()
        
        report = {
            "processing_statistics": self.statistics,
            "output_files": {
                "structured_documents": "structured_documents.json",
                "training_chunks": "training_chunks.json",
                "dataset_metadata": "dataset_metadata.json"
            },
            "quality_metrics": {
                "documents_processed": self.statistics["processed_documents"],
                "chunks_created": self.statistics["total_chunks"],
                "average_chunk_size": "~500 words",
                "chunk_overlap": "100 words"
            }
        }
        
        report_file = self.processed_data_dir / "processing_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved processing report to: {report_file.name}")
        
        # Print summary
        print("\n" + "="*70)
        print("PROCESSING SUMMARY")
        print("="*70)
        print(f"Raw sources processed: {self.statistics['raw_sources']}")
        print(f"Structured documents: {self.statistics['processed_documents']}")
        print(f"Training chunks created: {self.statistics['total_chunks']}")
        print("="*70)


def main():
    """
    Main execution function.
    """
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    
    raw_data_dir = dataset_root / "datasets" / "queen_elizabeth_ii" / "raw_data"
    processed_data_dir = dataset_root / "datasets" / "queen_elizabeth_ii" / "processed_data"
    
    processor = QueenElizabethDataProcessor(
        str(raw_data_dir),
        str(processed_data_dir)
    )
    
    processor.process_all()


if __name__ == "__main__":
    main()
