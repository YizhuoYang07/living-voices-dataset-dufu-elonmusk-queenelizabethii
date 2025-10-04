"""
Collect Additional Wikipedia Articles for Queen Elizabeth II

This script extends the initial Wikipedia collection with additional related articles
to reach the 75,000 token target.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import wikipedia


def collect_additional_articles():
    """
    Collect additional Wikipedia articles about Queen Elizabeth II.
    """
    print("="*70)
    print("Collecting Additional Wikipedia Articles")
    print("="*70)
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    output_dir = dataset_root / "datasets" / "queen_elizabeth_ii" / "raw_data"
    wikipedia_dir = output_dir / "wikipedia"
    metadata_dir = output_dir / "metadata"
    
    # Load existing related articles
    related_file = wikipedia_dir / "related_articles.json"
    try:
        with open(related_file, 'r', encoding='utf-8') as f:
            existing_articles = json.load(f)
        print(f"Loaded {len(existing_articles)} existing articles")
    except FileNotFoundError:
        existing_articles = []
        print("No existing articles found, starting fresh")
    
    # Additional articles to collect
    additional_titles = [
        "George VI of the United Kingdom",
        "Monarchy of the United Kingdom",
        "Queen Elizabeth II's jewels",
        "Royal family",
        "Winston Churchill",
        "Margaret Thatcher"
    ]
    
    print(f"\nCollecting {len(additional_titles)} new articles...\n")
    
    newly_collected = []
    collection_log = []
    
    for title in additional_titles:
        try:
            print(f"Collecting: {title}")
            page = wikipedia.page(title)
            
            data = {
                "title": page.title,
                "url": page.url,
                "content": page.content,
                "summary": page.summary,
                "collection_timestamp": datetime.now().isoformat(),
                "word_count": len(page.content.split())
            }
            
            newly_collected.append(data)
            collection_log.append({
                "source": "Wikipedia Additional Article",
                "title": page.title,
                "url": page.url,
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "word_count": data["word_count"]
            })
            
            print(f"  ✓ Collected {data['word_count']:,} words")
            
        except wikipedia.exceptions.PageError:
            print(f"  ✗ Page not found: {title}")
            collection_log.append({
                "source": "Wikipedia Additional Article",
                "title": title,
                "timestamp": datetime.now().isoformat(),
                "status": "not_found"
            })
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"  ✗ Disambiguation needed for: {title}")
            print(f"    Options: {e.options[:5]}")
            collection_log.append({
                "source": "Wikipedia Additional Article",
                "title": title,
                "timestamp": datetime.now().isoformat(),
                "status": "disambiguation",
                "options": e.options[:10]
            })
        except Exception as e:
            print(f"  ✗ Error: {e}")
            collection_log.append({
                "source": "Wikipedia Additional Article",
                "title": title,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            })
    
    if not newly_collected:
        print("\nNo new articles collected.")
        return
    
    # Combine with existing articles
    all_articles = existing_articles + newly_collected
    
    # Save updated collection
    print(f"\nSaving {len(all_articles)} total articles...")
    with open(related_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Saved to: {related_file}")
    
    # Update collection log
    log_file = metadata_dir / "collection_log.json"
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            existing_log = json.load(f)
        existing_log["items"].extend(collection_log)
        existing_log["total_items"] = len(existing_log["items"])
        existing_log["last_updated"] = datetime.now().isoformat()
    except FileNotFoundError:
        existing_log = {
            "collection_date": datetime.now().isoformat(),
            "total_items": len(collection_log),
            "items": collection_log
        }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(existing_log, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Updated collection log")
    
    # Calculate statistics
    total_words = sum(article["word_count"] for article in all_articles)
    estimated_tokens = int(total_words / 1.3)
    
    print("\n" + "="*70)
    print("COLLECTION COMPLETE")
    print("="*70)
    print(f"New articles collected: {len(newly_collected)}")
    print(f"Total articles: {len(all_articles)}")
    print(f"Total words (related articles only): {total_words:,}")
    print(f"Estimated tokens (related articles): {estimated_tokens:,}")
    print("="*70)
    print("\nRun validate_data.py to see updated overall statistics.")


if __name__ == "__main__":
    collect_additional_articles()
