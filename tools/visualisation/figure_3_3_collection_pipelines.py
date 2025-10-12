"""
Figure 3.3: Parallel collection pipeline flowcharts
Compares data collection pipelines for Du Fu vs. modern personas

Apple iWork Color Scheme maintained throughout
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import textwrap

# Apple iWork color palette
COLORS = {
    'dufu': '#FF6B35',
    'modern': '#007AFF',  # Using Musk's blue for "modern" category
    'bg_light': '#F2F2F7',
    'bg_dark': '#E5E5EA',
    'text_dark': '#1C1C1E',
    'text_medium': '#636366',
    'success': '#34C759',
    'warning': '#FF9500',
    'arrow': '#8E8E93'
}

# Pipeline stages
dufu_pipeline = [
    {
        'stage': 'Source\nIdentification',
        'content': 'Tang-Song Literature\nChronological Map\nDatabase',
        'method': 'Scholarly editions\n(Quan Tang Shi)',
        'output': '1,496 poems'
    },
    {
        'stage': 'Automated\nExtraction',
        'content': 'XML parsing\nCharacter encoding\nvalidation',
        'method': 'Custom Python\nscripts',
        'output': '431,083 chars'
    },
    {
        'stage': 'Manual\nVerification',
        'content': '10% sample\nvalidation against\nprint editions',
        'method': 'Cross-reference\nwith Owen (2016)',
        'output': '99.5% accuracy'
    },
    {
        'stage': 'Annotation\nEnrichment',
        'content': 'Allusions\nHistorical context\nTranslations',
        'method': 'Multi-layer\nintegration',
        'output': '600,000+ chars'
    },
    {
        'stage': 'Quality\nValidation',
        'content': 'Schema compliance\nDuplicate detection\nCompleteness check',
        'method': 'JSON validation\nFuzzy matching',
        'output': '100% complete'
    }
]

modern_pipeline = [
    {
        'stage': 'Source\nIdentification',
        'content': 'Wikipedia\n(CC BY-SA 3.0)\nPublic databases',
        'method': 'API access\nWeb scraping',
        'output': '70 documents'
    },
    {
        'stage': 'Automated\nExtraction',
        'content': 'HTML parsing\nText extraction\nMetadata capture',
        'method': 'BeautifulSoup\nwikipediaapi',
        'output': '334,581 words'
    },
    {
        'stage': 'Manual\nVerification',
        'content': '15% sample\nvalidation for\naccuracy',
        'method': 'Fact-checking\nagainst sources',
        'output': '2.3% error rate'
    },
    {
        'stage': 'Content\nStructuring',
        'content': 'Paragraph seg.\nSemantic chunking\nContext windows',
        'method': 'NLP-based\nsegmentation',
        'output': '437 chunks'
    },
    {
        'stage': 'Quality\nValidation',
        'content': 'Schema compliance\nCopyright check\nTemporal bounds',
        'method': 'Automated +\nmanual review',
        'output': '100% compliant'
    }
]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

# Title
fig.suptitle('Data Collection Pipelines: Historical vs. Contemporary Sources', 
             fontsize=18, fontweight='bold', y=0.98, color=COLORS['text_dark'])

# Function to draw pipeline
def draw_pipeline(ax, pipeline, color, title):
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Pipeline title
    ax.text(8.5, 4.5, title, fontsize=15, fontweight='bold', 
            ha='center', color=color)
    
    stage_width = 2.8
    stage_height = 3.2
    x_start = 0.5
    x_gap = 0.3
    
    for i, stage in enumerate(pipeline):
        x_pos = x_start + i * (stage_width + x_gap)
        
        # Stage box
        box = FancyBboxPatch((x_pos, 0.3), stage_width, stage_height,
                            boxstyle="round,pad=0.1",
                            facecolor=color, 
                            edgecolor='white',
                            linewidth=2.5, 
                            alpha=0.15)
        ax.add_patch(box)
        
        # Stage header
        header = Rectangle((x_pos, 3.1), stage_width, 0.4,
                          facecolor=color, edgecolor='white', 
                          linewidth=2, alpha=0.85)
        ax.add_patch(header)
        ax.text(x_pos + stage_width/2, 3.3, stage['stage'],
               fontsize=9, fontweight='bold', ha='center', va='center',
               color='white')
        
        # Content section
        content_wrapped = textwrap.fill(stage['content'], width=18)
        ax.text(x_pos + stage_width/2, 2.3, content_wrapped,
               fontsize=7.5, ha='center', va='center', 
               color=COLORS['text_dark'],
               linespacing=1.5)
        
        # Method section (lighter background)
        method_bg = Rectangle((x_pos + 0.1, 1.2), stage_width - 0.2, 0.8,
                             facecolor=COLORS['bg_light'], 
                             edgecolor=COLORS['bg_dark'], linewidth=1)
        ax.add_patch(method_bg)
        
        method_wrapped = textwrap.fill(stage['method'], width=18)
        ax.text(x_pos + stage_width/2, 1.6, method_wrapped,
               fontsize=7, ha='center', va='center',
               color=COLORS['text_medium'], style='italic',
               linespacing=1.4)
        
        # Output label
        output_bg = Rectangle((x_pos + 0.15, 0.4), stage_width - 0.3, 0.5,
                             facecolor='white', 
                             edgecolor=color, linewidth=1.5)
        ax.add_patch(output_bg)
        
        ax.text(x_pos + stage_width/2, 0.65, stage['output'],
               fontsize=7.5, fontweight='bold', ha='center', va='center',
               color=color)
        
        # Arrow to next stage
        if i < len(pipeline) - 1:
            arrow = FancyArrowPatch(
                (x_pos + stage_width + 0.05, 2),
                (x_pos + stage_width + x_gap - 0.05, 2),
                arrowstyle='->', mutation_scale=25, 
                linewidth=3, color=COLORS['arrow'], alpha=0.6
            )
            ax.add_patch(arrow)

# Draw both pipelines
draw_pipeline(ax1, dufu_pipeline, COLORS['dufu'], 
             'Du Fu (杜甫) — Classical Chinese Poetry Pipeline')
draw_pipeline(ax2, modern_pipeline, COLORS['modern'], 
             'Modern Personas (Musk & Elizabeth II) — Contemporary Text Pipeline')

plt.tight_layout()
plt.savefig('../../figures/figure_3_3_collection_pipelines.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Figure 3.3 saved: living-voices-dataset/figures/figure_3_3_collection_pipelines.png")
plt.close()
