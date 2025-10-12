"""
Figure 3.4: Complete Du Fu poem chunk visualization
Shows six-layer structure with color-coded relationships

Apple iWork Color Scheme maintained throughout
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import textwrap

# Apple iWork color palette
COLORS = {
    'layer1': '#FF6B35',  # Classical Chinese - Du Fu orange
    'layer2': '#FF9500',  # Pinyin - Warning orange
    'layer3': '#34C759',  # Modern Chinese - Success green
    'layer4': '#007AFF',  # English - Musk blue
    'layer5': '#AF52DE',  # Allusions - Queen purple
    'layer6': '#8E8E93',  # Historical context - Medium gray
    'bg_light': '#F2F2F7',
    'bg_dark': '#E5E5EA',
    'text_dark': '#1C1C1E',
    'text_medium': '#636366',
    'connection': '#D1D1D6'
}

# Sample Du Fu poem chunk (simplified for visualization)
poem_data = {
    'Classical Chinese': {
        'color': COLORS['layer1'],
        'content': '國破山河在\n城春草木深\n感時花濺淚\n恨別鳥驚心',
        'label': 'Layer 1: Classical Chinese (原文)'
    },
    'Pinyin': {
        'color': COLORS['layer2'],
        'content': 'guó pò shān hé zài\nchéng chūn cǎo mù shēn\ngǎn shí huā jiàn lèi\nhèn bié niǎo jīng xīn',
        'label': 'Layer 2: Pinyin Romanization (拼音)'
    },
    'Modern Chinese': {
        'color': COLORS['layer3'],
        'content': '国家破碎但山河依旧\n城中春深草木繁茂\n感伤时局看花流泪\n痛恨离别听鸟惊心',
        'label': 'Layer 3: Modern Chinese Translation (现代译文)'
    },
    'English': {
        'color': COLORS['layer4'],
        'content': 'The nation is broken, yet mountains and rivers remain\nSpring in the city, grass and trees grow deep\nFeeling the times, even flowers bring tears\nHating separation, birds startle the heart',
        'label': 'Layer 4: English Translation'
    },
    'Allusions': {
        'color': COLORS['layer5'],
        'content': '• "國破" alludes to An Lushan Rebellion (755-763)\n• "山河在" echoes natural permanence vs. human impermanence\n• "草木深" suggests abandoned capital overgrown\n• Poem exemplifies Tang "regulated verse" (律詩) form',
        'label': 'Layer 5: Allusion Annotations (典故注释)'
    },
    'Historical Context': {
        'color': COLORS['layer6'],
        'content': 'Composed: Spring 757 CE\nLocation: Chang\'an (长安), occupied by rebels\nDu Fu\'s situation: Held captive in occupied capital\nHistorical significance: Masterpiece of Tang Dynasty war poetry, expressing personal anguish amid national crisis',
        'label': 'Layer 6: Historical Context (历史背景)'
    }
}

fig, ax = plt.subplots(figsize=(16, 13))
ax.set_xlim(0, 16)
ax.set_ylim(0, 20)
ax.axis('off')

# Title
ax.text(8, 19, 'Multi-Layered Du Fu Poem Chunk Structure', 
        fontsize=18, fontweight='bold', ha='center', color=COLORS['text_dark'])

ax.text(8, 18.2, 'Poem: 春望 (Spring View) — Chunk ID: dufu_0409_001', 
        fontsize=12, ha='center', color=COLORS['text_medium'], style='italic')

# Draw layers
y_start = 16.5
layer_height = 2.5
layer_gap = 0.3
x_left = 1
width = 14

layers_order = [
    'Classical Chinese', 'Pinyin', 'Modern Chinese', 
    'English', 'Allusions', 'Historical Context'
]

for i, layer_name in enumerate(layers_order):
    layer = poem_data[layer_name]
    y_pos = y_start - i * (layer_height + layer_gap)
    
    # Layer box
    box = FancyBboxPatch((x_left, y_pos - layer_height), width, layer_height,
                        boxstyle="round,pad=0.08",
                        facecolor=layer['color'], 
                        edgecolor='white',
                        linewidth=3, 
                        alpha=0.2)
    ax.add_patch(box)
    
    # Layer label (tab-like header)
    label_width = 6
    label_height = 0.5
    label_box = Rectangle((x_left, y_pos - 0.05), label_width, label_height,
                          facecolor=layer['color'], 
                          edgecolor='white',
                          linewidth=2, alpha=0.9)
    ax.add_patch(label_box)
    
    ax.text(x_left + label_width/2, y_pos + 0.2, layer['label'],
           fontsize=10, fontweight='bold', ha='center', va='center',
           color='white')
    
    # Content
    content_wrapped = layer['content']
    ax.text(x_left + 0.4, y_pos - layer_height/2, content_wrapped,
           fontsize=9.5, va='center', color=COLORS['text_dark'],
           linespacing=1.6,
           family='Arial Unicode MS' if i < 3 else 'Arial')
    
    # Connection line to next layer
    if i < len(layers_order) - 1:
        line_x = x_left + width/2
        line_y_start = y_pos - layer_height - 0.05
        line_y_end = y_pos - layer_height - layer_gap + 0.05
        ax.plot([line_x, line_x], [line_y_start, line_y_end],
               color=COLORS['connection'], linewidth=2, linestyle='--', alpha=0.5)

# Add metadata box at bottom
metadata_y = 0.8
metadata_box = Rectangle((1, metadata_y), 14, 1.2,
                         facecolor=COLORS['bg_light'],
                         edgecolor=COLORS['bg_dark'],
                         linewidth=2)
ax.add_patch(metadata_box)

metadata_text = 'Metadata: persona_id=dufu | document_id=poem_0409 | chunk_id=dufu_0409_001 | composition_date=757 CE | genre=Poetry (五言律詩) | themes=war, displacement, loyalty'
wrapped_metadata = textwrap.fill(metadata_text, width=110)
ax.text(8, 1.4, wrapped_metadata,
       fontsize=8.5, ha='center', va='center', color=COLORS['text_medium'],
       linespacing=1.5)

# Add annotation explaining the structure
annotation_text = 'Each chunk integrates multiple layers enabling:\n• Character-level matching (Layer 1)\n• Phonetic search (Layer 2)\n• Semantic retrieval across languages (Layers 3-4)\n• Cultural context understanding (Layers 5-6)'
ax.text(15.5, 8, annotation_text,
       fontsize=8, ha='left', va='center', color=COLORS['text_medium'],
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                edgecolor=COLORS['bg_dark'], linewidth=1.5),
       linespacing=1.6)

plt.tight_layout()
plt.savefig('../../figures/figure_3_4_poem_chunk_structure.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Figure 3.4 saved: living-voices-dataset/figures/figure_3_4_poem_chunk_structure.png")
plt.close()
