"""
Queen Elizabeth II Wikipedia Data Collection

This script collects biographical and historical information about Queen Elizabeth II
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
from bs4 import BeautifulSoup


class QueenElizabethDataCollector:
    """
    Collector for Queen Elizabeth II biographical and historical data from Wikipedia.
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
        
        Uses improved disambiguation handling to ensure we get the correct
        Elizabeth II (1926-2022) page, not Elizabeth I (1533-1603).
        
        Returns:
            Dictionary containing biographical data
        """
        print("Collecting main biography from Wikipedia...")
        
        try:
            # Try multiple title variations to avoid disambiguation issues
            possible_titles = [
                "Elizabeth II of the United Kingdom",
                "Queen Elizabeth II",
                "Elizabeth II"
            ]
            
            page = None
            for title in possible_titles:
                try:
                    print(f"  - Trying: {title}")
                    test_page = wikipedia.page(title, auto_suggest=False)
                    # Validate this is Elizabeth II (1926-2022) not Elizabeth I (1533-1603)
                    if "1926" in test_page.content and ("2022" in test_page.content or "Elizabeth II" in test_page.title):
                        page = test_page
                        print(f"  ✓ Found correct page: {test_page.title}")
                        break
                except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
                    continue
            
            if page is None:
                print("  - Trying with auto_suggest enabled...")
                page = wikipedia.page("Elizabeth II", auto_suggest=True)
            
            # Validate the page is correct
            if "1533" in page.content[:1000] or ("Elizabeth I" in page.title and "Elizabeth II" not in page.title):
                raise ValueError(
                    f"Wrong page retrieved: {page.title}. "
                    "This appears to be Elizabeth I (1533-1603) instead of Elizabeth II (1926-2022)."
                )
            
            data = {
                "title": page.title,
                "url": page.url,
                "content": page.content,
                "summary": page.summary,
                "categories": page.categories,
                "sections": self._extract_sections(page),
                "references": page.references[:50],  # Limit references
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
        except ValueError as e:
            print(f"Error: {e}")
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
                
                print(f"    ✓ Collected {data['word_count']} words")
                
            except wikipedia.exceptions.PageError:
                print(f"    ✗ Page not found: {title}")
                self.collection_log.append({
                    "source": "Wikipedia Related Article",
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "status": "not_found"
                })
                continue
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"    ✗ Disambiguation needed for: {title}")
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
                print(f"    ✗ Error collecting {title}: {e}")
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
        
        # Save main biography
        biography_file = self.wikipedia_dir / "biography.json"
        with open(biography_file, 'w', encoding='utf-8') as f:
            json.dump(biography, f, ensure_ascii=False, indent=2)
        print(f"  - Saved biography to: {biography_file}")
        
        # Save related articles
        if related_articles:
            related_file = self.wikipedia_dir / "related_articles.json"
            with open(related_file, 'w', encoding='utf-8') as f:
                json.dump(related_articles, f, ensure_ascii=False, indent=2)
            print(f"  - Saved {len(related_articles)} related articles to: {related_file}")
        
        # Save collection log
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
        
        # Estimate tokens (approximately 1.3 words per token for English)
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
                "target_tokens": 75000,
                "current_tokens": estimated_tokens,
                "progress_percent": round((estimated_tokens / 75000) * 100, 2),
                "tokens_needed": max(0, 75000 - estimated_tokens)
            }
        }
        
        # Save summary
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
        print(f"\nProgress toward 75,000 token goal:")
        print(f"  Current: {summary['status']['current_tokens']:,} tokens")
        print(f"  Progress: {summary['status']['progress_percent']}%")
        print(f"  Remaining: {summary['status']['tokens_needed']:,} tokens")
        print("="*70)


def main():
    """
    Main execution function.
    """
    # Set output directory (3 levels up to datasets/)
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    output_dir = dataset_root / "datasets" / "queen_elizabeth_ii" / "raw_data"
    
    print("="*70)
    print("Queen Elizabeth II Data Collection - Wikipedia")
    print("="*70)
    print(f"Output directory: {output_dir}")
    print()
    
    # Initialize collector
    collector = QueenElizabethDataCollector(str(output_dir))
    
    # Collect main biography
    biography = collector.collect_main_biography()
    
    if not biography:
        print("Error: Failed to collect main biography. Exiting.")
        sys.exit(1)
    
    # Related articles to collect
    related_articles_titles = [
        "Coronation of Elizabeth II",
        "Death and state funeral of Elizabeth II",
        "Silver Jubilee of Elizabeth II",
        "Golden Jubilee of Elizabeth II",
        "Diamond Jubilee of Elizabeth II",
        "Platinum Jubilee of Elizabeth II",
        "Royal Christmas Message",
        "Personal flag of Queen Elizabeth II"
    ]
    
    # Collect related articles
    related_articles = collector.collect_related_articles(related_articles_titles)
    
    # Save all data
    collector.save_data(biography, related_articles)
    
    # Generate and print summary
    summary = collector.generate_summary_report(biography, related_articles)
    collector.print_summary(summary)
    
    print("\nData collection completed successfully!")
    print(f"Data saved to: {output_dir}")


if __name__ == "__main__":
    main()
