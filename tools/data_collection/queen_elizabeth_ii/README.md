# Queen Elizabeth II Data Collection Tools

This directory contains scripts for collecting data about Queen Elizabeth II (1926-2022, reigned 1952-2022).

## Overview

Queen Elizabeth II's dataset focuses on her 70-year reign as the United Kingdom's monarch, capturing her formal speeches, public addresses, and historical significance.

## Data Sources

1. **Wikipedia API**: Biographical information, historical context
2. **Royal.uk Archives**: Official speeches and statements (manual extraction)
3. **Christmas Broadcasts**: Annual addresses (1952-2022)
4. **State Addresses**: Parliamentary speeches, Commonwealth addresses

## Collection Strategy

### Target Content
- **Token Goal**: 75,000 tokens minimum
- **Time Period**: 1952-2022 (70 years)
- **Language**: Formal British English
- **Content Types**: Speeches, broadcasts, official statements

### Challenges
- Limited content availability (controlled royal communications)
- Formal diplomatic language style
- Historical context spanning 70 years
- Copyright considerations for recent speeches

## Scripts

### 1. `collect_wikipedia_data.py`
Collects biographical and historical information from Wikipedia.

**Usage**:
```bash
python collect_wikipedia_data.py --output ../../datasets/queen_elizabeth_ii/raw_data/
```

### 2. `collect_speeches.py`
Manual collection template for organizing speech data.

### 3. `validate_sources.py`
Validates collected data and ensures proper attribution.

## Data Quality Standards

- All sources must be properly attributed
- Maintain chronological metadata for all content
- Verify historical accuracy
- Ensure copyright compliance
- Document collection methodology

## Output Structure

Collected data will be stored in:
```
datasets/queen_elizabeth_ii/
├── raw_data/
│   ├── wikipedia/
│   │   └── biography.json
│   ├── speeches/
│   │   ├── christmas_broadcasts/
│   │   └── state_addresses/
│   └── metadata/
│       └── source_log.json
```

## Notes

- Focus on public domain and officially released content
- Prioritize historical significance and representativeness
- Balance different periods of reign (early, middle, late)
- Include contextual information for RAG system effectiveness
