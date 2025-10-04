"""
Elon Musk Additional Wikipedia Data Collection

This script collects supplementary biographical and company information 
about Elon Musk from additional Wikipedia articles to reach the 100K token target.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import wikipedia


class AdditionalDataCollector:
    """
    Collector for additional Elon Musk related articles from Wikipedia.
    """
    
    def __init__(self, raw_data_dir: str):
        """
        Initialize the collector.
        
        Args:
            raw_data_dir: Directory containing existing raw data
        """
        self.raw_data_dir = Path(raw_data_dir)
        self.wikipedia_dir = self.raw_data_dir / "wikipedia"
        self.metadata_dir = self.raw_data_dir / "metadata"
        
        self.collection_log = []
        
    def load_existing_data(self) -> Dict:
        """
        Load existing collection summary.
        
        Returns:
            Dictionary with current collection statistics
        """
        summary_file = self.metadata_dir / "collection_summary.json"
        
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def collect_articles(self, article_titles: List[str]) -> List[Dict]:
        """
        Collect data from additional Wikipedia articles.
        
        Args:
            article_titles: List of article titles to collect
            
        Returns:
            List of dictionaries containing article data
        """
        print(f"Collecting {len(article_titles)} additional articles...")
        
        collected_articles = []
        
        for title in article_titles:
            try:
                print(f"  - Collecting: {title}")
                page = wikipedia.page(title, auto_suggest=False)
                
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
                    "source": "Wikipedia Additional Article",
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
                    "source": "Wikipedia Additional Article",
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "status": "not_found"
                })
                continue
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"    Disambiguation needed for: {title}")
                print(f"      Options: {e.options[:5]}")
                
                if e.options:
                    try:
                        print(f"      Trying first option: {e.options[0]}")
                        page = wikipedia.page(e.options[0], auto_suggest=False)
                        
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
                            "source": "Wikipedia Additional Article",
                            "title": page.title,
                            "url": page.url,
                            "timestamp": datetime.now().isoformat(),
                            "status": "success",
                            "word_count": data["word_count"]
                        })
                        print(f"    Collected {data['word_count']} words")
                    except Exception as e2:
                        print(f"      Failed: {e2}")
                        continue
                        
            except Exception as e:
                print(f"    Error collecting {title}: {e}")
                self.collection_log.append({
                    "source": "Wikipedia Additional Article",
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "status": "error",
                    "error": str(e)
                })
                continue
        
        return collected_articles
    
    def merge_and_save(self, new_articles: List[Dict]):
        """
        Merge new articles with existing collection and save.
        
        Args:
            new_articles: List of newly collected articles
        """
        print("\nMerging with existing data...")
        
        existing_file = self.wikipedia_dir / "related_articles.json"
        
        if existing_file.exists():
            with open(existing_file, 'r', encoding='utf-8') as f:
                existing_articles = json.load(f)
        else:
            existing_articles = []
        
        merged_articles = existing_articles + new_articles
        
        with open(existing_file, 'w', encoding='utf-8') as f:
            json.dump(merged_articles, f, ensure_ascii=False, indent=2)
        
        print(f"  - Saved {len(merged_articles)} total related articles")
        
        log_file = self.metadata_dir / "collection_log.json"
        with open(log_file, 'r', encoding='utf-8') as f:
            existing_log = json.load(f)
        
        existing_log["items"].extend(self.collection_log)
        existing_log["total_items"] = len(existing_log["items"])
        existing_log["last_updated"] = datetime.now().isoformat()
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(existing_log, f, ensure_ascii=False, indent=2)
        
        print(f"  - Updated collection log")
    
    def update_summary(self) -> Dict:
        """
        Recalculate and update summary statistics.
        
        Returns:
            Updated summary dictionary
        """
        biography_file = self.wikipedia_dir / "biography.json"
        with open(biography_file, 'r', encoding='utf-8') as f:
            biography = json.load(f)
        
        related_file = self.wikipedia_dir / "related_articles.json"
        with open(related_file, 'r', encoding='utf-8') as f:
            related_articles = json.load(f)
        
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
        Print updated collection summary.
        
        Args:
            summary: Summary statistics dictionary
        """
        print("\n" + "="*70)
        print("UPDATED COLLECTION SUMMARY")
        print("="*70)
        print(f"Total Sources: {summary['total_sources']}")
        print(f"Total Words: {summary['totals']['words']:,}")
        print(f"Estimated Tokens: {summary['totals']['estimated_tokens']:,}")
        print(f"\nProgress toward 100,000 token goal:")
        print(f"  Current: {summary['status']['current_tokens']:,} tokens")
        print(f"  Progress: {summary['status']['progress_percent']}%")
        print(f"  Remaining: {summary['status']['tokens_needed']:,} tokens")
        
        if summary['status']['current_tokens'] >= 100000:
            print(f"\n  ✓ TARGET ACHIEVED!")
        
        print("="*70)


def main():
    """
    Main execution function.
    """
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    raw_data_dir = dataset_root / "datasets" / "elon_musk" / "raw_data"
    
    print("="*70)
    print("Elon Musk Additional Data Collection - Wikipedia")
    print("="*70)
    
    collector = AdditionalDataCollector(str(raw_data_dir))
    
    existing_summary = collector.load_existing_data()
    if existing_summary:
        current_tokens = existing_summary.get("status", {}).get("current_tokens", 0)
        print(f"Current collection: {current_tokens:,} tokens")
        print(f"Target: 100,000 tokens")
        print(f"Needed: {max(0, 100000 - current_tokens):,} tokens\n")
    
    additional_articles = [
        "X.com",
        "Zip2",
        "Tesla Autopilot",
        "Tesla Cybertruck",
        "Tesla Gigafactory",
        "Falcon Heavy",
        "Dragon 2",
        "SpaceX Starship",
        "Crew Dragon Demo-2",
        "OpenAI",
        "Artificial intelligence",
        "Electric vehicle",
        "Sustainable energy",
        "Commercial spaceflight",
        "Private spaceflight",
        "Mars Society"
    ]
    
    new_articles = collector.collect_articles(additional_articles)
    
    if new_articles:
        collector.merge_and_save(new_articles)
        summary = collector.update_summary()
        collector.print_summary(summary)
    else:
        print("\nNo new articles collected.")
    
    print("\nAdditional data collection completed!")


if __name__ == "__main__":
    main()
