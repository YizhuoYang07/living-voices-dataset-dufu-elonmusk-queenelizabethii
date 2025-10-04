"""
Queen Elizabeth II Speech Collection Template

This script provides a structured template for manually collecting and organizing
speeches and official statements by Queen Elizabeth II.

Due to copyright restrictions on recent royal speeches, this template helps organize
publicly available content from official sources.

Author: Living Voices Project
Date: 2024-10-04
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class SpeechTemplate:
    """
    Template structure for organizing Queen Elizabeth II speeches.
    """
    
    @staticmethod
    def create_speech_entry(
        title: str,
        date: str,
        category: str,
        content: str,
        occasion: str = "",
        location: str = "",
        source_url: str = "",
        notes: str = ""
    ) -> Dict:
        """
        Create a standardized speech entry.
        
        Args:
            title: Title of the speech
            date: Date in ISO format (YYYY-MM-DD)
            category: Speech category (christmas_broadcast, state_address, etc.)
            content: Full text of the speech
            occasion: Special occasion or context
            location: Location where speech was delivered
            source_url: URL to official source
            notes: Additional notes or context
            
        Returns:
            Dictionary containing structured speech data
        """
        return {
            "title": title,
            "date": date,
            "year": int(date[:4]) if date else None,
            "category": category,
            "occasion": occasion,
            "location": location,
            "content": content,
            "word_count": len(content.split()),
            "character_count": len(content),
            "source": {
                "url": source_url,
                "access_date": datetime.now().isoformat(),
                "copyright_status": "public_domain" if int(date[:4]) < 1972 else "verify_needed"
            },
            "metadata": {
                "reign_period": SpeechTemplate._determine_reign_period(date),
                "historical_context": notes,
                "created_timestamp": datetime.now().isoformat()
            }
        }
    
    @staticmethod
    def _determine_reign_period(date: str) -> str:
        """
        Determine the period of reign for the speech.
        
        Args:
            date: Date in ISO format
            
        Returns:
            Reign period label
        """
        if not date:
            return "unknown"
        
        year = int(date[:4])
        
        if 1952 <= year <= 1969:
            return "early_reign"
        elif 1970 <= year <= 1989:
            return "middle_reign"
        elif 1990 <= year <= 2009:
            return "late_reign"
        elif 2010 <= year <= 2022:
            return "final_years"
        else:
            return "unknown"


# Example Speech Categories
SPEECH_CATEGORIES = {
    "christmas_broadcast": "Annual Christmas Day broadcasts",
    "state_opening": "State Opening of Parliament addresses",
    "commonwealth_day": "Commonwealth Day messages",
    "jubilee": "Jubilee celebrations speeches",
    "war_memorial": "Remembrance and war memorial addresses",
    "state_visit": "State visit speeches",
    "special_occasion": "Special occasions and events"
}


# Template for Christmas Broadcasts Collection
CHRISTMAS_BROADCASTS_TEMPLATE = """
# Christmas Broadcasts Collection Guide

## Overview
Queen Elizabeth II delivered annual Christmas broadcasts from 1952 to 2021.
These speeches provide consistent year-over-year content and are often available
in the public domain or through official royal archives.

## Collection Strategy

### Priority Years (Represent different eras):
1. 1952 - First Christmas broadcast (early reign)
2. 1957 - First televised broadcast
3. 1977 - Silver Jubilee year
4. 1991 - Gulf War period
5. 1997 - Death of Princess Diana
6. 2002 - Golden Jubilee year
7. 2012 - Diamond Jubilee year
8. 2020 - COVID-19 pandemic
9. 2021 - Final Christmas broadcast

### Sources:
- Royal.uk official transcripts (limited availability)
- British Library archives
- National Archives (UK)
- Academic databases and historical collections

## Data Entry Format:

```python
speech = {
    "title": "Christmas Broadcast 1952",
    "date": "1952-12-25",
    "category": "christmas_broadcast",
    "occasion": "First Christmas Broadcast as Queen",
    "location": "Sandringham House",
    "content": "[Full speech text here]",
    "source": {
        "url": "https://...",
        "description": "Official royal archives"
    },
    "notes": "First broadcast after accession to throne in February 1952"
}
```

## Token Estimation:
- Average Christmas broadcast: 600-1000 words (~460-770 tokens)
- 70 broadcasts total (1952-2021): ~35,000-50,000 tokens potential
- Priority: Collect at least 10 representative broadcasts (~5,000-7,000 tokens)
"""


def create_manual_entry_template(output_dir: str):
    """
    Create a manual entry template file for speech collection.
    
    Args:
        output_dir: Directory to save the template
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    template = {
        "collection_info": {
            "purpose": "Manual entry template for Queen Elizabeth II speeches",
            "date_created": datetime.now().isoformat(),
            "categories": SPEECH_CATEGORIES
        },
        "example_entries": [
            SpeechTemplate.create_speech_entry(
                title="Christmas Broadcast 1952",
                date="1952-12-25",
                category="christmas_broadcast",
                content="[Insert full speech text here]",
                occasion="First Christmas Broadcast as Queen",
                location="Sandringham House",
                source_url="https://www.royal.uk/...",
                notes="First broadcast after accession in February 1952"
            )
        ],
        "instructions": {
            "1_collect": "Gather speech texts from official sources",
            "2_enter": "Copy speech text into 'content' field",
            "3_metadata": "Fill in all metadata fields accurately",
            "4_verify": "Double-check dates and sources",
            "5_save": "Save as JSON in appropriate subfolder"
        },
        "speeches": []
    }
    
    template_file = output_path / "speech_entry_template.json"
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print(f"Template created: {template_file}")
    
    # Create guide document
    guide_file = output_path / "collection_guide.md"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(CHRISTMAS_BROADCASTS_TEMPLATE)
    
    print(f"Guide created: {guide_file}")


def main():
    """
    Main execution function.
    """
    script_dir = Path(__file__).parent
    dataset_root = script_dir.parent.parent.parent
    output_dir = dataset_root / "datasets" / "queen_elizabeth_ii" / "raw_data" / "speeches"
    
    print("="*70)
    print("Creating Speech Collection Templates")
    print("="*70)
    
    create_manual_entry_template(str(output_dir))
    
    print("\nTemplates created successfully!")
    print(f"Location: {output_dir}")
    print("\nNext steps:")
    print("1. Review collection_guide.md for speech collection strategy")
    print("2. Use speech_entry_template.json to enter collected speeches")
    print("3. Focus on priority Christmas broadcasts and state addresses")


if __name__ == "__main__":
    main()
