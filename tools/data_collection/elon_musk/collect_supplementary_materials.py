#!/usr/bin/env python3
"""
Collect Elon Musk supplementary materials:
- Key speeches and interviews
- Important public statements
- Technical writings and presentations

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import json
import time
import os
from datetime import datetime
import wikipedia


class ElonMuskSupplementCollector:
    """
    Collects supplementary materials about Elon Musk.
    """
    
    def __init__(self, output_dir):
        """
        Initialize the collector.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.materials = []
        self.collection_log = []
    
    def collect_all(self):
        """
        Main collection method.
        """
        print("=" * 80)
        print("Elon Musk - Supplementary Materials Collection")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Define articles to collect
        articles_to_collect = [
            # Company deep dives
            {
                'title': 'SpaceX Starship',
                'description': 'Mars rocket project details',
                'category': 'spacex'
            },
            {
                'title': 'SpaceX Falcon 9',
                'description': 'Reusable rocket technology',
                'category': 'spacex'
            },
            {
                'title': 'Tesla Autopilot',
                'description': 'Autonomous driving technology',
                'category': 'tesla'
            },
            {
                'title': 'Tesla Model S',
                'description': 'Flagship electric vehicle',
                'category': 'tesla'
            },
            {
                'title': 'Tesla Model 3',
                'description': 'Mass market electric vehicle',
                'category': 'tesla'
            },
            {
                'title': 'Tesla Gigafactory',
                'description': 'Battery manufacturing facilities',
                'category': 'tesla'
            },
            {
                'title': 'Neuralink',
                'description': 'Brain-computer interface company',
                'category': 'neuralink'
            },
            {
                'title': 'The Boring Company',
                'description': 'Tunnel construction company',
                'category': 'boring'
            },
            
            # Business events
            {
                'title': 'Acquisition of Twitter by Elon Musk',
                'description': 'Twitter/X acquisition 2022',
                'category': 'twitter'
            },
            {
                'title': 'Elon Musk\'s Tesla SEC settlement',
                'description': 'SEC lawsuit and settlement',
                'category': 'controversy'
            },
            
            # Interviews and media
            {
                'title': 'The Joe Rogan Experience',
                'description': 'Popular podcast (Musk appearances)',
                'category': 'interview'
            },
            {
                'title': 'TED (conference)',
                'description': 'TED talks platform (context)',
                'category': 'interview'
            },
            
            # Concepts and philosophy
            {
                'title': 'First principles',
                'description': 'Thinking methodology',
                'category': 'philosophy'
            },
            {
                'title': 'Mars colonization',
                'description': 'Multi-planetary species vision',
                'category': 'vision'
            },
            {
                'title': 'Sustainable energy',
                'description': 'Energy transition vision',
                'category': 'vision'
            },
            {
                'title': 'Artificial general intelligence',
                'description': 'AI development and safety',
                'category': 'ai'
            },
            
            # Comparisons and context
            {
                'title': 'Jeff Bezos',
                'description': 'Amazon founder and space competitor',
                'category': 'context'
            },
            {
                'title': 'Richard Branson',
                'description': 'Virgin Galactic founder',
                'category': 'context'
            },
            {
                'title': 'Steve Jobs',
                'description': 'Apple founder (comparison)',
                'category': 'context'
            },
            
            # Technical deep dives
            {
                'title': 'Electric battery',
                'description': 'Battery technology details',
                'category': 'technology'
            },
            {
                'title': 'Rocket reusability',
                'description': 'Reusable rocket technology',
                'category': 'technology'
            },
            {
                'title': 'Autonomous driving',
                'description': 'Self-driving technology',
                'category': 'technology'
            },
            
            # Business and innovation
            {
                'title': 'Vertical integration',
                'description': 'Business strategy',
                'category': 'strategy'
            },
            {
                'title': 'Innovation',
                'description': 'Innovation theory and practice',
                'category': 'strategy'
            },
            {
                'title': 'Disruptive innovation',
                'description': 'Market disruption theory',
                'category': 'strategy'
            }
        ]
        
        print(f"Collecting {len(articles_to_collect)} supplementary articles...")
        print()
        
        for i, article_info in enumerate(articles_to_collect, 1):
            print(f"{i}/{len(articles_to_collect)}: {article_info['title']}")
            print(f"  Category: {article_info['category']}")
            
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
        
        # Save all data
        print("Saving collected data...")
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
                'id': f"musk_supplement_{len(self.materials) + 1}",
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
            
            self.materials.append(article_data)
            
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
        # Save materials
        materials_file = os.path.join(self.output_dir, 'supplementary_materials.json')
        with open(materials_file, 'w', encoding='utf-8') as f:
            json.dump(self.materials, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: supplementary_materials.json ({len(self.materials)} articles)")
        
        # Save collection log
        log_file = os.path.join(self.output_dir, 'collection_log.json')
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.collection_log, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved: collection_log.json")
        
        # Generate summary
        summary = {
            'collection_date': datetime.now().isoformat(),
            'person': 'Elon Musk',
            'content_type': 'Supplementary Materials (Companies, Technology, Philosophy)',
            'total_articles': len(self.materials),
            'successful_collections': len([log for log in self.collection_log if log['status'] == 'success']),
            'failed_collections': len([log for log in self.collection_log if log['status'] != 'success']),
            'total_words': sum(article['word_count'] for article in self.materials),
            'total_characters': sum(article['char_count'] for article in self.materials),
            'estimated_tokens': int(sum(article['char_count'] for article in self.materials) * 1.1),
            'categories': {},
            'articles_by_title': [article['title'] for article in self.materials]
        }
        
        # Count by category
        for article in self.materials:
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
        print(f"Estimated tokens: {summary['estimated_tokens']:,}")
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
    output_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/elon_musk/raw_data/supplementary_materials"
    
    # Create collector
    collector = ElonMuskSupplementCollector(output_dir)
    
    # Collect all data
    collector.collect_all()


if __name__ == "__main__":
    main()
