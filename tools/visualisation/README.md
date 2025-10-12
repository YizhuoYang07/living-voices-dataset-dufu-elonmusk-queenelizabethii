# Visualization Tools for Living Voices Dataset Report

## Overview

This directory contains Python visualization scripts developed to generate publication-quality figures for Section 3 (Data Sources) of the AT2 technical report. All scripts utilize matplotlib for programmatic figure generation, ensuring consistency across visualizations and reproducibility of graphical outputs.

## Color Palette Specification

All visualizations implement a consistent color scheme to maintain visual coherence across figures and facilitate persona identification:

| Element | Color Name | Hex Code | Application |
|---------|-----------|----------|-------------|
| Du Fu (杜甫) | Deep Orange | `#FF6B35` | Classical Chinese historical content |
| Elon Musk | Bright Blue | `#007AFF` | Contemporary English content |
| Queen Elizabeth II | Royal Purple | `#AF52DE` | Formal English content |
| Background (Light) | Soft Gray | `#F2F2F7` | Primary backgrounds |
| Background (Dark) | Medium Gray | `#E5E5EA` | Borders and dividers |
| Text (Primary) | Near Black | `#1C1C1E` | Main text elements |
| Text (Secondary) | Medium Gray | `#636366` | Supporting text |

### Multi-Layer Color Mapping (Figure 3.4)

| Layer | Content Type | Hex Code | Description |
|-------|-------------|----------|-------------|
| 1 | Classical Chinese | `#FF6B35` | Original text |
| 2 | Pinyin Romanization | `#FF9500` | Phonetic transcription |
| 3 | Modern Chinese | `#34C759` | Contemporary translation |
| 4 | English Translation | `#007AFF` | English rendering |
| 5 | Allusion Annotations | `#AF52DE` | Cultural references |
| 6 | Historical Context | `#8E8E93` | Contextual information |

## Figure Descriptions

### Figure 3.1: Hierarchical Data Structure Diagram

**Script:** `figure_3_1_hierarchical_structure.py`  
**Output:** `living-voices-dataset/figures/figure_3_1_hierarchical_structure.png`  
**Dimensions:** 14" × 9" (4200 × 2700 pixels at 300 DPI)

Illustrates the three-tier hierarchical transformation from raw data sources through structured document organization to training-ready chunks. Each tier displays volume metrics differentiated by persona using the established color scheme.

**Report Placement:** Section 3.1, following the paragraph concluding "...across such vast time spans (Bamman & Smith, 2012; Lewis et al., 2020)."

**Visual Elements:**
- Three horizontal layers representing successive data transformation stages
- Color-coded rectangular elements indicating persona-specific volumes
- Directional arrows depicting data flow progression
- Marginal annotations identifying transformation processes

---

### Figure 3.2: Metadata Schema Comparison

**Script:** `figure_3_2_metadata_records.py`  
**Output:** `living-voices-dataset/figures/figure_3_2_metadata_records.png`  
**Dimensions:** 18" × 10" (5400 × 3000 pixels at 300 DPI)

Presents complete metadata records for representative chunks from each persona, demonstrating schema adaptation across diverse genres and historical periods. Metadata fields are organized by category (Identifiers, Temporal, Linguistic, Provenance) to highlight structural consistency despite content variation.

**Report Placement:** Section 3.1, immediately following Table 3.2 (Metadata Schema Architecture)

**Visual Elements:**
- Three parallel panels presenting persona-specific metadata
- Categorical field groupings with hierarchical organization
- Authentic metadata values demonstrating real-world application
- Persona-coordinated header coloring

---

### Figure 3.3: Data Collection Pipeline Comparison

**Script:** `figure_3_3_collection_pipelines.py`  
**Output:** `living-voices-dataset/figures/figure_3_3_collection_pipelines.png`  
**Dimensions:** 16" × 12" (4800 × 3600 pixels at 300 DPI)

Contrasts data collection methodologies for historical (Du Fu) versus contemporary (Musk, Elizabeth II) personas through parallel pipeline visualizations. Each pipeline encompasses five sequential stages: source identification, automated extraction, manual verification, content structuring/annotation enrichment, and quality validation.

**Report Placement:** Section 3.2, following the sentence "This achieved 99.5% extraction accuracy."

**Visual Elements:**
- Dual parallel pipelines distinguished by persona coloring
- Five-stage sequential representation per pipeline
- Methodology descriptions and quantitative outcomes per stage
- Directional arrows indicating process flow
- Explicit visualization of methodological divergence between historical and contemporary approaches

---

### Figure 3.4: Multi-Layer Chunk Architecture

**Script:** `figure_3_4_poem_chunk_structure.py`  
**Output:** `living-voices-dataset/figures/figure_3_4_poem_chunk_structure.png`  
**Dimensions:** 16" × 13" (4800 × 3900 pixels at 300 DPI)

Visualizes the six-layer architectural structure of a Du Fu poem chunk using "春望" (Spring View) as an exemplar. Demonstrates the integration of original text, phonetic transcription, translations, cultural annotations, and historical contextualization within a single retrievable unit.

**Report Placement:** Section 3.3, following the paragraph concluding "...rather than character-exact matching."

**Visual Elements:**
- Six vertically stacked layers with distinct color coding
- Complete poem content across all linguistic and contextual layers
- Tab-style headers identifying each layer's function
- Inter-layer connection indicators
- Explanatory annotation detailing retrieval capabilities
- Footer displaying chunk-level metadata

## Installation and Execution

### System Requirements

The visualization scripts require the following Python packages:
- `matplotlib >= 3.5.0`
- `numpy >= 1.20.0`

Installation via pip:
```bash
pip install matplotlib numpy
```

### Generating All Figures

Execute the master script to generate all four figures sequentially:

```bash
cd living-voices-dataset/tools/visualisation
python generate_all_figures.py
```

The master script performs the following operations:
1. Verifies or creates the output directory (`living-voices-dataset/figures/`)
2. Executes all four visualization scripts in sequence
3. Generates PNG output files at 300 DPI resolution
4. Reports generation status and output locations

### Generating Individual Figures

Individual figures may be generated independently:

```bash
cd living-voices-dataset/tools/visualisation
python figure_3_1_hierarchical_structure.py
python figure_3_2_metadata_records.py
python figure_3_3_collection_pipelines.py
python figure_3_4_poem_chunk_structure.py
```

## Directory Structure

```
living-voices-dataset/
├── tools/visualisation/
│   ├── README.md                              # Documentation (this file)
│   ├── generate_all_figures.py                # Master generation script
│   ├── figure_3_1_hierarchical_structure.py   # Figure 3.1 generator
│   ├── figure_3_2_metadata_records.py         # Figure 3.2 generator
│   ├── figure_3_3_collection_pipelines.py     # Figure 3.3 generator
│   └── figure_3_4_poem_chunk_structure.py     # Figure 3.4 generator
│
└── figures/                                   # Output directory
    ├── figure_3_1_hierarchical_structure.png  # Generated Figure 3.1
    ├── figure_3_2_metadata_records.png        # Generated Figure 3.2
    ├── figure_3_3_collection_pipelines.png    # Generated Figure 3.3
    └── figure_3_4_poem_chunk_structure.png    # Generated Figure 3.4
```

## Design Specifications

### Core Principles

1. **Visual Consistency:** Uniform color scheme, typography, and layout conventions across all figures
2. **Clarity and Legibility:** High-contrast color selections, appropriate font sizing, and unambiguous labeling
3. **Professional Aesthetic:** Clean design adhering to modern visualization standards
4. **Academic Standards:** Publication-quality output suitable for formal technical documentation
5. **High Resolution:** 300 DPI output for print reproduction quality
6. **Accessibility Compliance:** Color palette selected for color vision deficiency compatibility

### Technical Specifications

| Figure | Dimensions (inches) | Resolution | Approximate File Size |
|--------|-------------------|------------|---------------------|
| 3.1 | 14 × 9 | 300 DPI | 500 KB |
| 3.2 | 18 × 10 | 300 DPI | 600 KB |
| 3.3 | 16 × 12 | 300 DPI | 700 KB |
| 3.4 | 16 × 13 | 300 DPI | 650 KB |

## Customization

### Modifying Color Scheme

Color values may be modified by editing the `COLORS` dictionary in each script:

```python
COLORS = {
    'dufu': '#FF6B35',      # Du Fu persona color
    'musk': '#007AFF',      # Elon Musk persona color
    'queen': '#AF52DE',     # Queen Elizabeth II persona color
    # Additional color definitions...
}
```

### Adjusting Figure Dimensions

Figure dimensions may be adjusted via the `figsize` parameter:

```python
fig, ax = plt.subplots(figsize=(14, 9))  # Width × Height in inches
```

Note: Dimension modifications may require adjustment of text sizes and element spacing to maintain visual balance.

## Output Characteristics

Generated figures are optimized for multiple use cases:

- **Print Publication:** 300 DPI resolution ensures high-quality reproduction
- **Digital Distribution:** PNG format provides lossless compression with broad compatibility
- **Presentation Materials:** Suitable dimensions and resolution for poster and slide integration
- **Technical Documentation:** Publication-ready quality for academic reports and papers

## Technical Notes

All scripts utilize matplotlib's object-oriented API for precise control over figure elements. Color specifications follow hexadecimal RGB notation for exact color reproduction. Generated figures use PNG format to preserve visual fidelity without compression artifacts.

---

**Project:** Living Voices Dataset  
**Course:** UTS 36118 Applied Natural Language Processing  
**Assignment:** AT2 Part B - Group Project Technical Report  
**Academic Year:** 2024
