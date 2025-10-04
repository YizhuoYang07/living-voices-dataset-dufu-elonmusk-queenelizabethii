"""
Du Fu Poetry Collection from Tang-Song Literature API

This script collects Du Fu's complete poetry works from the
Tang-Song Literature Chronological Map API.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from api_config import APIConfig


class DuFuDataCollector:
    """
    Collector for Du Fu's poetry and biographical data from API.
    """
    
    def __init__(self, output_dir: str, config: Optional[APIConfig] = None):
        """
        Initialize the collector.
        
        Args:
            output_dir: Directory to save collected data
            config: Optional API configuration instance
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.poems_dir = self.output_dir / "api_data" / "poems"
        self.poems_dir.mkdir(parents=True, exist_ok=True)
        
        self.biography_dir = self.output_dir / "api_data" / "biography"
        self.biography_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_dir = self.output_dir / "metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = config or APIConfig()
        self.session = requests.Session()
        self.session.headers.update(self.config.request_config["headers"])
        
        self.collection_log = []
        
    def _make_request(self, url: str, retry_count: int = 0) -> Optional[Dict]:
        """
        Make HTTP request with retry logic.
        
        Args:
            url: URL to request
            retry_count: Current retry attempt number
            
        Returns:
            JSON response data or None if failed
        """
        max_retries = self.config.request_config["retry_attempts"]
        timeout = self.config.request_config["timeout"]
        
        try:
            print(f"  Requesting: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"    Error: {e}")
            
            if retry_count < max_retries:
                delay = self.config.request_config["retry_delay"] * (retry_count + 1)
                print(f"    Retrying in {delay} seconds... (Attempt {retry_count + 1}/{max_retries})")
                time.sleep(delay)
                return self._make_request(url, retry_count + 1)
            else:
                print(f"    Failed after {max_retries} attempts")
                return None
    
    def collect_poems(self, max_pages: Optional[int] = None) -> List[Dict]:
        """
        Collect Du Fu's poems from API with pagination.
        
        Args:
            max_pages: Optional maximum number of pages to collect
            
        Returns:
            List of collected poems
        """
        print("Collecting Du Fu's poems from API...")
        print("=" * 70)
        
        all_poems = []
        page_no = 0
        
        while True:
            if max_pages and page_no >= max_pages:
                print(f"\nReached maximum page limit: {max_pages}")
                break
            
            print(f"\nPage {page_no}:")
            url = self.config.get_du_fu_poems_url(page_no=page_no)
            
            data = self._make_request(url)
            
            if not data:
                print(f"  No data returned for page {page_no}")
                break
            
            if not isinstance(data, list):
                if isinstance(data, dict) and "items" in data:
                    poems = data["items"]
                elif isinstance(data, dict) and "data" in data:
                    poems = data["data"]
                else:
                    print(f"  Unexpected data format: {type(data)}")
                    break
            else:
                poems = data
            
            if not poems:
                print(f"  No more poems found (empty response)")
                break
            
            print(f"  Collected {len(poems)} poems")
            all_poems.extend(poems)
            
            page_file = self.poems_dir / f"poems_page_{page_no}.json"
            with open(page_file, 'w', encoding='utf-8') as f:
                json.dump(poems, f, ensure_ascii=False, indent=2)
            
            self.collection_log.append({
                "type": "poems",
                "page": page_no,
                "count": len(poems),
                "file": str(page_file),
                "url": url,
                "timestamp": datetime.now().isoformat()
            })
            
            page_no += 1
            
            time.sleep(1)
        
        print(f"\n{'=' * 70}")
        print(f"Total poems collected: {len(all_poems)}")
        print(f"Total pages: {page_no}")
        
        return all_poems
    
    def collect_biography(self) -> Optional[Dict]:
        """
        Collect Du Fu's biographical information.
        
        Returns:
            Biography data or None if failed
        """
        print("\nCollecting Du Fu's biographical information...")
        
        url = self.config.get_du_fu_biography_url()
        data = self._make_request(url)
        
        if data:
            bio_file = self.biography_dir / "dufu_biography.json"
            with open(bio_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"  Saved biography to: {bio_file}")
            
            self.collection_log.append({
                "type": "biography",
                "file": str(bio_file),
                "url": url,
                "timestamp": datetime.now().isoformat()
            })
        
        return data
    
    def save_collection_log(self):
        """
        Save collection log to metadata directory.
        """
        log_file = self.metadata_dir / "collection_log.json"
        
        log_data = {
            "collection_date": datetime.now().isoformat(),
            "total_operations": len(self.collection_log),
            "operations": self.collection_log
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nCollection log saved to: {log_file}")
    
    def generate_summary(self, poems: List[Dict]) -> Dict:
        """
        Generate collection summary statistics.
        
        Args:
            poems: List of collected poems
            
        Returns:
            Summary statistics dictionary
        """
        total_poems = len(poems)
        
        poems_with_dates = [p for p in poems if p.get("creation_date_raw")]
        poems_with_places = [p for p in poems if p.get("place_code")]
        
        poem_types = {}
        for poem in poems:
            ptype = poem.get("poem_type", "Unknown")
            poem_types[ptype] = poem_types.get(ptype, 0) + 1
        
        total_chars = sum(
            len(''.join(p.get("poem_content_lines", []))) 
            for p in poems
        )
        
        estimated_tokens = int(total_chars * 1.3)
        
        summary = {
            "collection_date": datetime.now().isoformat(),
            "total_poems": total_poems,
            "poems_with_dates": len(poems_with_dates),
            "poems_with_places": len(poems_with_places),
            "poem_types": poem_types,
            "statistics": {
                "total_characters": total_chars,
                "estimated_tokens": estimated_tokens,
                "average_poem_length": total_chars // total_poems if total_poems > 0 else 0
            },
            "target": {
                "token_goal": 100000,
                "current_tokens": estimated_tokens,
                "progress_percent": round((estimated_tokens / 100000) * 100, 2)
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
        print("\n" + "=" * 70)
        print("COLLECTION SUMMARY")
        print("=" * 70)
        print(f"Total Poems Collected: {summary['total_poems']}")
        print(f"  - With dates: {summary['poems_with_dates']}")
        print(f"  - With locations: {summary['poems_with_places']}")
        
        print(f"\nPoem Types:")
        for ptype, count in sorted(summary['poem_types'].items(), 
                                   key=lambda x: x[1], reverse=True):
            print(f"  {ptype}: {count}")
        
        print(f"\nStatistics:")
        print(f"  Total characters: {summary['statistics']['total_characters']:,}")
        print(f"  Estimated tokens: {summary['statistics']['estimated_tokens']:,}")
        print(f"  Average poem length: {summary['statistics']['average_poem_length']} chars")
        
        print(f"\nProgress toward 100,000 token goal:")
        print(f"  Current: {summary['target']['current_tokens']:,} tokens")
        print(f"  Progress: {summary['target']['progress_percent']}%")
        
        print("=" * 70)


def main():
    """
    Main execution function.
    """
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    output_dir = dataset_root / "datasets" / "du_fu" / "raw_data"
    
    print("=" * 70)
    print("Du Fu Data Collection - Tang-Song Literature API")
    print("=" * 70)
    print(f"Output directory: {output_dir}")
    print()
    
    config = APIConfig()
    collector = DuFuDataCollector(str(output_dir), config)
    
    poems = collector.collect_poems(max_pages=None)
    
    if poems:
        collector.collect_biography()
        collector.save_collection_log()
        
        summary = collector.generate_summary(poems)
        collector.print_summary(summary)
        
        print(f"\nData collection completed successfully!")
        print(f"Data saved to: {output_dir}")
    else:
        print("\nError: No poems were collected!")
        sys.exit(1)


if __name__ == "__main__":
    main()
