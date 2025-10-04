#!/usr/bin/env python3
"""
Du Fu Data Extraction from CNKGraph.Writings.xml
Extract and process Du Fu poems from the Tang-Song Literature XML database
for RAG-based dialogue system training.

Author: Living Voices Dataset Project
Date: 2025-10-04
"""

import xml.etree.ElementTree as ET
import json
import csv
from datetime import datetime
from collections import defaultdict
import os


class DuFuXMLExtractor:
    """
    Extracts Du Fu poems from CNKGraph.Writings.xml (1.7GB, 1.6M poems)
    and processes them for RAG system training.
    """
    
    def __init__(self, xml_file_path, output_dir):
        """
        Initialize the extractor.
        
        Args:
            xml_file_path: Path to CNKGraph.Writings.xml
            output_dir: Directory for output files
        """
        self.xml_file_path = xml_file_path
        self.output_dir = output_dir
        
        # Statistics
        self.stats = {
            'total_poems_scanned': 0,
            'dufu_poems_found': 0,
            'dufu_author_id': None,
            'start_time': datetime.now()
        }
        
        # Du Fu data collections
        self.dufu_poems = []
        self.dufu_metadata = {}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_all_dufu_poems(self):
        """
        Main extraction method - iteratively parse XML and extract Du Fu poems.
        """
        print("=" * 80)
        print("Du Fu Poetry Extraction from CNKGraph.Writings.xml")
        print("=" * 80)
        print(f"XML File: {self.xml_file_path}")
        print(f"Output Directory: {self.output_dir}")
        print()
        
        if not os.path.exists(self.xml_file_path):
            raise FileNotFoundError(f"XML file not found: {self.xml_file_path}")
        
        print("Starting iterative XML parsing (memory-efficient for 1.7GB file)...")
        print()
        
        # Use iterparse for memory-efficient processing
        context = ET.iterparse(self.xml_file_path, events=("end",))
        
        for event, elem in context:
            if elem.tag == "Poem":
                self.stats['total_poems_scanned'] += 1
                
                # Check if this is a Du Fu poem
                author = elem.get('AU', '')
                if author == '杜甫':
                    poem_data = self._extract_poem_data(elem)
                    self.dufu_poems.append(poem_data)
                    self.stats['dufu_poems_found'] += 1
                    
                    # Store author ID
                    if not self.stats['dufu_author_id']:
                        self.stats['dufu_author_id'] = elem.get('AId', '')
                
                # Clear processed element to free memory
                elem.clear()
                
                # Progress report every 100K poems
                if self.stats['total_poems_scanned'] % 100000 == 0:
                    self._print_progress()
        
        print()
        print("=" * 80)
        print("Extraction Complete!")
        print(f"Total poems scanned: {self.stats['total_poems_scanned']:,}")
        print(f"Du Fu poems found: {self.stats['dufu_poems_found']:,}")
        print(f"Du Fu author ID: {self.stats['dufu_author_id']}")
        print("=" * 80)
        print()
        
        return self.dufu_poems
    
    def _extract_poem_data(self, poem_elem):
        """
        Extract comprehensive data from a single poem XML element.
        
        Args:
            poem_elem: XML Element representing a poem
            
        Returns:
            Dictionary containing all poem data
        """
        poem_data = {}
        
        # Basic metadata
        poem_data['poem_id'] = poem_elem.get('Id', '')
        poem_data['author'] = poem_elem.get('AU', '')
        poem_data['author_id'] = poem_elem.get('AId', '')
        poem_data['dynasty'] = poem_elem.get('D', '')
        
        # Temporal information
        poem_data['creation_date'] = poem_elem.get('AD', '')
        poem_data['group_number'] = poem_elem.get('G', '')
        
        # Spatial information
        poem_data['place_code'] = poem_elem.get('AP', '')
        
        # Literary characteristics
        poem_data['poem_type'] = poem_elem.get('T', '')
        poem_data['poem_type_detail'] = poem_elem.get('TD', '')
        poem_data['rhyme_category'] = poem_elem.get('R', '')
        poem_data['rhyme_number'] = poem_elem.get('RA', '')
        poem_data['final_rhyme'] = poem_elem.get('FR', '')
        poem_data['has_title'] = poem_elem.get('TS', '') == 'true'
        
        # Title extraction
        title_elem = poem_elem.find('Title')
        if title_elem is not None:
            poem_data['title'] = title_elem.get('C', '')
            poem_data['title_annotations'] = self._extract_annotations(title_elem.find('Ns'))
        else:
            poem_data['title'] = ''
            poem_data['title_annotations'] = []
        
        # Content extraction (lines)
        jus_elem = poem_elem.find('Jus')
        if jus_elem is not None:
            lines = []
            line_tones = []
            line_rhymes = []
            line_annotations = []
            
            for ju in jus_elem.findall('Ju'):
                lines.append(ju.get('C', ''))
                line_tones.append(ju.get('T', ''))
                line_rhymes.append(ju.get('R', ''))
                line_annotations.append(self._extract_annotations(ju.find('Ns')))
            
            poem_data['lines'] = lines
            poem_data['line_tones'] = line_tones
            poem_data['line_rhymes'] = line_rhymes
            poem_data['line_annotations'] = line_annotations
        else:
            poem_data['lines'] = []
            poem_data['line_tones'] = []
            poem_data['line_rhymes'] = []
            poem_data['line_annotations'] = []
        
        # Allusions (典故)
        as_elem = poem_elem.find('As')
        if as_elem is not None:
            allusions = []
            for a in as_elem.findall('A'):
                allusion = {
                    'allusion_id': a.get('AI', ''),
                    'sentence_index': a.get('SI', ''),
                    'text': a.text or ''
                }
                allusions.append(allusion)
            poem_data['allusions'] = allusions
        else:
            poem_data['allusions'] = []
        
        # Source books (文献来源)
        fs_elem = poem_elem.find('Fs')
        if fs_elem is not None:
            source_books = [f.text for f in fs_elem.findall('F') if f.text]
            poem_data['source_books'] = source_books
        else:
            poem_data['source_books'] = []
        
        # Extract all annotation types
        annotations_by_type = self._extract_annotations_by_type(poem_elem)
        poem_data['text_annotations'] = annotations_by_type['Text']
        poem_data['word_dict_annotations'] = annotations_by_type['WordDictInJson']
        poem_data['char_dict_annotations'] = annotations_by_type['CharDictInJson']
        poem_data['allusion_key_annotations'] = annotations_by_type['AllusionKey']
        poem_data['image_annotations'] = annotations_by_type['Image']
        
        # Sentence indices
        sis_elem = poem_elem.find('SIs')
        if sis_elem is not None:
            sentence_indices = []
            for si in sis_elem.findall('SI'):
                indices = [int(i.text) for i in si.findall('int') if i.text and i.text.isdigit()]
                sentence_indices.append(indices)
            poem_data['sentence_indices'] = sentence_indices
        else:
            poem_data['sentence_indices'] = []
        
        return poem_data
    
    def _extract_annotations(self, ns_elem):
        """
        Extract annotations from a Ns (Notes) element.
        
        Args:
            ns_elem: XML Element containing notes
            
        Returns:
            List of annotation dictionaries
        """
        annotations = []
        if ns_elem is not None:
            for n in ns_elem.findall('N'):
                annotation = {
                    'type': n.get('T', ''),
                    'index': n.get('I', ''),
                    'content': n.text or ''
                }
                annotations.append(annotation)
        return annotations
    
    def _extract_annotations_by_type(self, poem_elem):
        """
        Extract all annotations categorized by type.
        
        Args:
            poem_elem: XML Element representing a poem
            
        Returns:
            Dictionary with annotation types as keys
        """
        annotations = {
            'Text': [],
            'WordDictInJson': [],
            'CharDictInJson': [],
            'AllusionKey': [],
            'Image': []
        }
        
        for n in poem_elem.iter('N'):
            n_type = n.get('T', '')
            if n_type in annotations:
                annotation = {
                    'index': n.get('I', ''),
                    'content': n.text or ''
                }
                annotations[n_type].append(annotation)
        
        return annotations
    
    def _print_progress(self):
        """Print progress during extraction."""
        elapsed = (datetime.now() - self.stats['start_time']).total_seconds()
        rate = self.stats['total_poems_scanned'] / elapsed if elapsed > 0 else 0
        
        print(f"Progress: {self.stats['total_poems_scanned']:,} poems scanned | "
              f"{self.stats['dufu_poems_found']:,} Du Fu poems found | "
              f"{rate:.0f} poems/sec")
    
    def save_to_json(self, filename='dufu_poems_full.json'):
        """
        Save extracted poems to JSON file.
        
        Args:
            filename: Output JSON filename
        """
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'author': '杜甫',
                    'author_id': self.stats['dufu_author_id'],
                    'total_poems': len(self.dufu_poems),
                    'extraction_date': datetime.now().isoformat(),
                    'source': 'CNKGraph.Writings.xml'
                },
                'poems': self.dufu_poems
            }, f, ensure_ascii=False, indent=2)
        
        print(f"Saved JSON: {output_path}")
        print(f"  Total poems: {len(self.dufu_poems)}")
        return output_path
    
    def save_to_csv(self, filename='dufu_poems_structured.csv'):
        """
        Save extracted poems to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        output_path = os.path.join(self.output_dir, filename)
        
        if not self.dufu_poems:
            print("Warning: No poems to save")
            return None
        
        # Prepare rows for CSV (flatten nested structures)
        csv_rows = []
        for poem in self.dufu_poems:
            row = {
                'poem_id': poem['poem_id'],
                'title': poem['title'],
                'author': poem['author'],
                'author_id': poem['author_id'],
                'dynasty': poem['dynasty'],
                'creation_date': poem['creation_date'],
                'place_code': poem['place_code'],
                'poem_type': poem['poem_type'],
                'poem_type_detail': poem['poem_type_detail'],
                'rhyme_category': poem['rhyme_category'],
                'has_title': poem['has_title'],
                'line_count': len(poem['lines']),
                'full_text': '\n'.join(poem['lines']),
                'allusions_count': len(poem['allusions']),
                'source_books_count': len(poem['source_books']),
                'text_annotations_count': len(poem['text_annotations']),
                'lines_json': json.dumps(poem['lines'], ensure_ascii=False),
                'allusions_json': json.dumps(poem['allusions'], ensure_ascii=False),
                'source_books_json': json.dumps(poem['source_books'], ensure_ascii=False)
            }
            csv_rows.append(row)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
            writer.writeheader()
            writer.writerows(csv_rows)
        
        print(f"Saved CSV: {output_path}")
        print(f"  Total rows: {len(csv_rows)}")
        return output_path
    
    def generate_statistics(self):
        """
        Generate comprehensive statistics about extracted poems.
        
        Returns:
            Dictionary containing statistics
        """
        if not self.dufu_poems:
            return {}
        
        stats = {
            'total_poems': len(self.dufu_poems),
            'author_id': self.stats['dufu_author_id'],
            
            # Temporal analysis
            'creation_dates': defaultdict(int),
            'date_range': {'earliest': None, 'latest': None},
            
            # Spatial analysis
            'places': defaultdict(int),
            'unique_places': set(),
            
            # Literary analysis
            'poem_types': defaultdict(int),
            'poem_type_details': defaultdict(int),
            'rhyme_categories': defaultdict(int),
            
            # Content analysis
            'total_lines': 0,
            'poems_with_title': 0,
            'poems_with_allusions': 0,
            'poems_with_sources': 0,
            'poems_with_annotations': 0,
            
            # Annotation analysis
            'total_allusions': 0,
            'total_source_books': 0,
            'annotation_types': defaultdict(int)
        }
        
        for poem in self.dufu_poems:
            # Temporal
            if poem['creation_date']:
                stats['creation_dates'][poem['creation_date']] += 1
                if not stats['date_range']['earliest'] or poem['creation_date'] < stats['date_range']['earliest']:
                    stats['date_range']['earliest'] = poem['creation_date']
                if not stats['date_range']['latest'] or poem['creation_date'] > stats['date_range']['latest']:
                    stats['date_range']['latest'] = poem['creation_date']
            
            # Spatial
            if poem['place_code']:
                stats['places'][poem['place_code']] += 1
                stats['unique_places'].add(poem['place_code'])
            
            # Literary
            if poem['poem_type']:
                stats['poem_types'][poem['poem_type']] += 1
            if poem['poem_type_detail']:
                stats['poem_type_details'][poem['poem_type_detail']] += 1
            if poem['rhyme_category']:
                stats['rhyme_categories'][poem['rhyme_category']] += 1
            
            # Content
            stats['total_lines'] += len(poem['lines'])
            if poem['has_title']:
                stats['poems_with_title'] += 1
            if poem['allusions']:
                stats['poems_with_allusions'] += 1
                stats['total_allusions'] += len(poem['allusions'])
            if poem['source_books']:
                stats['poems_with_sources'] += 1
                stats['total_source_books'] += len(poem['source_books'])
            
            # Annotations
            annotation_types = ['text_annotations', 'word_dict_annotations', 
                              'char_dict_annotations', 'allusion_key_annotations']
            has_annotations = False
            for ann_type in annotation_types:
                if poem[ann_type]:
                    has_annotations = True
                    stats['annotation_types'][ann_type] += len(poem[ann_type])
            if has_annotations:
                stats['poems_with_annotations'] += 1
        
        # Convert sets and defaultdicts to regular dicts for JSON serialization
        stats['unique_places'] = len(stats['unique_places'])
        stats['creation_dates'] = dict(stats['creation_dates'])
        stats['places'] = dict(stats['places'])
        stats['poem_types'] = dict(stats['poem_types'])
        stats['poem_type_details'] = dict(stats['poem_type_details'])
        stats['rhyme_categories'] = dict(stats['rhyme_categories'])
        stats['annotation_types'] = dict(stats['annotation_types'])
        
        # Calculate averages
        stats['average_lines_per_poem'] = stats['total_lines'] / len(self.dufu_poems)
        stats['poems_with_title_percentage'] = (stats['poems_with_title'] / len(self.dufu_poems)) * 100
        stats['poems_with_allusions_percentage'] = (stats['poems_with_allusions'] / len(self.dufu_poems)) * 100
        
        return stats
    
    def save_statistics(self, filename='dufu_statistics.json'):
        """
        Save statistics to JSON file.
        
        Args:
            filename: Output JSON filename
        """
        stats = self.generate_statistics()
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"Saved statistics: {output_path}")
        self._print_statistics_summary(stats)
        return output_path
    
    def _print_statistics_summary(self, stats):
        """Print a summary of statistics."""
        print()
        print("=" * 80)
        print("Du Fu Poetry Statistics")
        print("=" * 80)
        print(f"Total poems: {stats['total_poems']:,}")
        print(f"Total lines: {stats['total_lines']:,}")
        print(f"Average lines per poem: {stats['average_lines_per_poem']:.1f}")
        print()
        print(f"Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        print(f"Unique time periods: {len(stats['creation_dates'])}")
        print(f"Unique places: {stats['unique_places']}")
        print()
        print(f"Poem types: {len(stats['poem_types'])}")
        print(f"Rhyme categories: {len(stats['rhyme_categories'])}")
        print()
        print(f"Poems with title: {stats['poems_with_title']} ({stats['poems_with_title_percentage']:.1f}%)")
        print(f"Poems with allusions: {stats['poems_with_allusions']} ({stats['poems_with_allusions_percentage']:.1f}%)")
        print(f"Total allusions: {stats['total_allusions']:,}")
        print(f"Total source books: {stats['total_source_books']:,}")
        print("=" * 80)


def main():
    """Main execution function."""
    
    # Configuration
    xml_file = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/du_fu/data/external/唐宋文学编年地图/CNKGraph.Writings.xml"
    output_dir = "/Users/rickiyang/Documents/UTS/36118-Applied Natural Language Processing/AT2/living-voices-dataset/datasets/du_fu/raw_data"
    
    # Create extractor
    extractor = DuFuXMLExtractor(xml_file, output_dir)
    
    # Extract poems
    poems = extractor.extract_all_dufu_poems()
    
    if not poems:
        print("Error: No Du Fu poems were extracted!")
        return
    
    # Save results
    print()
    print("Saving extracted data...")
    extractor.save_to_json()
    extractor.save_to_csv()
    extractor.save_statistics()
    
    print()
    print("=" * 80)
    print("Du Fu Data Extraction Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
