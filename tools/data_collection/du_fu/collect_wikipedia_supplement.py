#!/usr/bin/env python3
"""
Collect supplementary data about Du Fu from Wikipedia and Wikidata.
This script gathers biographical, historical, and cultural context
that complements the existing poetry corpus.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import requests
import json
import time
from datetime import datetime
import os


class DuFuWikipediaCollector:
    """
    Collects supplementary information about Du Fu from Wikipedia and Wikidata.
    Focuses on biographical, historical, and cultural context.
    """
    
    def __init__(self, output_dir):
        """
        Initialize the collector.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        self.wikipedia_base = "https://en.wikipedia.org/w/api.php"
        self.wikidata_base = "https://www.wikidata.org/w/api.php"
        
        # Du Fu's Wikidata ID
        self.du_fu_qid = "Q36014"
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Storage for collected data
        self.wikipedia_data = {}
        self.wikidata_data = {}
        self.related_articles = []
    
    def collect_all(self):
        """
        Main collection method - gather all supplementary data.
        """
        print("=" * 80)
        print("Du Fu Wikipedia & Wikidata Supplementary Data Collection")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print()
        
        # Step 1: Collect Wikipedia articles
        print("Step 1: Collecting Wikipedia articles...")
        self._collect_wikipedia_articles()
        
        # Step 2: Collect Wikidata information
        print("\nStep 2: Collecting Wikidata information...")
        self._collect_wikidata_info()
        
        # Step 3: Collect related articles
        print("\nStep 3: Collecting related articles...")
        self._collect_related_articles()
        
        # Step 4: Save all data
        print("\nStep 4: Saving collected data...")
        self._save_all_data()
        
        print("\n" + "=" * 80)
        print("Collection Complete!")
        print("=" * 80)
    
    def _collect_wikipedia_articles(self):
        """
        Collect Wikipedia articles about Du Fu in multiple languages.
        """
        articles_to_collect = [
            {
                'lang': 'en',
                'title': 'Du Fu',
                'description': 'Main English article about Du Fu'
            },
            {
                'lang': 'zh',
                'title': '杜甫',
                'description': 'Main Chinese article about Du Fu'
            }
        ]
        
        for article in articles_to_collect:
            print(f"  Collecting: {article['title']} ({article['lang']})")
            
            # Get article content
            content = self._get_wikipedia_article(article['lang'], article['title'])
            
            if content:
                self.wikipedia_data[f"{article['lang']}_{article['title']}"] = {
                    'language': article['lang'],
                    'title': article['title'],
                    'description': article['description'],
                    'content': content,
                    'collected': datetime.now().isoformat()
                }
                print(f"    ✓ Collected: {len(content)} characters")
            else:
                print(f"    ✗ Failed to collect")
            
            time.sleep(1)  # Rate limiting
    
    def _get_wikipedia_article(self, lang, title):
        """
        Get a Wikipedia article's full text.
        
        Args:
            lang: Language code (e.g., 'en', 'zh')
            title: Article title
            
        Returns:
            Article text or None if failed
        """
        try:
            base_url = f"https://{lang}.wikipedia.org/w/api.php"
            
            params = {
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'extracts',
                'explaintext': True,
                'exsectionformat': 'plain'
            }
            
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get('query', {}).get('pages', {})
            
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    return page_data.get('extract', '')
            
            return None
            
        except Exception as e:
            print(f"    Error: {e}")
            return None
    
    def _collect_wikidata_info(self):
        """
        Collect structured data from Wikidata about Du Fu.
        """
        print(f"  Querying Wikidata for Q36014 (Du Fu)...")
        
        try:
            params = {
                'action': 'wbgetentities',
                'ids': self.du_fu_qid,
                'format': 'json',
                'languages': 'en|zh'
            }
            
            response = requests.get(self.wikidata_base, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            entity = data.get('entities', {}).get(self.du_fu_qid, {})
            
            # Extract relevant information
            self.wikidata_data = {
                'qid': self.du_fu_qid,
                'labels': entity.get('labels', {}),
                'descriptions': entity.get('descriptions', {}),
                'aliases': entity.get('aliases', {}),
                'claims': self._extract_relevant_claims(entity.get('claims', {})),
                'collected': datetime.now().isoformat()
            }
            
            print(f"    ✓ Collected Wikidata information")
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    def _extract_relevant_claims(self, claims):
        """
        Extract relevant Wikidata claims about Du Fu.
        
        Args:
            claims: Wikidata claims dictionary
            
        Returns:
            Filtered claims dictionary
        """
        # Properties we're interested in
        relevant_properties = {
            'P31': 'instance of',
            'P106': 'occupation',
            'P19': 'place of birth',
            'P20': 'place of death',
            'P569': 'date of birth',
            'P570': 'date of death',
            'P27': 'country of citizenship',
            'P101': 'field of work',
            'P135': 'movement',
            'P737': 'influenced by',
            'P800': 'notable work',
            'P1066': 'student of',
            'P802': 'student',
            'P140': 'religion',
            'P22': 'father',
            'P25': 'mother',
            'P26': 'spouse',
            'P40': 'child'
        }
        
        extracted = {}
        
        for prop_id, prop_name in relevant_properties.items():
            if prop_id in claims:
                extracted[prop_id] = {
                    'property': prop_name,
                    'values': claims[prop_id]
                }
        
        return extracted
    
    def _collect_related_articles(self):
        """
        Collect related Wikipedia articles about Tang Dynasty, Chinese poetry, etc.
        """
        related_topics = [
            ('en', 'Tang Dynasty', 'Historical period'),
            ('en', 'An Lushan Rebellion', 'Major historical event'),
            ('en', 'Chinese poetry', 'Literary tradition'),
            ('en', 'Classical Chinese poetry', 'Poetry form'),
            ('en', 'Tang poetry', 'Specific poetry period'),
            ('en', 'Li Bai', 'Contemporary poet'),
            ('en', 'Wang Wei (Tang dynasty)', 'Contemporary poet'),
            ('en', 'Regulated verse', 'Poetry form (Lüshi)'),
            ('en', 'Chengdu', 'Major location in Du Fu\'s life'),
            ('en', "Chang'an", 'Tang Dynasty capital')
        ]
        
        for lang, title, description in related_topics:
            print(f"  Collecting: {title} ({description})")
            
            content = self._get_wikipedia_article(lang, title)
            
            if content:
                self.related_articles.append({
                    'language': lang,
                    'title': title,
                    'description': description,
                    'content': content,
                    'word_count': len(content.split()),
                    'char_count': len(content),
                    'collected': datetime.now().isoformat()
                })
                print(f"    ✓ Collected: {len(content.split())} words")
            else:
                print(f"    ✗ Failed to collect")
            
            time.sleep(1)  # Rate limiting
    
    def _save_all_data(self):
        """
        Save all collected data to JSON files.
        """
        # Save Wikipedia articles
        wikipedia_file = os.path.join(self.output_dir, 'wikipedia_articles.json')
        with open(wikipedia_file, 'w', encoding='utf-8') as f:
            json.dump(self.wikipedia_data, f, ensure_ascii=False, indent=2)
        print(f"  Saved: wikipedia_articles.json ({len(self.wikipedia_data)} articles)")
        
        # Save Wikidata information
        wikidata_file = os.path.join(self.output_dir, 'wikidata_info.json')
        with open(wikidata_file, 'w', encoding='utf-8') as f:
            json.dump(self.wikidata_data, f, ensure_ascii=False, indent=2)
        print(f"  Saved: wikidata_info.json")
        
        # Save related articles
        related_file = os.path.join(self.output_dir, 'related_articles.json')
        with open(related_file, 'w', encoding='utf-8') as f:
            json.dump(self.related_articles, f, ensure_ascii=False, indent=2)
        print(f"  Saved: related_articles.json ({len(self.related_articles)} articles)")
        
        # Generate collection summary
        summary = {
            'collection_date': datetime.now().isoformat(),
            'author': 'Du Fu (杜甫)',
            'wikidata_qid': self.du_fu_qid,
            'wikipedia_articles': len(self.wikipedia_data),
            'related_articles': len(self.related_articles),
            'total_related_words': sum(a['word_count'] for a in self.related_articles),
            'languages': list(set(a['language'] for a in self.related_articles)),
            'topics_covered': [a['title'] for a in self.related_articles]
        }
        
        summary_file = os.path.join(self.output_dir, 'collection_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  Saved: collection_summary.json")
        
        # Print summary
        print()
        print("=" * 80)
        print("Collection Summary")
        print("=" * 80)
        print(f"Wikipedia articles collected: {summary['wikipedia_articles']}")
        print(f"Related articles collected: {summary['related_articles']}")
        print(f"Total words in related articles: {summary['total_related_words']:,}")
        print()
        print("Topics covered:")
        for topic in summary['topics_covered']:
            print(f"  - {topic}")
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
