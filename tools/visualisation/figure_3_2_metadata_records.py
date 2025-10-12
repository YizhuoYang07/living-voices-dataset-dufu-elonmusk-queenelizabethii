"""
Figure 3.2: Side-by-side metadata record visualization
Shows metadata schema adaptation across three personas

Apple iWork Color Scheme maintained throughout
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import textwrap

# Apple iWork color palette
COLORS = {
    'dufu': '#FF6B35',
    'musk': '#007AFF', 
    'queen': '#AF52DE',
    'bg_light': '#F2F2F7',
    'bg_dark': '#E5E5EA',
    'text_dark': '#1C1C1E',
    'text_medium': '#636366',
    'field_bg': '#FFFFFF'
}

# Sample metadata for each persona
metadata_samples = {
    'Du Fu': {
        'color': COLORS['dufu'],
        'fields': [
            ('persona_id', 'dufu'),
            ('document_id', 'poem_1234'),
            ('chunk_id', 'dufu_1234_001'),
            ('composition_date', '757 CE'),
            ('historical_context', 'An Lushan Rebellion'),
            ('language', 'lzh (Classical Chinese)'),
            ('genre', 'Poetry (七言律詩)'),
            ('themes', 'war, displacement, loyalty'),
            ('source_url', 'Tang-Song Literature DB'),
            ('collection_date', '2024-09-15'),
            ('license', 'Public Domain'),
            ('reliability_tier', 'Tier 1 (Scholarly)')
        ]
    },
    'Elon Musk': {
        'color': COLORS['musk'],
        'fields': [
            ('persona_id', 'elon_musk'),
            ('document_id', 'biography_tesla'),
            ('chunk_id', 'musk_bio_042'),
            ('composition_date', '2023-06-12'),
            ('historical_context', 'SpaceX/Tesla Era'),
            ('language', 'eng (English)'),
            ('genre', 'Biography'),
            ('themes', 'innovation, space, EV'),
            ('source_url', 'Wikipedia CC BY-SA 3.0'),
            ('collection_date', '2024-10-02'),
            ('license', 'CC BY-SA 3.0'),
            ('reliability_tier', 'Tier 2 (Community)')
        ]
    },
    'Queen Elizabeth II': {
        'color': COLORS['queen'],
        'fields': [
            ('persona_id', 'queen_elizabeth_ii'),
            ('document_id', 'speech_jubilee'),
            ('chunk_id', 'queen_speech_015'),
            ('composition_date', '2012-06-05'),
            ('historical_context', 'Diamond Jubilee'),
            ('language', 'eng (English)'),
            ('genre', 'Formal Speech'),
            ('themes', 'service, duty, unity'),
            ('source_url', 'Wikipedia CC BY-SA 3.0'),
            ('collection_date', '2024-10-01'),
            ('license', 'CC BY-SA 3.0'),
            ('reliability_tier', 'Tier 2 (Community)')
        ]
    }
}

fig, axes = plt.subplots(1, 3, figsize=(18, 10))
fig.suptitle('Metadata Schema Across Three Personas', 
             fontsize=18, fontweight='bold', y=0.98, color=COLORS['text_dark'])

for ax, (persona, data) in zip(axes, metadata_samples.items()):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Persona header
    header = Rectangle((0.5, 14.2), 9, 1.3, 
                       facecolor=data['color'], 
                       edgecolor='white', linewidth=2, alpha=0.85)
    ax.add_patch(header)
    ax.text(5, 14.85, persona, fontsize=16, fontweight='bold', 
            ha='center', va='center', color='white')
    
    # Metadata fields
    y_position = 13.5
    field_height = 0.9
    gap = 0.2
    
    # Category groupings
    categories = {
        'Identifiers': ['persona_id', 'document_id', 'chunk_id'],
        'Temporal': ['composition_date', 'historical_context'],
        'Linguistic': ['language', 'genre', 'themes'],
        'Provenance': ['source_url', 'collection_date', 'license', 'reliability_tier']
    }
    
    for category, field_names in categories.items():
        # Category label
        ax.text(0.7, y_position + 0.2, category, 
               fontsize=10, fontweight='bold', color=data['color'], va='top')
        y_position -= 0.6
        
        # Fields in this category
        for field_name, field_value in data['fields']:
            if field_name in field_names:
                # Field background
                field_box = Rectangle((1, y_position - field_height), 8.5, field_height,
                                     facecolor=COLORS['field_bg'], 
                                     edgecolor=COLORS['bg_dark'], linewidth=1.5)
                ax.add_patch(field_box)
                
                # Field name (bold)
                ax.text(1.3, y_position - 0.25, field_name + ':', 
                       fontsize=9, fontweight='bold', va='center',
                       color=COLORS['text_dark'])
                
                # Field value (wrapped if needed)
                wrapped_value = textwrap.fill(field_value, width=25)
                ax.text(5.5, y_position - 0.45, wrapped_value,
                       fontsize=8, va='center', color=COLORS['text_medium'])
                
                y_position -= (field_height + gap)
        
        y_position -= 0.3  # Extra gap between categories

plt.tight_layout()
plt.savefig('../../figures/figure_3_2_metadata_records.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Figure 3.2 saved: living-voices-dataset/figures/figure_3_2_metadata_records.png")
plt.close()
