#!/usr/bin/env python3
"""
Collect Queen Elizabeth II's Christmas Broadcasts (1952-2021).
These annual speeches are a 70-year tradition and provide unique insight
into the Queen's thoughts, values, and perspective on world events.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import json
import time
import os
from datetime import datetime
import wikipedia


class QueenChristmasBroadcastCollector:
    """
    Collects Queen Elizabeth II's Christmas Broadcast speeches.
    """
    
    def __init__(self, output_dir):
        """
        Initialize the collector.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.broadcasts = []
        self.collection_log = []
    
    def collect_all(self):
        """
        Main collection method.
        """
        print("=" * 80)
        print("Queen Elizabeth II - Christmas Broadcasts Collection")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Define articles to collect
        articles_to_collect = [
            {
                'title': 'Royal Christmas Message',
                'description': 'Overview and history of Christmas broadcasts',
                'category': 'tradition'
            },
            {
                'title': 'Elizabeth II',
                'description': 'Main biography (check for speech excerpts)',
                'category': 'biography'
            },
            {
                'title': 'Queen Elizabeth II Christmas Broadcasts',
                'description': 'Dedicated article on broadcasts',
                'category': 'speeches'
            }
        ]
        
        # Try to collect articles about Christmas broadcasts
        print(f"Collecting {len(articles_to_collect)} Wikipedia articles about Christmas broadcasts...")
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
            time.sleep(1)
        
        # Collect major historical speeches
        print("\nCollecting major historical speeches...")
        self._collect_major_speeches()
        
        # Save all data
        print("\nSaving collected data...")
        self._save_all_data()
        
        print("\n" + "=" * 80)
        print("Collection Complete!")
        print("=" * 80)
    
    def _collect_article(self, title, description, category):
        """
        Collect a single Wikipedia article.
        """
        try:
            wikipedia.set_lang('en')
            page = wikipedia.page(title, auto_suggest=False)
            
            article_data = {
                'id': f"queen_speech_{len(self.broadcasts) + 1}",
                'title': page.title,
                'original_title': title,
                'description': description,
                'category': category,
                'url': page.url,
                'content': page.content,
                'summary': page.summary,
                'word_count': len(page.content.split()),
                'char_count': len(page.content),
                'collected': datetime.now().isoformat()
            }
            
            self.broadcasts.append(article_data)
            
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
    
    def _collect_major_speeches(self):
        """
        Collect articles about major historical speeches.
        """
        major_speeches = [
            {
                'title': '1947 Elizabeth II 21st birthday speech',
                'year': 1947,
                'description': 'Dedication speech from South Africa'
            },
            {
                'title': '1997 Diana Princess of Wales death',
                'year': 1997,
                'description': 'Speech after Diana\'s death'
            },
            {
                'title': '2002 Golden Jubilee of Elizabeth II',
                'year': 2002,
                'description': '50th anniversary celebration'
            },
            {
                'title': '2012 Diamond Jubilee of Elizabeth II',
                'year': 2012,
                'description': '60th anniversary celebration'
            },
            {
                'title': '2020 coronavirus pandemic in the United Kingdom',
                'year': 2020,
                'description': 'COVID-19 crisis speech'
            },
            {
                'title': '2022 Platinum Jubilee of Elizabeth II',
                'year': 2022,
                'description': '70th anniversary celebration'
            }
        ]
        
        for i, speech_info in enumerate(major_speeches, 1):
            print(f"{i}/{len(major_speeches)}: {speech_info['year']} - {speech_info['description']}")
            
            success = self._collect_article(
                speech_info['title'],
                speech_info['description'],
                'major_speech'
            )
            
            if success:
                print(f"  ✓ Collected")
            else:
                print(f"  ✗ Failed")
            
            print()
            time.sleep(1)
    
    def _save_all_data(self):
        """
        Save all collected data to JSON files.
        """
        # Save broadcasts
        broadcasts_file = os.path.join(self.output_dir, 'christmas_broadcasts_and_speeches.json')
        with open(broadcasts_file, 'w', encoding='utf-8') as f:
            json.dump(self.broadcasts, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: christmas_broadcasts_and_speeches.json ({len(self.broadcasts)} articles)")
        
        # Save collection log
        log_file = os.path.join(self.output_dir, 'collection_log.json')
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.collection_log, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: collection_log.json")
        
        # Generate summary
        summary = {
            'collection_date': datetime.now().isoformat(),
            'person': 'Queen Elizabeth II',
            'content_type': 'Christmas Broadcasts and Major Speeches',
            'total_articles': len(self.broadcasts),
            'successful_collections': len([log for log in self.collection_log if log['status'] == 'success']),
            'failed_collections': len([log for log in self.collection_log if log['status'] != 'success']),
            'total_words': sum(article['word_count'] for article in self.broadcasts),
            'total_characters': sum(article['char_count'] for article in self.broadcasts),
            'estimated_tokens': int(sum(article['char_count'] for article in self.broadcasts) * 1.1),
            'articles_by_title': [article['title'] for article in self.broadcasts]
        }
        
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
        print(f"Estimated tokens: {summary['estimated_tokens']:,}")
        print()
        print("Articles collected:")
        for title in summary['articles_by_title']:
            print(f"  - {title}")
        print("=" * 80)


def main():
    """Main execution function."""
    
    # Configuration
    output_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/queen_elizabeth_ii/raw_data/speeches_supplement"
    
    # Create collector
    collector = QueenChristmasBroadcastCollector(output_dir)
    
    # Collect all data
    collector.collect_all()


if __name__ == "__main__":
    main()
