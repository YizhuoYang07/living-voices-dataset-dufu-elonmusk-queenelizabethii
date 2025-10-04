# Living Voices Dataset# Living Voices - Dataset Overview



**Project**: Living Voices - Multi-Persona RAG System  ## Project Structure

**Institution**: University of Technology Sydney (UTS)  

**Course**: 36118 Applied Natural Language Processing  ```

**Academic Year**: 2024-2025  data/

**Version**: 1.0  ├── elon_musk/                          # Elon Musk persona dataset

**Last Updated**: October 4, 2025│   ├── raw_data/

│   │   ├── social_media/               # Twitter/X content, social posts

## Abstract│   │   ├── interviews/                 # Podcast transcripts, media interviews

│   │   ├── speeches/                   # Conference talks, keynote addresses

The Living Voices Dataset is a comprehensive multilingual collection designed for Retrieval-Augmented Generation (RAG) systems targeting historical and contemporary persona dialogue simulation. This dataset encompasses three distinct personas spanning 13 centuries of human history: Du Fu (712-770 CE), Queen Elizabeth II (1926-2022), and Elon Musk (1971-present). The collection aggregates 1,810,721 tokens across 1,564 structured documents and 3,858 optimized training chunks.│   │   ├── writings/                   # Articles, books, official statements

│   │   └── wikipedia/                  # Encyclopedia and biographical data

## Project Overview│   ├── processed_data/

│   │   ├── cleaned/                    # Normalized and cleaned text

### Research Objectives│   │   ├── segmented/                  # Sentence/paragraph segmentation

│   │   ├── annotated/                  # NER, sentiment, topic annotations

1. **Persona Authenticity**: Construct linguistically and contextually accurate digital representations of historical and contemporary figures│   │   └── vectorized/                 # TF-IDF and embedding representations

2. **Temporal Diversity**: Capture communication patterns across diverse historical periods and cultural contexts│   ├── external_resources/

3. **RAG Optimization**: Structure data for efficient retrieval and generation in conversational AI systems│   │   ├── knowledge_base/             # Tesla, SpaceX, technology context

4. **Academic Rigor**: Maintain scholarly standards in data collection, processing, and documentation│   │   ├── timeline/                   # Career milestones, company history

│   │   └── context/                    # Market conditions, contemporary events

### Dataset Composition│   ├── metadata/                       # Dataset documentation and statistics

│   └── README.md                       # Detailed dataset documentation

| Persona | Time Period | Language | Documents | Chunks | Tokens | Sources |│

|---------|-------------|----------|-----------|--------|--------|---------|├── queen_elizabeth_ii/                 # Queen Elizabeth II persona dataset

| Du Fu | 712-770 CE | Classical Chinese | 1,496 | 3,449 | 558,867 | Poetry corpus, historical records |│   ├── raw_data/

| Elon Musk | 1971-present | English | 48 | 96 | 1,101,561 | Interviews, speeches, Wikipedia |│   │   ├── official_speeches/          # State addresses, formal ceremonies

| Queen Elizabeth II | 1926-2022 | English | 20 | 313 | 150,293 | Official speeches, Wikipedia |│   │   ├── christmas_broadcasts/       # Annual Christmas messages (1952-2021)

| **Total** | **13 centuries** | **2 languages** | **1,564** | **3,858** | **1,810,721** | **Multiple verified sources** |│   │   ├── parliamentary_addresses/    # Parliament openings, official statements

│   │   ├── interviews/                 # Rare media appearances, documentaries

## Directory Structure│   │   └── wikipedia/                  # Biographical and historical data

│   ├── processed_data/

```│   │   ├── cleaned/                    # Text normalization and standardization

datasets/│   │   ├── segmented/                  # Topic-based content segmentation

├── du_fu/                          # Classical Chinese poet (712-770 CE)│   │   ├── annotated/                  # Historical context and sentiment analysis

│   ├── raw_data/                   # Original source materials│   │   └── vectorized/                 # Vector representations for retrieval

│   │   ├── poetry/                 # Complete poetry corpus (1,144 poems)│   ├── external_resources/

│   │   ├── wikipedia/              # Biographical and contextual articles│   │   ├── knowledge_base/             # Royal protocols, Commonwealth history

│   │   └── historical_records/     # Historical documentation│   │   ├── timeline/                   # Reign events, historical milestones

│   ├── processed_data/             # RAG-optimized structured data│   │   └── context/                    # Political climate, social changes

│   │   ├── structured_documents.json│   ├── metadata/                       # Quality metrics and documentation

│   │   ├── training_chunks.json│   └── README.md                       # Comprehensive dataset guide

│   │   ├── dataset_metadata.json│

│   │   ├── processing_report.json├── 杜甫/                              # Du Fu persona dataset (existing)

│   │   └── validation_report.json│   └── [existing structure]

│   ├── external_resources/         # Supporting materials│

│   │   ├── tang_dynasty_context/   # Historical context└── data_collection_standards.md        # Universal guidelines and standards

│   │   └── geographical_data/      # Location information```

│   └── README.md

│## Dataset Characteristics

├── elon_musk/                      # Contemporary entrepreneur (1971-)

│   ├── raw_data/| Persona | Language | Primary Sources | Time Period | Content Types |

│   │   ├── wikipedia/              # Biographical articles|---------|----------|----------------|-------------|---------------|

│   │   ├── supplementary_materials/ # Deep-dive articles| **Elon Musk** | English | Social media, interviews, speeches | 1999-2024 | Technical, business, personal |

│   │   └── interviews/             # Interview transcripts| **Queen Elizabeth II** | English | Official speeches, broadcasts | 1952-2022 | Formal, ceremonial, constitutional |

│   ├── processed_data/| **Du Fu (杜甫)** | Chinese | Poetry, historical records | 712-770 CE | Literary, philosophical, social |

│   │   ├── structured_documents.json

│   │   ├── training_chunks.json## Data Processing Pipeline

│   │   ├── dataset_metadata.json

│   │   ├── processing_report.json### Stage 1: Raw Data Collection

│   │   └── validation_report.json- **Wikipedia API integration** for biographical data

│   └── README.md- **Web scraping** for publicly available content

│- **Manual curation** for high-quality sources

├── queen_elizabeth_ii/             # British monarch (1926-2022)- **Source verification** and reliability assessment

│   ├── raw_data/

│   │   ├── wikipedia/              # Biographical articles### Stage 2: Text Processing

│   │   ├── speeches/               # Official speeches and broadcasts- **Cleaning**: HTML removal, encoding normalization

│   │   └── related_articles/       # Royal family, Commonwealth- **Segmentation**: Sentence and paragraph boundaries

│   ├── processed_data/- **Language detection** and handling

│   │   ├── structured_documents.json- **Deduplication** and quality filtering

│   │   ├── training_chunks.json

│   │   ├── dataset_metadata.json### Stage 3: Annotation and Analysis

│   │   ├── processing_report.json- **Named Entity Recognition** (NER)

│   │   └── validation_report.json- **Sentiment analysis** and emotional labeling

│   └── README.md- **Topic modeling** and categorization

│- **Temporal annotation** and chronological ordering

├── metadata/                       # Cross-dataset documentation

│   ├── persona_profiles.json       # Comprehensive persona descriptions### Stage 4: Vector Representation

│   ├── collection_standards.json   # Data collection protocols- **TF-IDF vectorization** for retrieval

│   └── README.md- **Dense embeddings** for semantic similarity

│- **Index construction** for efficient search

├── README.md                       # This file- **Quality validation** and performance testing

└── DATA_COLLECTION_STANDARDS.md   # Detailed methodology

```## Usage in RAG System



## Methodology### Retrieval Component

- **Query processing**: TF-IDF similarity matching

### Data Collection- **Context ranking**: Relevance and temporal weighting

- **Multi-source fusion**: Combining different content types

#### Source Selection Criteria- **Persona-specific filtering**: Maintaining character consistency

- **Authenticity**: Primary sources prioritized over secondary interpretations

- **Reliability**: Verified sources from academic, governmental, or authoritative institutions### Generation Component

- **Public Domain**: Exclusive use of legally accessible public content- **Prompt engineering**: Persona-specific templates

- **Representative Coverage**: Balanced representation across persona's life phases- **Context integration**: Seamless information blending

- **Style preservation**: Maintaining authentic voice

#### Collection Procedures- **Response validation**: Quality and accuracy checking

1. **Du Fu**: Utilized complete digitized poetry corpus from scholarly databases, supplemented with historical Wikipedia articles

2. **Elon Musk**: Collected Wikipedia biographical content and related technical/business articles## Quality Metrics

3. **Queen Elizabeth II**: Gathered Wikipedia articles covering reign, speeches, and constitutional role

### Coverage Metrics

### Data Processing Pipeline- **Temporal Coverage**: Representation across life periods

- **Content Diversity**: Multiple source types and formats

#### Stage 1: Text Extraction and Cleaning- **Topic Breadth**: Comprehensive subject matter coverage

- HTML/XML markup removal- **Language Quality**: Grammatical and semantic correctness

- Character encoding normalization (UTF-8)

- Whitespace standardization### Accuracy Metrics

- Duplicate detection and removal- **Factual Accuracy**: Historical and biographical correctness

- **Source Reliability**: Verification against authoritative sources

#### Stage 2: Document Structuring- **Consistency**: Cross-reference validation

- Metadata annotation (date, source, category, language)- **Completeness**: Minimal information gaps

- Content segmentation by topic and chronology

- Entity recognition and tagging### Performance Metrics

- Quality assessment scoring- **Retrieval Precision**: Relevant content identification

- **Response Quality**: Generated content evaluation

#### Stage 3: Training Chunk Generation- **Processing Speed**: Efficiency measurements

- Semantic-unit based segmentation- **Storage Optimization**: Data compression and access

- Context preservation across chunks

- Optimal length determination for RAG retrieval## Ethical Framework

- Cross-reference maintenance

### Data Collection Ethics

#### Stage 4: Validation and Quality Control- **Public Domain Priority**: Focus on openly available content

- Structural integrity verification- **Attribution Standards**: Proper source crediting

- Cross-reference validation- **Privacy Respect**: Avoiding personal/private information

- Statistical analysis of token distribution- **Cultural Sensitivity**: Respectful representation

- Manual spot-checking of content accuracy

### Usage Ethics

### Technical Specifications- **Educational Purpose**: Academic and learning applications

- **Balanced Representation**: Avoiding bias and stereotyping

#### File Formats- **Historical Accuracy**: Fact-based content generation

- **Raw Data**: JSON, TXT, CSV- **Responsible AI**: Transparent limitations and capabilities

- **Processed Data**: JSON (structured documents and chunks)

- **Metadata**: JSON, Markdown## Technical Specifications



#### Data Schema### File Formats

- **Raw Data**: TXT, CSV, JSON

**Structured Document Schema**:- **Processed Data**: CSV, JSON, PKL

```json- **Vectors**: NPY, PKL, HDF5

{- **Metadata**: JSON, YAML, MD

  "id": "unique_document_identifier",

  "title": "document_title",### Dependencies

  "type": "biography|poetry|speech|interview|article",- **Python 3.9+**: Core processing language

  "category": "thematic_category",- **scikit-learn**: TF-IDF and machine learning

  "content": "full_text_content",- **pandas**: Data manipulation and analysis

  "summary": "brief_summary",- **requests**: API interactions and web scraping

  "url": "source_url",- **transformers**: Advanced NLP capabilities

  "word_count": integer,

  "char_count": integer,### Performance Requirements

  "collected": "ISO_8601_datetime",- **Storage**: ~5GB total for all personas

  "processed": "ISO_8601_datetime",- **Memory**: 8GB RAM for processing

  "metadata": {- **Processing Time**: <24 hours for complete pipeline

    "persona": "persona_name",- **Query Response**: <2 seconds for retrieval + generation

    "language": "language_code",

    "time_period": "relevant_dates"---

  }

}**Project**: Living Voices - Digital Persona RAG System  

```**Institution**: University of Technology Sydney (UTS)  

**Course**: 36118 Applied Natural Language Processing  

**Training Chunk Schema**:**Team**: Ricki Yang, Haoyu Wang, Weiran Sun, Lin Li, Guorui Gao  

```json**Last Updated**: 2024-10-04
{
  "id": "unique_chunk_identifier",
  "source_document_id": "reference_to_parent_document",
  "type": "full_article|summary|excerpt",
  "title": "chunk_title",
  "content": "chunk_text",
  "category": "thematic_category",
  "tokens": integer,
  "metadata": {
    "document_type": "parent_type",
    "word_count": integer,
    "char_count": integer
  }
}
```

## Quality Assurance

### Validation Metrics
- **Completeness**: All required fields present in 100% of documents
- **Uniqueness**: Zero duplicate IDs across all datasets
- **Referential Integrity**: 100% valid cross-references between chunks and documents
- **Token Accuracy**: Validated token counts match actual content

### Quality Scores

| Dataset | Documents | Chunks | Validation Status | Quality Score |
|---------|-----------|--------|-------------------|---------------|
| Du Fu | 1,496 | 3,449 | PASSED | 100/100 |
| Elon Musk | 48 | 96 | PASSED | 100/100 |
| Queen Elizabeth II | 20 | 313 | PASSED | 100/100 |

### Validation Reports
Each dataset includes a comprehensive `validation_report.json` containing:
- File existence verification
- Schema compliance checking
- Content integrity validation
- Statistical summaries
- Issue and warning logs

## Ethical Considerations

### Data Ethics
1. **Public Domain Compliance**: All content sourced from publicly accessible materials
2. **Attribution**: Original sources properly credited and documented
3. **Privacy**: No private or confidential information included
4. **Cultural Sensitivity**: Respectful treatment of historical and cultural contexts

### Usage Ethics
1. **Educational Purpose**: Dataset intended for academic and research applications
2. **Non-Commercial**: Restricted to non-commercial educational use
3. **Accuracy**: Historical and factual accuracy maintained throughout
4. **Bias Awareness**: Conscious effort to present balanced perspectives

### Limitations
1. **Source Limitations**: Reliance on available digital archives may introduce selection bias
2. **Translation**: Classical Chinese content maintains original language without translation
3. **Contemporary Content**: Musk and Elizabeth II datasets limited to public statements
4. **Temporal Gaps**: Not all life periods equally represented due to source availability

## RAG System Integration

### Retrieval Component Design
- **Indexing**: Vector embeddings for semantic similarity search
- **Context Ranking**: Relevance scoring based on query-document similarity
- **Temporal Filtering**: Time-aware retrieval for historical accuracy
- **Multi-Source Fusion**: Integration of multiple document types per query

### Generation Component Design
- **Persona Consistency**: Style-specific prompt engineering per persona
- **Context Integration**: Seamless incorporation of retrieved information
- **Factual Grounding**: Generation constrained by retrieved factual content
- **Response Validation**: Post-generation fact-checking against source material

### Performance Specifications
- **Retrieval Latency**: Target <500ms per query
- **Generation Quality**: BLEU score >0.7 for factual content
- **Persona Authenticity**: Human evaluation for style consistency
- **Scalability**: Support for concurrent multi-persona queries

## Usage Guidelines

### Academic Usage
This dataset is provided for educational and research purposes under the following conditions:
1. **Citation Required**: Proper attribution to Living Voices Project
2. **Non-Commercial**: No commercial applications without explicit permission
3. **Share-Alike**: Derivative works should maintain similar open standards
4. **Ethical Use**: Respect for depicted individuals and cultural contexts

### Recommended Citation
```
Living Voices Dataset (2024-2025). Du Fu, Elon Musk, and Queen Elizabeth II 
Persona Collections for RAG Systems. University of Technology Sydney. 
36118 Applied Natural Language Processing. Version 1.0.
```

### Access and Distribution
- **Repository**: Available through UTS institutional repository
- **License**: MIT License for code, CC BY-NC-SA 4.0 for data
- **Support**: Technical questions directed to project team

## Technical Requirements

### System Requirements
- **Storage**: Minimum 2GB available disk space
- **Memory**: 8GB RAM recommended for processing
- **Python**: Version 3.9 or higher
- **Dependencies**: See individual dataset README files

### Software Dependencies
```python
# Core processing
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0

# NLP libraries
transformers>=4.25.0
jieba>=0.42.1  # For Chinese text processing
spacy>=3.4.0

# Data handling
requests>=2.28.0
beautifulsoup4>=4.11.0
```

## Future Development

### Planned Enhancements
1. **Multilingual Expansion**: Addition of translation layers for cross-language queries
2. **Temporal Analysis**: Deep-dive into chronological pattern analysis
3. **Comparative Studies**: Cross-persona linguistic and thematic comparisons
4. **Interactive Interface**: Web-based exploration and query interface

### Research Opportunities
1. **Diachronic Linguistics**: Study of language evolution across three time periods
2. **Persona Psychology**: Computational analysis of personality expression
3. **Historical NLP**: Application of modern NLP to classical texts
4. **Cultural Studies**: Cross-cultural communication pattern analysis

## Team and Contact

**Project Team**:
- Ricki Yang (Project Lead)
- Haoyu Wang
- Weiran Sun
- Lin Li
- Guorui Gao

**Institution**: University of Technology Sydney  
**Faculty**: Faculty of Engineering and Information Technology  
**Course**: 36118 Applied Natural Language Processing  
**Instructor**: [Course Instructor Name]

**Contact**: For technical questions or collaboration inquiries, please contact through UTS official channels.

## Acknowledgments

We acknowledge the following sources and resources:
- Chinese Text Project for Du Fu poetry corpus
- Wikipedia contributors for biographical content
- Academic advisors for methodological guidance
- UTS Faculty for computational resources and support

## References

1. Project documentation available in individual dataset directories
2. Data collection standards detailed in `DATA_COLLECTION_STANDARDS.md`
3. Processing scripts available in `tools/` directory
4. Validation reports available in each dataset's `processed_data/` directory

---

**Document Version**: 1.0  
**Last Revision**: October 4, 2025  
**Status**: Complete and Validated  
**Next Review**: June 2025
