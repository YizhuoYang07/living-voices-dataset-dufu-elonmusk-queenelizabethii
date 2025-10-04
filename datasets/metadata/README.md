# Living Voices Dataset - Metadata

This directory contains comprehensive metadata files for the Living Voices Dataset, providing detailed information about dataset structure, statistics, sources, and versioning.

## 📁 Metadata Files

### Core Metadata

#### `version_info.json`
**Dataset version and release information**
- Version number (Semantic Versioning)
- Release date and status
- Persona details and compatibility info
- Maintainer information
- License and citation guidelines

#### `statistics.json`
**Comprehensive dataset statistics**
- Overview: Total counts and metrics
- Per-persona statistics:
  - Document counts by type
  - Chunk distribution
  - Content metrics (words/characters)
  - Language and era information
- Quality metrics and validation status
- Distribution analysis by language and era

#### `sources.json`
**Source attribution and references**
- Primary sources for each persona
- Attribution and licensing information
- Collection methodology
- Ethical considerations
- Reference links and URLs

#### `changelog.md`
**Version history and changes**
- Release notes for all versions
- Added, changed, and fixed items
- Version comparison table
- Maintenance and support information

---

## 📊 Dataset Statistics Summary

**Current Version:** 1.0.0 (Released 2025-10-04)

### Overview
- **Total Personas:** 3
- **Total Documents:** 1,566
- **Total Training Chunks:** 3,886
- **Total Content:** 765,664 units (characters + words)
- **Languages:** Classical Chinese, English
- **Time Span:** Tang Dynasty (712 CE) to Present (2025)

### By Persona

| Persona | Documents | Chunks | Content | Era |
|---------|-----------|--------|---------|-----|
| **Du Fu (杜甫)** | 1,496 | 3,449 | 431,083 chars | Tang Dynasty (712-770 CE) |
| **Elon Musk** | 48 | 96 | 321,176 words | Contemporary (1971-present) |
| **Queen Elizabeth II** | 22 | 341 | 13,405 words | Modern (1926-2022) |

---

## 🎯 Metadata Standards

This dataset follows established metadata standards for reproducibility and interoperability:

### Standards Compliance
- **Dublin Core:** Core metadata elements
- **Schema.org:** Dataset schema for web discovery
- **DataCite:** Research data citation standards
- **FAIR Principles:** Findable, Accessible, Interoperable, Reusable

### Metadata Elements

#### Descriptive Metadata
- Title, description, and keywords
- Creator and contributor information
- Language and subject classification
- Temporal and spatial coverage

#### Administrative Metadata
- Version control and change tracking
- Rights and licensing information
- Provenance and processing history
- Quality assurance records

#### Structural Metadata
- File formats and organization
- Relationships between components
- Schema and data model documentation
- Technical requirements

#### Preservation Metadata
- Fixity and integrity checks
- Format specifications
- Migration and backup procedures
- Long-term accessibility plans

---

## 📖 Usage Guide

### Accessing Metadata

All metadata files are in JSON or Markdown format and can be accessed programmatically:

```python
import json

# Load version information
with open('metadata/version_info.json', 'r', encoding='utf-8') as f:
    version_info = json.load(f)
    print(f"Dataset version: {version_info['version']}")

# Load statistics
with open('metadata/statistics.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)
    print(f"Total documents: {stats['overview']['total_documents']}")

# Load source information
with open('metadata/sources.json', 'r', encoding='utf-8') as f:
    sources = json.load(f)
    for persona in sources['sources_by_persona']:
        print(f"{persona}: {len(sources['sources_by_persona'][persona]['primary_sources'])} sources")
```

### Validating Dataset Integrity

Use metadata to verify dataset completeness:

```python
import json

def validate_dataset():
    with open('metadata/statistics.json', 'r') as f:
        expected = json.load(f)
    
    # Verify each persona
    for persona_id, stats in expected['personas'].items():
        doc_path = f'{persona_id}/processed_data/structured_documents.json'
        with open(doc_path, 'r') as f:
            actual_docs = len(json.load(f))
        
        expected_docs = stats['documents']['total']
        assert actual_docs == expected_docs, f"{persona_id}: Expected {expected_docs}, got {actual_docs}"
    
    print("✓ Dataset validation passed!")

validate_dataset()
```

---

## 🔄 Version Management

### Semantic Versioning

The dataset follows [Semantic Versioning](https://semver.org/):

- **MAJOR version** (X.0.0): Incompatible changes to structure or format
- **MINOR version** (1.X.0): New personas or features added
- **PATCH version** (1.0.X): Bug fixes and corrections

### Current Version: 1.0.0

This is the first stable release with:
- ✓ Complete data for 3 personas
- ✓ Validated and verified content
- ✓ Comprehensive documentation
- ✓ Production-ready status

---

## 📝 Citation & Attribution

### Dataset Citation

```bibtex
@dataset{living_voices_2025,
  title = {Living Voices Dataset},
  version = {1.0.0},
  year = {2025},
  author = {Living Voices Project Team},
  institution = {UTS 36118 Applied Natural Language Processing},
  note = {Multi-persona historical dataset for conversational AI}
}
```

### Source Attribution

Individual sources are documented in `sources.json` with:
- Original author/creator
- Publication or collection information
- License and usage rights
- Access dates and URLs

---

## 🛠️ Maintenance

### Update Schedule
- **Continuous:** Bug fixes and corrections
- **Quarterly:** Statistics updates and validation
- **Annual:** Major reviews and enhancements

### Quality Assurance
- Automated validation checks
- Manual content review
- Cross-reference verification
- User feedback incorporation

### Contact & Support

For questions, issues, or contributions:
- Review the changelog for version history
- Check statistics for dataset coverage
- Consult sources for attribution details
- Report issues through project channels

---

## 📄 License

**Dataset License:** Educational Use  
**Metadata License:** CC0 1.0 Universal (Public Domain)

Metadata files in this directory are released under CC0, allowing unrestricted use. Source data licenses vary by persona and are detailed in `sources.json`.

---

## 🔗 Related Documentation

- **Dataset Root:** `../README.md` - Main dataset documentation
- **Per-Persona READMEs:** Individual persona documentation
- **Data Collection Standards:** `../DATA_COLLECTION_STANDARDS.md`
- **Verification Report:** `../../VERIFICATION_REPORT.md`

---

**Last Updated:** 2025-10-04  
**Metadata Version:** 1.0.0  
**Status:** ✅ Complete and Production Ready