#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整提取CNKGraph.Writings.xml中的杜甫数据到三个CSV文件
基于最新的原生特征设计
"""

import xml.etree.ElementTree as ET
import json
import csv
from datetime import datetime
from collections import defaultdict
import os

def extract_dufu_data_to_csv():
    """提取杜甫数据到四个CSV文件"""
    print("🚀 开始提取CNKGraph.Writings.xml中的杜甫数据...")
    
    xml_file = "CNKGraph.Writings.xml"
    
    # 初始化数据收集器
    database_metadata = {}  # 数据库元数据
    dufu_metadata = {}      # 杜甫元数据
    dufu_poems = []
    timeline_data = defaultdict(lambda: {
        'poems_count': 0,
        'poem_ids': [],
        'group_numbers': [],
        'place_codes': [],
        'poem_types': defaultdict(int),
        'rhyme_categories': defaultdict(int),
        'has_source_books': 0,
        'total_allusions': 0,
        'total_annotations': 0,
        'annotation_types': defaultdict(int),
        'total_lines': 0,
        'has_title_count': 0,
        'group_poems_count': 0,
        'unique_places': set()
    })
    
    # 杜甫专属统计
    dufu_stats = {
        'creation_dates': defaultdict(int),
        'places': defaultdict(int),
        'poem_types': defaultdict(int),
        'rhyme_categories': defaultdict(int),
        'poem_type_details': defaultdict(int),
        'dynasties': defaultdict(int),
        'years_range': set(),
        'places_count': set(),
        'group_numbers': set(),
        'author_ids': set(),
        'has_final_rhyme': 0,
        'has_title_poems': 0,
        'poems_with_allusions': 0,
        'poems_with_annotations': 0,
        'total_lines_count': 0,
        'poems_with_source_books': 0,
        'annotation_types_distribution': defaultdict(int)
    }
    
    # 统计信息
    stats = {
        'total_poems': 0,
        'dufu_poems': 0,
        'dufu_mentions': 0,
        'dynasties': set(),
        'poem_types': defaultdict(int),
        'annotation_types': defaultdict(int),
        'earliest_date': None,
        'latest_date': None
    }
    
    try:
        print("📄 解析XML文件...")
        
        # 解析XML根元素信息 - 数据库元数据
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # 提取根元素database_metadata
        database_metadata.update({
            'dataset_name': 'CNKGraph.Writings',
            'xml_version': '1.0',  # 从XML声明获取
            'xml_encoding': 'utf-8',
            'namespace_xsi': root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', ''),
            'namespace_xsd': 'http://www.w3.org/2001/XMLSchema',
            'max_id': root.get('MaxId', ''),
            'extraction_timestamp': datetime.now().isoformat()
        })
        
        print(f"📊 XML MaxId: {database_metadata['max_id']}")
        
        # 使用迭代解析处理大文件
        print("🔍 开始迭代解析诗歌数据...")
        context = ET.iterparse(xml_file, events=("start", "end"))
        context = iter(context)
        event, root = next(context)
        
        for event, elem in context:
            if event == "end" and elem.tag == "Poem":
                stats['total_poems'] += 1
                
                # 获取诗歌基本属性
                poem_id = elem.get('Id', '')
                dynasty = elem.get('D', '')
                author = elem.get('AU', '')
                author_id = elem.get('AId', '')
                
                stats['dynasties'].add(dynasty)
                
                # 检查是否是杜甫的作品
                if author == '杜甫':
                    stats['dufu_poems'] += 1
                    
                    # 提取完整诗歌信息
                    poem_data = extract_poem_data(elem)
                    dufu_poems.append(poem_data)
                    
                    # 更新杜甫专属统计
                    update_dufu_stats(poem_data, dufu_stats)
                    
                    # 更新时间序列数据
                    update_timeline_data(poem_data, timeline_data)
                    
                    # 更新统计信息
                    poem_type = poem_data.get('poem_type', '')
                    if poem_type:
                        stats['poem_types'][poem_type] += 1
                    
                    # 更新日期范围
                    creation_date = poem_data.get('creation_date_raw', '')
                    if creation_date:
                        if not stats['earliest_date'] or creation_date < stats['earliest_date']:
                            stats['earliest_date'] = creation_date
                        if not stats['latest_date'] or creation_date > stats['latest_date']:
                            stats['latest_date'] = creation_date
                
                # 检查杜甫被提及
                xml_str = ET.tostring(elem, encoding='unicode')
                if '杜甫' in xml_str and author != '杜甫':
                    stats['dufu_mentions'] += 1
                
                # 清理内存
                elem.clear()
                root.clear()
                
                # 进度显示
                if stats['total_poems'] % 100000 == 0:
                    print(f"   已处理 {stats['total_poems']:,} 首诗歌，发现杜甫作品 {stats['dufu_poems']} 首")
        
        # 完善database_metadata
        database_metadata.update({
            'total_poems_count': stats['total_poems'],
            'dufu_poems_count': stats['dufu_poems'],
            'dufu_mentions_count': stats['dufu_mentions'],
            'dynasties_list': list(stats['dynasties']),
            'extraction_completed': True
        })
        
        # 生成杜甫元数据
        dufu_metadata = generate_dufu_metadata(dufu_stats, dufu_poems)
        
        print(f"\n✅ 数据提取完成！")
        print(f"   📚 总诗歌数: {stats['total_poems']:,}")
        print(f"   ✍️ 杜甫作品: {stats['dufu_poems']:,}")
        print(f"   📝 杜甫被提及: {stats['dufu_mentions']:,}")
        
        # 生成CSV文件
        generate_csv_files(database_metadata, dufu_metadata, dufu_poems, timeline_data)
        
        return database_metadata, dufu_metadata, dufu_poems, timeline_data
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

def extract_poem_data(poem_elem):
    """从XML元素提取完整的诗歌数据"""
    poem_data = {}
    
    # 基本属性
    poem_data['poem_id'] = poem_elem.get('Id', '')
    poem_data['group_number'] = poem_elem.get('G', '')
    poem_data['dynasty'] = poem_elem.get('D', '')
    poem_data['author'] = poem_elem.get('AU', '')
    poem_data['author_id'] = poem_elem.get('AId', '')
    poem_data['creation_date_raw'] = poem_elem.get('AD', '')
    poem_data['place_code'] = poem_elem.get('AP', '')
    poem_data['poem_type'] = poem_elem.get('T', '')
    poem_data['poem_type_detail'] = poem_elem.get('TD', '')
    poem_data['rhyme_category'] = poem_elem.get('R', '')
    poem_data['rhyme_number'] = poem_elem.get('RA', '')
    poem_data['final_rhyme'] = poem_elem.get('FR', '')
    poem_data['has_title'] = poem_elem.get('TS', '') == 'true'
    
    # 标题信息
    title_elem = poem_elem.find('Title')
    if title_elem is not None:
        poem_data['title_text'] = title_elem.get('C', '')
        title_annotations = extract_annotations(title_elem.find('Ns'))
        poem_data['title_annotations'] = json.dumps(title_annotations, ensure_ascii=False)
    else:
        poem_data['title_text'] = ''
        poem_data['title_annotations'] = json.dumps({}, ensure_ascii=False)
    
    # 来源文献
    fs_elem = poem_elem.find('Fs')
    if fs_elem is not None:
        source_books = [f.text for f in fs_elem.findall('F') if f.text]
        poem_data['source_books'] = json.dumps(source_books, ensure_ascii=False)
    else:
        poem_data['source_books'] = json.dumps([], ensure_ascii=False)
    
    # 典故信息
    as_elem = poem_elem.find('As')
    if as_elem is not None:
        allusions = []
        for a in as_elem.findall('A'):
            allusion = {
                'ai': a.get('AI', ''),
                'si': a.get('SI', ''),
                'text': a.text or ''
            }
            allusions.append(allusion)
        poem_data['allusion_info'] = json.dumps(allusions, ensure_ascii=False)
    else:
        poem_data['allusion_info'] = json.dumps([], ensure_ascii=False)
    
    # 诗句内容
    jus_elem = poem_elem.find('Jus')
    if jus_elem is not None:
        lines = []
        tones = []
        rhymes = []
        line_annotations = []
        
        for ju in jus_elem.findall('Ju'):
            lines.append(ju.get('C', ''))
            tones.append(ju.get('T', ''))
            rhymes.append(ju.get('R', ''))
            
            # 提取该句的注释
            ju_annotations = extract_annotations(ju.find('Ns'))
            line_annotations.append(ju_annotations)
        
        poem_data['poem_content_lines'] = json.dumps(lines, ensure_ascii=False)
        poem_data['poem_lines_tones'] = json.dumps(tones, ensure_ascii=False)
        poem_data['poem_lines_rhymes'] = json.dumps(rhymes, ensure_ascii=False)
        poem_data['line_annotations'] = json.dumps(line_annotations, ensure_ascii=False)
    else:
        poem_data['poem_content_lines'] = json.dumps([], ensure_ascii=False)
        poem_data['poem_lines_tones'] = json.dumps([], ensure_ascii=False)
        poem_data['poem_lines_rhymes'] = json.dumps([], ensure_ascii=False)
        poem_data['line_annotations'] = json.dumps([], ensure_ascii=False)
    
    # 分类注释
    all_annotations = extract_all_annotations(poem_elem)
    poem_data['text_annotations'] = json.dumps(all_annotations['Text'], ensure_ascii=False)
    poem_data['word_dict_annotations'] = json.dumps(all_annotations['WordDictInJson'], ensure_ascii=False)
    poem_data['char_dict_annotations'] = json.dumps(all_annotations['CharDictInJson'], ensure_ascii=False)
    poem_data['allusion_key_annotations'] = json.dumps(all_annotations['AllusionKey'], ensure_ascii=False)
    poem_data['image_annotations'] = json.dumps(all_annotations['Image'], ensure_ascii=False)
    
    # 句子索引
    sis_elem = poem_elem.find('SIs')
    if sis_elem is not None:
        sentence_indices = []
        for si in sis_elem.findall('SI'):
            indices = [int(i.text) for i in si.findall('int') if i.text and i.text.isdigit()]
            sentence_indices.append(indices)
        poem_data['sentence_indices'] = json.dumps(sentence_indices, ensure_ascii=False)
    else:
        poem_data['sentence_indices'] = json.dumps([], ensure_ascii=False)
    
    return poem_data

def extract_annotations(ns_elem):
    """提取Ns元素下的所有注释"""
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

def extract_all_annotations(poem_elem):
    """提取诗歌中所有类型的注释"""
    annotations = {
        'Text': [],
        'WordDictInJson': [],
        'CharDictInJson': [],
        'AllusionKey': [],
        'Image': []
    }
    
    # 递归查找所有N元素
    for n in poem_elem.iter('N'):
        n_type = n.get('T', '')
        if n_type in annotations:
            annotation = {
                'index': n.get('I', ''),
                'content': n.text or ''
            }
            annotations[n_type].append(annotation)
    
    return annotations

def update_dufu_stats(poem_data, dufu_stats):
    """更新杜甫专属统计数据"""
    # 创作时间统计
    creation_date = poem_data.get('creation_date_raw', '')
    if creation_date:
        dufu_stats['creation_dates'][creation_date] += 1
        # 提取年份
        year_match = creation_date[:4] if len(creation_date) >= 4 else creation_date
        dufu_stats['years_range'].add(year_match)
    
    # 地点统计
    place_code = poem_data.get('place_code', '')
    if place_code:
        dufu_stats['places'][place_code] += 1
        dufu_stats['places_count'].add(place_code)
    
    # 诗歌类型统计
    poem_type = poem_data.get('poem_type', '')
    if poem_type:
        dufu_stats['poem_types'][poem_type] += 1
    
    poem_type_detail = poem_data.get('poem_type_detail', '')
    if poem_type_detail:
        dufu_stats['poem_type_details'][poem_type_detail] += 1
    
    # 押韵统计
    rhyme_category = poem_data.get('rhyme_category', '')
    if rhyme_category:
        dufu_stats['rhyme_categories'][rhyme_category] += 1
    
    # 朝代统计
    dynasty = poem_data.get('dynasty', '')
    if dynasty:
        dufu_stats['dynasties'][dynasty] += 1
    
    # 组号统计
    group_number = poem_data.get('group_number', '')
    if group_number:
        dufu_stats['group_numbers'].add(group_number)
    
    # 作者ID统计
    author_id = poem_data.get('author_id', '')
    if author_id:
        dufu_stats['author_ids'].add(author_id)
    
    # 特殊特征统计
    if poem_data.get('final_rhyme'):
        dufu_stats['has_final_rhyme'] += 1
    
    if poem_data.get('has_title'):
        dufu_stats['has_title_poems'] += 1
    
    # 典故统计
    allusion_info = poem_data.get('allusion_info', '[]')
    if allusion_info and allusion_info != '[]':
        dufu_stats['poems_with_allusions'] += 1
    
    # 来源文献统计
    source_books = poem_data.get('source_books', '[]')
    if source_books and source_books != '[]':
        dufu_stats['poems_with_source_books'] += 1
    
    # 诗句行数统计
    poem_lines = poem_data.get('poem_content_lines', '[]')
    if poem_lines and poem_lines != '[]':
        lines = json.loads(poem_lines)
        dufu_stats['total_lines_count'] += len(lines)
    
    # 注释类型统计
    for annotation_type in ['text_annotations', 'word_dict_annotations', 'char_dict_annotations', 
                           'allusion_key_annotations', 'image_annotations']:
        annotations = poem_data.get(annotation_type, '[]')
        if annotations and annotations != '[]':
            annotation_list = json.loads(annotations)
            if annotation_list:
                dufu_stats['poems_with_annotations'] += 1
                dufu_stats['annotation_types_distribution'][annotation_type] += len(annotation_list)

def generate_dufu_metadata(dufu_stats, dufu_poems):
    """生成杜甫元数据"""
    dufu_metadata = {
        # 基本信息
        'author_name': '杜甫',
        'total_poems_count': len(dufu_poems),
        'author_id': list(dufu_stats['author_ids'])[0] if dufu_stats['author_ids'] else '',
        'extraction_timestamp': datetime.now().isoformat(),
        
        # 时间跨度
        'earliest_year': min(dufu_stats['years_range']) if dufu_stats['years_range'] else '',
        'latest_year': max(dufu_stats['years_range']) if dufu_stats['years_range'] else '',
        'total_years_span': len(dufu_stats['years_range']),
        'creation_dates_count': len(dufu_stats['creation_dates']),
        'most_productive_date': max(dufu_stats['creation_dates'].items(), key=lambda x: x[1])[0] if dufu_stats['creation_dates'] else '',
        'most_productive_date_count': max(dufu_stats['creation_dates'].values()) if dufu_stats['creation_dates'] else 0,
        
        # 地理分布
        'total_places_count': len(dufu_stats['places_count']),
        'most_frequent_place': max(dufu_stats['places'].items(), key=lambda x: x[1])[0] if dufu_stats['places'] else '',
        'most_frequent_place_count': max(dufu_stats['places'].values()) if dufu_stats['places'] else 0,
        'places_distribution': json.dumps(dict(dufu_stats['places']), ensure_ascii=False),
        
        # 诗歌体裁
        'poem_types_count': len(dufu_stats['poem_types']),
        'most_common_poem_type': max(dufu_stats['poem_types'].items(), key=lambda x: x[1])[0] if dufu_stats['poem_types'] else '',
        'most_common_poem_type_count': max(dufu_stats['poem_types'].values()) if dufu_stats['poem_types'] else 0,
        'poem_types_distribution': json.dumps(dict(dufu_stats['poem_types']), ensure_ascii=False),
        'poem_type_details_distribution': json.dumps(dict(dufu_stats['poem_type_details']), ensure_ascii=False),
        
        # 押韵特征
        'rhyme_categories_count': len(dufu_stats['rhyme_categories']),
        'most_used_rhyme': max(dufu_stats['rhyme_categories'].items(), key=lambda x: x[1])[0] if dufu_stats['rhyme_categories'] else '',
        'most_used_rhyme_count': max(dufu_stats['rhyme_categories'].values()) if dufu_stats['rhyme_categories'] else 0,
        'rhyme_categories_distribution': json.dumps(dict(dufu_stats['rhyme_categories']), ensure_ascii=False),
        
        # 特殊特征
        'has_final_rhyme_count': dufu_stats['has_final_rhyme'],
        'has_title_poems_count': dufu_stats['has_title_poems'],
        'poems_with_allusions_count': dufu_stats['poems_with_allusions'],
        'poems_with_annotations_count': dufu_stats['poems_with_annotations'],
        'poems_with_source_books_count': dufu_stats['poems_with_source_books'],
        'total_lines_count': dufu_stats['total_lines_count'],
        'average_lines_per_poem': dufu_stats['total_lines_count'] / len(dufu_poems) if dufu_poems else 0,
        
        # 组织特征
        'group_numbers_count': len(dufu_stats['group_numbers']),
        'dynasties_distribution': json.dumps(dict(dufu_stats['dynasties']), ensure_ascii=False),
        'annotation_types_distribution': json.dumps(dict(dufu_stats['annotation_types_distribution']), ensure_ascii=False),
        
        # 计算百分比
        'titled_poems_percentage': (dufu_stats['has_title_poems'] / len(dufu_poems) * 100) if dufu_poems else 0,
        'poems_with_allusions_percentage': (dufu_stats['poems_with_allusions'] / len(dufu_poems) * 100) if dufu_poems else 0,
        'poems_with_source_books_percentage': (dufu_stats['poems_with_source_books'] / len(dufu_poems) * 100) if dufu_poems else 0,
        'poems_with_annotations_percentage': (dufu_stats['poems_with_annotations'] / len(dufu_poems) * 100) if dufu_poems else 0
    }
    
    return dufu_metadata

def update_timeline_data(poem_data, timeline_data):
    """更新时间序列数据"""
    time_period = poem_data.get('creation_date_raw', '未知')
    if not time_period:
        time_period = '未知'
    
    tl = timeline_data[time_period]
    tl['poems_count'] += 1
    tl['poem_ids'].append(poem_data['poem_id'])
    
    if poem_data.get('group_number'):
        tl['group_numbers'].append(poem_data['group_number'])
        tl['group_poems_count'] += 1
    
    if poem_data.get('place_code'):
        tl['place_codes'].append(poem_data['place_code'])
        tl['unique_places'].add(poem_data['place_code'])
    
    if poem_data.get('poem_type'):
        tl['poem_types'][poem_data['poem_type']] += 1
    
    if poem_data.get('rhyme_category'):
        tl['rhyme_categories'][poem_data['rhyme_category']] += 1
    
    if poem_data.get('source_books') and poem_data['source_books'] != '[]':
        tl['has_source_books'] += 1
    
    if poem_data.get('allusion_info') and poem_data['allusion_info'] != '[]':
        allusions = json.loads(poem_data['allusion_info'])
        tl['total_allusions'] += len(allusions)
    
    if poem_data.get('poem_content_lines'):
        lines = json.loads(poem_data['poem_content_lines'])
        tl['total_lines'] += len(lines)
    
    if poem_data.get('has_title'):
        tl['has_title_count'] += 1

def generate_csv_files(database_metadata, dufu_metadata, dufu_poems, timeline_data):
    """生成四个CSV文件"""
    print("\n💾 生成CSV文件...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. 生成database_metadata.csv - 数据库元数据
    db_metadata_file = f"database_metadata_{timestamp}.csv"
    with open(db_metadata_file, 'w', newline='', encoding='utf-8') as f:
        if database_metadata:
            writer = csv.DictWriter(f, fieldnames=database_metadata.keys())
            writer.writeheader()
            writer.writerow(database_metadata)
    print(f"✅ {db_metadata_file} - 数据库元数据文件")
    
    # 2. 生成dufu_metadata.csv - 杜甫元数据
    dufu_metadata_file = f"dufu_metadata_{timestamp}.csv"
    with open(dufu_metadata_file, 'w', newline='', encoding='utf-8') as f:
        if dufu_metadata:
            writer = csv.DictWriter(f, fieldnames=dufu_metadata.keys())
            writer.writeheader()
            writer.writerow(dufu_metadata)
    print(f"✅ {dufu_metadata_file} - 杜甫元数据文件")
    
    # 3. 生成dufu_poems.csv - 杜甫诗歌文件
    poems_file = f"dufu_poems_{timestamp}.csv"
    if dufu_poems:
        with open(poems_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dufu_poems[0].keys())
            writer.writeheader()
            writer.writerows(dufu_poems)
    print(f"✅ {poems_file} - 杜甫诗歌文件 ({len(dufu_poems)} 首)")
    
    # 4. 生成dufu_timeline.csv - 时间序列文件
    timeline_list = []
    for time_period, data in timeline_data.items():
        timeline_row = {
            'time_period': time_period,
            'poems_count': data['poems_count'],
            'poem_ids': json.dumps(data['poem_ids'], ensure_ascii=False),
            'group_numbers': json.dumps(list(set(data['group_numbers'])), ensure_ascii=False),
            'place_codes': json.dumps(list(set(data['place_codes'])), ensure_ascii=False),
            'poem_types': json.dumps(dict(data['poem_types']), ensure_ascii=False),
            'rhyme_categories': json.dumps(dict(data['rhyme_categories']), ensure_ascii=False),
            'has_source_books': data['has_source_books'],
            'total_allusions': data['total_allusions'],
            'total_annotations': data['total_annotations'],
            'annotation_types': json.dumps(dict(data['annotation_types']), ensure_ascii=False),
            'total_lines': data['total_lines'],
            'has_title_count': data['has_title_count'],
            'group_poems_count': data['group_poems_count'],
            'unique_places_count': len(data['unique_places'])
        }
        timeline_list.append(timeline_row)
    
    timeline_file = f"dufu_timeline_{timestamp}.csv"
    if timeline_list:
        with open(timeline_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=timeline_list[0].keys())
            writer.writeheader()
            writer.writerows(timeline_list)
    print(f"✅ {timeline_file} - 时间序列文件 ({len(timeline_list)} 个时期)")
    
    print(f"\n🎉 所有CSV文件生成完成！")
    print(f"📁 文件位置: 当前目录")
    
    return db_metadata_file, dufu_metadata_file, poems_file, timeline_file

if __name__ == "__main__":
    print("📜 杜甫数据提取器 - CNKGraph.Writings.xml")
    print("="*60)
    
    # 检查XML文件是否存在
    if not os.path.exists("CNKGraph.Writings.xml"):
        print("❌ 未找到 CNKGraph.Writings.xml 文件")
        print("请确保XML文件在当前目录中")
        exit(1)
    
    # 执行提取
    db_metadata, dufu_metadata, poems, timeline = extract_dufu_data_to_csv()
    
    if db_metadata and dufu_metadata and poems and timeline:
        print("="*60)
        print("🎉 数据提取成功完成！")
        print("📊 生成的文件:")
        print("   1. database_metadata_*.csv - 数据库元数据")
        print("   2. dufu_metadata_*.csv - 杜甫作品元数据") 
        print("   3. dufu_poems_*.csv - 杜甫诗歌详细数据")
        print("   4. dufu_timeline_*.csv - 杜甫时间序列数据")
    else:
        print("❌ 数据提取失败")
