# Du Fu Data Collection Tools

## Overview

This directory contains tools for collecting Du Fu's biographical and poetic data from the Tang-Song Literature Chronological Map API (唐宋文学编年地图).

**Target**: 100,000+ tokens for Du Fu persona dataset

## Data Sources

### Primary API: Tang-Song Literature Chronological Map

Based on Postman collection analysis, the API provides:

1. **Poetry Library (诗文库)** - Main source
   - Endpoint: `/api/writing/{dynasty}/{authorName}/{authorId}`
   - Du Fu info: dynasty=Tang (唐), author=杜甫, authorId=17270
   - Pagination supported: `pageNo` parameter (default 20 poems per page)

2. **People Database (人物)**
   - Endpoint: `/api/people/{dynasty}/{personId}`
   - Biographical information

3. **Geography (地理)**
   - Location information for poem creation places

4. **Calendar (年历)**
   - Historical events and dates

5. **Allusions & Vocabulary (词汇、典故)**
   - Cultural references and terminology

## API Structure

### Base URL
The Postman collections use `{{host}}` variable for base URL.
Format: `https://{{host}}/api/...`

### Authentication
Need to determine if authentication is required.

## Collection Strategy

### Phase 1: Core Poetry Collection
1. Collect all Du Fu poems from Poetry Library API
2. Extract:
   - Poem ID, title, content
   - Creation date (creation_date_raw)
   - Place code (place_code)
   - Poem type and style
   - Annotations and allusions
   - Word dictionary annotations

### Phase 2: Biographical Data
1. Extract Du Fu's biographical information
2. Life events timeline
3. Geographic movements

### Phase 3: Contextual Enrichment
1. Historical events (年历)
2. Geographic context (地理)
3. Cultural references (典故)

## Data Quality Requirements

From project plan:
- **Poem count**: 1,400+ poems (Du Fu's complete works)
- **Time coverage**: 712-770 CE (58 years)
- **Annotations**: Time, place, background, theme tags for each poem
- **Token target**: 100,000+ tokens (including annotations)

## Output Structure

```
datasets/du_fu/raw_data/
├── api_data/
│   ├── poems/
│   │   ├── poems_page_0.json
│   │   ├── poems_page_1.json
│   │   └── ...
│   ├── biography/
│   │   └── dufu_biography.json
│   ├── geography/
│   │   └── locations.json
│   └── timeline/
│       └── historical_events.json
├── metadata/
│   ├── collection_log.json
│   └── api_responses.json
└── README.md
```

## Next Steps

1. Create API client with proper base URL configuration
2. Implement pagination handler for poems collection
3. Build error handling and retry logic
4. Create data validation and quality checks
5. Generate collection summary statistics

## Notes

- Previous CSV files (dufu_poems_20250830_093635.csv) are outdated and will be ignored
- Fresh collection from API ensures data consistency
- All code follows academic standards: English comments, no emojis
- Comprehensive logging for reproducibility

---

**Author**: Living Voices Project - Du Fu Dataset Team  
**Date**: October 4, 2024  
**Status**: Initial planning phase
