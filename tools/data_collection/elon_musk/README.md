# Elon Musk Data Collection Tools

This directory contains scripts for collecting data about Elon Musk (1971-present).

## Overview

Elon Musk's dataset focuses on his career as entrepreneur, engineer, and technology visionary, capturing his evolution from PayPal to Tesla, SpaceX, and beyond.

## Data Sources

1. **Wikipedia API**: Biographical information, career milestones, company history
2. **Public Speeches**: TED talks, conference presentations, product launches
3. **Company Communications**: Tesla/SpaceX official statements and shareholder letters
4. **Media Interviews**: Authorized transcripts from major media outlets

## Collection Strategy

### Target Content
- **Token Goal**: 100,000 tokens minimum
- **Time Period**: 1999-2024 (25 years of public career)
- **Language**: English (American, technical style)
- **Content Types**: Speeches, interviews, company statements, biographical material

### Challenges
- High content volume across multiple platforms
- Diverse communication styles (technical to casual)
- Copyright considerations for interviews and speeches
- Social media content (Twitter/X) access limitations

### Content Distribution Target
- Technical/Engineering: 40%
- Business/Strategy: 25%
- Future Vision: 20%
- Personal Views: 15%

## Scripts

### 1. collect_wikipedia_data.py
Collects biographical and company information from Wikipedia.

**Usage**:
```bash
python collect_wikipedia_data.py --output ../../datasets/elon_musk/raw_data/
```

### 2. collect_additional_sources.py
Template for collecting supplementary content from various sources.

### 3. validate_data.py
Validates collected data and ensures proper attribution.

## Data Quality Standards

- All sources must be properly attributed
- Maintain chronological metadata for all content
- Verify factual accuracy against multiple sources
- Ensure copyright compliance
- Document collection methodology

## Output Structure

Collected data will be stored in:
```
datasets/elon_musk/
├── raw_data/
│   ├── wikipedia/
│   │   └── biography.json
│   ├── speeches/
│   ├── interviews/
│   └── metadata/
│       └── source_log.json
```

## Notes

- Focus on publicly available and authorized content
- Prioritize technical and business content over social media
- Balance different career phases (PayPal, Tesla, SpaceX, X)
- Include contextual information for RAG system effectiveness
- Maintain consistent time period tagging (early/middle/recent career)

## Time Periods

- Early Career (1999-2008): PayPal era, business foundation
- Growth Phase (2008-2018): Tesla/SpaceX expansion, technology evangelist
- Recent Phase (2018-2024): X acquisition, increased public profile
