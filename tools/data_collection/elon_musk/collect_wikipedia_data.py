"""
Elon Musk Wikipedia Data Collection

This script collects biographical and career information about Elon Musk
from Wikipedia using the Wikipedia API.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import wikipedia


class ElonMuskDataCollector:
    """
    Collector for Elon Musk biographical and career data from Wikipedia.
    """
    
    def __init__(self, output_dir: str):
        """
        Initialize the collector.
        
        Args:
            output_dir: Directory to save collected data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.wikipedia_dir = self.output_dir / "wikipedia"
        self.wikipedia_dir.mkdir(exist_ok=True)
        
        self.metadata_dir = self.output_dir / "metadata"
        self.metadata_dir.mkdir(exist_ok=True)
        
        self.collection_log = []
        
    def collect_main_biography(self) -> Dict:
        """
        Collect main biographical information from the primary Wikipedia article.
        
        Returns:
            Dictionary containing biographical data
        """
        print("Collecting main biography from Wikipedia...")
        
        try:
            page = wikipedia.page("Elon Musk", auto_suggest=False)
            
            data = {
                "title": page.title,
                "url": page.url,
                "content": page.content,
                "summary": page.summary,
                "categories": page.categories,
                "sections": self._extract_sections(page),
                "references": page.references[:100],
                "collection_timestamp": datetime.now().isoformat(),
                "word_count": len(page.content.split()),
                "character_count": len(page.content)
            }
            
            self.collection_log.append({
                "source": "Wikipedia Main Article",
                "title": page.title,
                "url": page.url,
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "word_count": data["word_count"]
            })
            
            print(f"  - Collected {data['word_count']} words from main biography")
            return data
            
        except wikipedia.exceptions.PageError as e:
            print(f"Error: Page not found - {e}")
            self.collection_log.append({
                "source": "Wikipedia Main Article",
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            })
            return {}
        except Exception as e:
            print(f"Error collecting main biography: {e}")
            self.collection_log.append({
                "source": "Wikipedia Main Article",
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            })
            return {}
    
    def collect_related_articles(self, article_titles: List[str]) -> List[Dict]:
        """
        Collect data from related Wikipedia articles.
        
        Args:
            article_titles: List of article titles to collect
            
        Returns:
            List of dictionaries containing article data
        """
        print(f"\nCollecting {len(article_titles)} related articles...")
        
        collected_articles = []
        
        for title in article_titles:
            try:
                print(f"  - Collecting: {title}")
                page = wikipedia.page(title)
                
                data = {
                    "title": page.title,
                    "url": page.url,
                    "content": page.content,
                    "summary": page.summary,
                    "collection_timestamp": datetime.now().isoformat(),
                    "word_count": len(page.content.split())
                }
                
                collected_articles.append(data)
                
                self.collection_log.append({
                    "source": "Wikipedia Related Article",
                    "title": page.title,
                    "url": page.url,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "word_count": data["word_count"]
                })
                
                print(f"    Collected {data['word_count']} words")
                
            except wikipedia.exceptions.PageError:
                print(f"    Page not found: {title}")
                self.collection_log.append({
                    "source": "Wikipedia Related Article",
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "status": "not_found"
                })
                continue
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"    Disambiguation needed for: {title}")
                print(f"      Options: {e.options[:5]}")
                self.collection_log.append({
                    "source": "Wikipedia Related Article",
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "status": "disambiguation",
                    "options": e.options[:10]
                })
                continue
            except Exception as e:
                print(f"    Error collecting {title}: {e}")
                self.collection_log.append({
                    "source": "Wikipedia Related Article",
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "status": "error",
                    "error": str(e)
                })
                continue
        
        return collected_articles
    
    def _extract_sections(self, page) -> Dict[str, str]:
        """
        Extract content by section from Wikipedia page.
        
        Args:
            page: Wikipedia page object
            
        Returns:
            Dictionary mapping section titles to content
        """
        sections = {}
        content_lines = page.content.split('\n')
        current_section = "Introduction"
        current_content = []
        
        for line in content_lines:
            if line.startswith('== ') and line.endswith(' =='):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip('= ')
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def save_data(self, biography: Dict, related_articles: List[Dict]):
        """
        Save collected data to JSON files.
        
        Args:
            biography: Main biography data
            related_articles: List of related article data
        """
        print("\nSaving collected data...")
        
        biography_file = self.wikipedia_dir / "biography.json"
        with open(biography_file, 'w', encoding='utf-8') as f:
            json.dump(biography, f, ensure_ascii=False, indent=2)
        print(f"  - Saved biography to: {biography_file}")
        
        if related_articles:
            related_file = self.wikipedia_dir / "related_articles.json"
            with open(related_file, 'w', encoding='utf-8') as f:
                json.dump(related_articles, f, ensure_ascii=False, indent=2)
            print(f"  - Saved {len(related_articles)} related articles to: {related_file}")
        
        log_file = self.metadata_dir / "collection_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                "collection_date": datetime.now().isoformat(),
                "total_items": len(self.collection_log),
                "items": self.collection_log
            }, f, ensure_ascii=False, indent=2)
        print(f"  - Saved collection log to: {log_file}")
    
    def generate_summary_report(self, biography: Dict, related_articles: List[Dict]) -> Dict:
        """
        Generate summary statistics for collected data.
        
        Args:
            biography: Main biography data
            related_articles: List of related article data
            
        Returns:
            Dictionary containing summary statistics
        """
        total_words = biography.get("word_count", 0)
        total_words += sum(article.get("word_count", 0) for article in related_articles)
        
        total_chars = biography.get("character_count", 0)
        total_chars += sum(len(article.get("content", "")) for article in related_articles)
        
        estimated_tokens = int(total_words / 1.3)
        
        summary = {
            "collection_date": datetime.now().isoformat(),
            "total_sources": 1 + len(related_articles),
            "main_biography": {
                "words": biography.get("word_count", 0),
                "characters": biography.get("character_count", 0)
            },
            "related_articles": {
                "count": len(related_articles),
                "total_words": sum(article.get("word_count", 0) for article in related_articles)
            },
            "totals": {
                "words": total_words,
                "characters": total_chars,
                "estimated_tokens": estimated_tokens
            },
            "status": {
                "target_tokens": 100000,
                "current_tokens": estimated_tokens,
                "progress_percent": round((estimated_tokens / 100000) * 100, 2),
                "tokens_needed": max(0, 100000 - estimated_tokens)
            }
        }
        
        summary_file = self.metadata_dir / "collection_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        return summary
    
    def print_summary(self, summary: Dict):
        """
        Print collection summary to console.
        
        Args:
            summary: Summary statistics dictionary
        """
        print("\n" + "="*70)
        print("COLLECTION SUMMARY")
        print("="*70)
        print(f"Total Sources Collected: {summary['total_sources']}")
        print(f"Total Words: {summary['totals']['words']:,}")
        print(f"Estimated Tokens: {summary['totals']['estimated_tokens']:,}")
        print(f"\nProgress toward 100,000 token goal:")
        print(f"  Current: {summary['status']['current_tokens']:,} tokens")
        print(f"  Progress: {summary['status']['progress_percent']}%")
        print(f"  Remaining: {summary['status']['tokens_needed']:,} tokens")
        print("="*70)


def main():
    """
    Main execution function.
    """
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    output_dir = dataset_root / "datasets" / "elon_musk" / "raw_data"
    
    print("="*70)
    print("Elon Musk Data Collection - Wikipedia")
    print("="*70)
    print(f"Output directory: {output_dir}")
    print()
    
    collector = ElonMuskDataCollector(str(output_dir))
    
    biography = collector.collect_main_biography()
    
    if not biography:
        print("Error: Failed to collect main biography. Exiting.")
        sys.exit(1)
    
    related_articles_titles = [
        "Tesla, Inc.",
        "SpaceX",
        "PayPal",
        "Neuralink",
        "The Boring Company",
        "X Corp.",
        "SolarCity",
        "Hyperloop",
        "Starlink",
        "Tesla Roadster (first generation)",
        "Tesla Model S",
        "Falcon 9",
        "Starship (spacecraft)",
        "Mars colonization"
    ]
    
    related_articles = collector.collect_related_articles(related_articles_titles)
    
    collector.save_data(biography, related_articles)
    
    summary = collector.generate_summary_report(biography, related_articles)
    collector.print_summary(summary)
    
    print("\nData collection completed successfully!")
    print(f"Data saved to: {output_dir}")


if __name__ == "__main__":
    main()
