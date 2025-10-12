"""
Figure 3.1: Three-tier hierarchical data structure diagram
Visualizes Raw Data → Structured Documents → Training Chunks with persona color-coding

Apple iWork Color Scheme:
- Du Fu: #FF6B35 (Deep Orange)
- Elon Musk: #007AFF (Bright Blue)
- Queen Elizabeth II: #AF52DE (Royal Purple)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

# Apple iWork color palette
COLORS = {
    'dufu': '#FF6B35',
    'musk': '#007AFF', 
    'queen': '#AF52DE',
    'bg_light': '#F2F2F7',
    'bg_dark': '#E5E5EA',
    'text_dark': '#1C1C1E',
    'text_medium': '#636366',
    'arrow': '#8E8E93'
}

# Data - CORRECTED
data = {
    'Du Fu': {
        'documents': 1496,
        'chunks': 3449,
        'content': '431,083 chars',
        'color': COLORS['dufu']
    },
    'Elon Musk': {
        'documents': 48,
        'chunks': 96,
        'content': '321,176 words',
        'color': COLORS['musk']
    },
    'Queen Elizabeth II': {
        'documents': 22,
        'chunks': 341,
        'content': '13,405 words',
        'color': COLORS['queen']
    }
}

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(8, 9.5, 'Hierarchical Data Structure: Living Voices Dataset', 
        fontsize=20, fontweight='bold', ha='center', color=COLORS['text_dark'])

# Three layers with proper spacing
layers = [
    {'y': 7.8, 'label': 'Layer 1: Raw Data Sources', 'desc': 'Original collected materials'},
    {'y': 5.2, 'label': 'Layer 2: Structured Documents', 'desc': 'Organized with metadata'},
    {'y': 2.6, 'label': 'Layer 3: Training Chunks', 'desc': 'Segmented for RAG system'}
]

personas = ['Du Fu', 'Elon Musk', 'Queen Elizabeth II']
x_positions = [2.5, 8, 13.5]

# Draw each layer
for layer_idx, layer_info in enumerate(layers):
    y_center = layer_info['y']
    
    # Layer background box
    layer_bg = Rectangle((0.3, y_center - 0.9), 15.4, 1.8,
                         facecolor=COLORS['bg_light'],
                         edgecolor=COLORS['bg_dark'],
                         linewidth=2.5,
                         zorder=0)
    ax.add_patch(layer_bg)
    
    # Layer title (left side)
    ax.text(0.6, y_center + 0.6, layer_info['label'],
           fontsize=13, fontweight='bold', va='top',
           color=COLORS['text_dark'])
    
    ax.text(0.6, y_center + 0.3, layer_info['desc'],
           fontsize=10, va='top', style='italic',
           color=COLORS['text_medium'])
    
    # Draw persona boxes for this layer
    for persona_idx, (persona, x_pos) in enumerate(zip(personas, x_positions)):
        color = data[persona]['color']
        
        # Determine what to show based on layer
        if layer_idx == 0:  # Raw Data - show document count
            main_value = data[persona]['documents']
            label = 'Documents'
            sublabel = data[persona]['content']
        elif layer_idx == 1:  # Structured Documents - show document count
            main_value = data[persona]['documents']
            label = 'Documents'
            sublabel = 'with metadata'
        else:  # Training Chunks - show chunk count
            main_value = data[persona]['chunks']
            label = 'Chunks'
            sublabel = 'training-ready'
        
        # Box dimensions
        box_width = 3.2
        box_height = 1.3
        
        # Draw persona box
        persona_box = FancyBboxPatch(
            (x_pos - box_width/2, y_center - box_height/2),
            box_width, box_height,
            boxstyle="round,pad=0.08",
            facecolor=color,
            edgecolor='white',
            linewidth=3,
            alpha=0.9,
            zorder=2
        )
        ax.add_patch(persona_box)
        
        # Persona name (at top of first layer only)
        if layer_idx == 0:
            ax.text(x_pos, y_center + 1.15, persona,
                   fontsize=11, fontweight='bold', ha='center',
                   color=color,
                   bbox=dict(boxstyle='round,pad=0.4', 
                           facecolor='white',
                           edgecolor=color,
                           linewidth=2))
        
        # Main number (large)
        ax.text(x_pos, y_center + 0.15, f'{main_value:,}',
               fontsize=18, fontweight='bold', ha='center', va='center',
               color='white', zorder=3)
        
        # Label (what the number represents)
        ax.text(x_pos, y_center - 0.25, label,
               fontsize=11, ha='center', va='center',
               color='white', alpha=0.9, zorder=3)
        
        # Sublabel (additional info)
        ax.text(x_pos, y_center - 0.48, sublabel,
               fontsize=8, ha='center', va='center',
               color='white', alpha=0.8, style='italic', zorder=3)
    
    # Draw arrows to next layer
    if layer_idx < len(layers) - 1:
        y_from = y_center - 1.0
        y_to = layers[layer_idx + 1]['y'] + 1.0
        
        for x_pos in x_positions:
            arrow = FancyArrowPatch(
                (x_pos, y_from), (x_pos, y_to),
                arrowstyle='->', mutation_scale=30,
                linewidth=3, color=COLORS['arrow'],
                alpha=0.5, zorder=1
            )
            ax.add_patch(arrow)
            
        # Process label between layers
        process_y = (y_from + y_to) / 2
        if layer_idx == 0:
            process_text = 'Collection &\nValidation'
        else:
            process_text = 'Segmentation &\nChunking'
            
        ax.text(15.5, process_y, process_text,
               fontsize=9, ha='center', va='center',
               color=COLORS['text_medium'],
               bbox=dict(boxstyle='round,pad=0.4',
                        facecolor='white',
                        edgecolor=COLORS['bg_dark'],
                        linewidth=1.5))

# Summary statistics at bottom
summary_y = 0.8
ax.text(8, summary_y, 'Total Dataset: 1,566 documents → 1,566 structured documents → 3,886 training chunks',
       fontsize=12, ha='center', fontweight='bold',
       color=COLORS['text_dark'],
       bbox=dict(boxstyle='round,pad=0.5',
                facecolor=COLORS['bg_light'],
                edgecolor=COLORS['bg_dark'],
                linewidth=2))

# Legend
legend_y = 0.15
legend_elements = []
for persona in personas:
    patch = mpatches.Patch(color=data[persona]['color'], 
                          label=f"{persona}: {data[persona]['documents']} docs, {data[persona]['chunks']} chunks",
                          alpha=0.9)
    legend_elements.append(patch)

legend = ax.legend(handles=legend_elements, 
                  loc='upper center',
                  bbox_to_anchor=(0.5, 0.02),
                  ncol=3,
                  frameon=True,
                  fancybox=True,
                  fontsize=10,
                  edgecolor=COLORS['bg_dark'])
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.95)

plt.tight_layout()
plt.savefig('../../figures/figure_3_1_hierarchical_structure.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Figure 3.1 saved: living-voices-dataset/figures/figure_3_1_hierarchical_structure.png")
plt.close()
