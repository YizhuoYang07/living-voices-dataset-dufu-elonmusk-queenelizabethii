#!/usr/bin/env python3
"""
Collect supplementary data about Du Fu from Wikipedia using wikipedia library.
This script gathers biographical, historical, and cultural context
that complements the existing poetry corpus.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import wikipedia
import json
import time
from datetime import datetime
import os


class DuFuWikipediaCollector:
    """
    Collects supplementary information about Du Fu from Wikipedia.
    Focuses on biographical, historical, and cultural context.
    """
    
    def __init__(self, output_dir):
        """
        Initialize the collector.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Storage for collected data
        self.wikipedia_articles = []
        self.collection_log = []
    
    def collect_all(self):
        """
        Main collection method - gather all supplementary data.
        """
        print("=" * 80)
        print("Du Fu Wikipedia Supplementary Data Collection")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Define articles to collect
        articles_to_collect = [
            {
                'title': 'Du Fu',
                'description': 'Main biographical article',
                'category': 'biography'
            },
            {
                'title': 'Tang Dynasty',
                'description': 'Historical period (618-907 CE)',
                'category': 'history'
            },
            {
                'title': 'An Lushan Rebellion',
                'description': 'Major historical event (755-763 CE)',
                'category': 'history'
            },
            {
                'title': 'Chinese poetry',
                'description': 'Literary tradition overview',
                'category': 'literature'
            },
            {
                'title': 'Classical Chinese poetry',
                'description': 'Classical poetry forms',
                'category': 'literature'
            },
            {
                'title': 'Tang poetry',
                'description': 'Tang Dynasty poetry tradition',
                'category': 'literature'
            },
            {
                'title': 'Li Bai',
                'description': 'Contemporary poet (701-762 CE)',
                'category': 'biography'
            },
            {
                'title': 'Wang Wei (Tang dynasty)',
                'description': 'Contemporary poet (699-759 CE)',
                'category': 'biography'
            },
            {
                'title': 'Regulated verse',
                'description': 'Poetry form (Lüshi 律詩)',
                'category': 'literature'
            },
            {
                'title': 'Chengdu',
                'description': "Major city in Du Fu's life",
                'category': 'geography'
            },
            {
                'title': "Chang'an",
                'description': 'Tang Dynasty capital',
                'category': 'geography'
            },
            {
                'title': 'Confucianism',
                'description': 'Philosophical influence',
                'category': 'philosophy'
            },
            {
                'title': 'Buddhism in China',
                'description': 'Religious context',
                'category': 'philosophy'
            },
            {
                'title': 'Taoism',
                'description': 'Philosophical and religious tradition',
                'category': 'philosophy'
            }
        ]
        
        print(f"Collecting {len(articles_to_collect)} Wikipedia articles...")
        print()
        
        for i, article_info in enumerate(articles_to_collect, 1):
            print(f"{i}/{len(articles_to_collect)}: {article_info['title']}")
            print(f"  Description: {article_info['description']}")
            
            success = self._collect_article(
                article_info['title'],
                article_info['description'],
                article_info['category']
            )
            
            if success:
                print(f"  ✓ Collected successfully")
            else:
                print(f"  ✗ Failed to collect")
            
            print()
            time.sleep(1)  # Rate limiting
        
        # Save all data
        print("Saving collected data...")
        self._save_all_data()
        
        print("\n" + "=" * 80)
        print("Collection Complete!")
        print("=" * 80)
    
    def _collect_article(self, title, description, category):
        """
        Collect a single Wikipedia article.
        
        Args:
            title: Article title
            description: Article description
            category: Article category
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Set language to English
            wikipedia.set_lang('en')
            
            # Get page
            page = wikipedia.page(title, auto_suggest=False)
            
            # Extract information
            article_data = {
                'id': f"dufu_wiki_{len(self.wikipedia_articles) + 1}",
                'title': page.title,
                'original_title': title,
                'description': description,
                'category': category,
                'url': page.url,
                'content': page.content,
                'summary': page.summary,
                'word_count': len(page.content.split()),
                'char_count': len(page.content),
                'sections': page.sections if hasattr(page, 'sections') else [],
                'collected': datetime.now().isoformat()
            }
            
            self.wikipedia_articles.append(article_data)
            
            # Log success
            self.collection_log.append({
                'title': title,
                'status': 'success',
                'word_count': article_data['word_count'],
                'timestamp': datetime.now().isoformat()
            })
            
            return True
            
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"  Warning: Disambiguation page. Options: {e.options[:5]}")
            self.collection_log.append({
                'title': title,
                'status': 'disambiguation',
                'options': e.options[:10],
                'timestamp': datetime.now().isoformat()
            })
            return False
            
        except wikipedia.exceptions.PageError:
            print(f"  Error: Page not found")
            self.collection_log.append({
                'title': title,
                'status': 'not_found',
                'timestamp': datetime.now().isoformat()
            })
            return False
            
        except Exception as e:
            print(f"  Error: {type(e).__name__}: {e}")
            self.collection_log.append({
                'title': title,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def _save_all_data(self):
        """
        Save all collected data to JSON files.
        """
        # Save main articles
        articles_file = os.path.join(self.output_dir, 'wikipedia_articles.json')
        with open(articles_file, 'w', encoding='utf-8') as f:
            json.dump(self.wikipedia_articles, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: wikipedia_articles.json ({len(self.wikipedia_articles)} articles)")
        
        # Save collection log
        log_file = os.path.join(self.output_dir, 'collection_log.json')
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.collection_log, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: collection_log.json")
        
        # Generate summary
        summary = {
            'collection_date': datetime.now().isoformat(),
            'author': 'Du Fu (杜甫)',
            'total_articles': len(self.wikipedia_articles),
            'successful_collections': len([log for log in self.collection_log if log['status'] == 'success']),
            'failed_collections': len([log for log in self.collection_log if log['status'] != 'success']),
            'total_words': sum(article['word_count'] for article in self.wikipedia_articles),
            'total_characters': sum(article['char_count'] for article in self.wikipedia_articles),
            'categories': {},
            'articles_by_title': [article['title'] for article in self.wikipedia_articles]
        }
        
        # Count by category
        for article in self.wikipedia_articles:
            category = article['category']
            if category not in summary['categories']:
                summary['categories'][category] = {
                    'count': 0,
                    'total_words': 0
                }
            summary['categories'][category]['count'] += 1
            summary['categories'][category]['total_words'] += article['word_count']
        
        summary_file = os.path.join(self.output_dir, 'collection_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: collection_summary.json")
        
        # Print summary
        print()
        print("=" * 80)
        print("Collection Summary")
        print("=" * 80)
        print(f"Articles collected: {summary['total_articles']}")
        print(f"Successful: {summary['successful_collections']}")
        print(f"Failed: {summary['failed_collections']}")
        print(f"Total words: {summary['total_words']:,}")
        print(f"Total characters: {summary['total_characters']:,}")
        print()
        print("By category:")
        for category, stats in summary['categories'].items():
            print(f"  {category}: {stats['count']} articles, {stats['total_words']:,} words")
        print()
        print("Articles collected:")
        for title in summary['articles_by_title']:
            print(f"  - {title}")
        print("=" * 80)


def main():
    """Main execution function."""
    
    # Configuration
    output_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/du_fu/raw_data/wikipedia_supplement"
    
    # Create collector
    collector = DuFuWikipediaCollector(output_dir)
    
    # Collect all supplementary data
    collector.collect_all()


if __name__ == "__main__":
    main()
