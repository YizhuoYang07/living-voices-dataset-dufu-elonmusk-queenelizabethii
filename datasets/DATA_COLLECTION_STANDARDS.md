# Living Voices - Data Collection Standards

## Overview
This document outlines the standardized data collection and processing procedures for all personas in the Living Voices project.

## Universal File Naming Conventions

### Raw Data Files
```
{source_type}_{year}_{month}_{sequential_id}.{format}
```
Examples:
- `speech_2023_03_001.txt`
- `interview_2022_12_005.json`
- `social_media_2024_01_150.csv`

### Processed Data Files
```
{persona_id}_{processing_stage}_{date_processed}.{format}
```
Examples:
- `elon_musk_cleaned_20241004.csv`
- `queen_elizabeth_vectorized_20241004.pkl`

## Data Schema Standards

### Raw Data Schema
```json
{
  "id": "unique_identifier",
  "persona": "elon_musk|queen_elizabeth_ii|du_fu",
  "source_type": "speech|interview|social_media|writing|wikipedia",
  "title": "content_title",
  "content": "full_text_content",
  "date": "YYYY-MM-DD",
  "source_url": "original_source_link",
  "reliability_score": "1-5_scale",
  "language": "en|zh|multi",
  "context": "situational_context",
  "keywords": ["tag1", "tag2", "tag3"],
  "collection_date": "YYYY-MM-DD",
  "collector": "team_member_id"
}
```

### Processed Data Schema
```json
{
  "id": "unique_identifier",
  "persona": "persona_name",
  "original_id": "reference_to_raw_data",
  "processed_content": "cleaned_text",
  "segments": ["segment1", "segment2"],
  "annotations": {
    "sentiment": "positive|negative|neutral",
    "topics": ["topic1", "topic2"],
    "entities": ["entity1", "entity2"],
    "temporal_markers": ["date1", "event1"]
  },
  "vectors": {
    "tfidf": "vector_representation",
    "embeddings": "dense_vector"
  },
  "processing_metadata": {
    "processing_date": "YYYY-MM-DD",
    "pipeline_version": "v1.0",
    "quality_score": "0.0-1.0"
  }
}
```

## Quality Assurance Checklist

### Data Collection Phase
- [ ] Source URL documented and accessible
- [ ] Date and context information complete
- [ ] Content type categorized correctly
- [ ] Language identified
- [ ] Reliability assessment conducted
- [ ] Ethical guidelines followed

### Data Processing Phase
- [ ] Text cleaning performed
- [ ] Encoding standardized (UTF-8)
- [ ] Segmentation applied appropriately
- [ ] Annotations follow schema
- [ ] Vector representations generated
- [ ] Quality metrics calculated

### Integration Phase
- [ ] Data format compatible with RAG system
- [ ] Cross-references between files maintained
- [ ] Duplicate content identified and handled
- [ ] Timeline consistency verified
- [ ] Context information preserved

## Persona-Specific Guidelines

### Elon Musk
- **Focus Areas**: Technology, business strategy, future vision
- **Language Style**: Informal to technical, innovative terminology
- **Temporal Priority**: Recent content (2015-present) given higher weight
- **Special Handling**: Technical jargon annotation required

### Queen Elizabeth II
- **Focus Areas**: State affairs, ceremonial duties, constitutional matters
- **Language Style**: Formal, diplomatic, traditional
- **Temporal Priority**: Even distribution across reign period
- **Special Handling**: Historical context essential for understanding

### Du Fu (杜甫)
- **Focus Areas**: Poetry, social commentary, personal philosophy
- **Language Style**: Classical Chinese, poetic expression
- **Temporal Priority**: Life period chronological ordering
- **Special Handling**: Historical and cultural context critical

## Technical Requirements

### Minimum Dataset Size
- **Per Persona**: 10,000+ tokens of unique content
- **Temporal Coverage**: Minimum 5 major life periods
- **Source Diversity**: At least 3 different source types

### Processing Pipeline Requirements
- **Text Cleaning**: Remove markup, normalize spacing
- **Tokenization**: Language-appropriate segmentation
- **Vector Generation**: TF-IDF + optional embeddings
- **Quality Control**: Automated and manual validation

### Storage Requirements
- **Format**: JSON for structured data, CSV for tabular
- **Encoding**: UTF-8 universal
- **Backup**: Version control with Git
- **Documentation**: README.md in each directory

## Ethical and Legal Compliance

### Data Sources
- Only publicly available content
- Proper attribution maintained
- Copyright and fair use respected
- Privacy considerations for recent content

### Content Guidelines
- Educational and research purposes only
- Balanced representation sought
- Controversial content handled sensitively
- Historical accuracy prioritized

### Usage Restrictions
- Non-commercial academic use
- Attribution to Living Voices project required
- Respect for depicted individuals' dignity
- Compliance with institutional ethics guidelines

---

**Document Version**: 1.0  
**Last Updated**: 2024-10-04  
**Authority**: Living Voices Project Team