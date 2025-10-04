# 唐宋文学编年地图数据集

## 项目简介

本文件夹包含从CNKGraph（中国知识图谱）项目中提取的唐宋文学作品数据，重点关注杜甫诗歌的全面分析。数据源自大规模XML数据库，包含超过160万首古代诗歌作品。

## 数据源信息

### 原始数据集
- **数据集名称**: CNKGraph.Writings
- **文件名**: CNKGraph.Writings.xml
- **文件大小**: 1.7GB
- **总记录数**: 1,614,233首诗歌
- **编码格式**: UTF-8
- **数据格式**: XML结构化数据

### 杜甫作品统计
- **杜甫作品总数**: 1,496首
- **杜甫被提及次数**: 5,873次
- **创作时间跨度**: 736年 - 乾元二年（约32年）
- **创作地点**: 86个不同地理位置
- **诗歌体裁**: 9种类型
- **押韵类别**: 77种不同韵部

## 文件结构

### 核心数据文件

#### 1. CNKGraph.Writings.xml
原始XML数据文件，包含完整的古代诗歌数据库。

#### 2. CSV数据文件（按时间戳命名）

**database_metadata_YYYYMMDD_HHMMSS.csv**
- 数据库元数据信息
- 包含数据集基本统计和提取信息
- 字段数量: 12个

**dufu_metadata_YYYYMMDD_HHMMSS.csv**
- 杜甫作品专属元数据
- 综合统计分析结果
- 字段数量: 37个
- 包含时间、地理、体裁、音韵等维度的统计

**dufu_poems_YYYYMMDD_HHMMSS.csv**
- 杜甫诗歌详细数据
- 每首诗的完整信息记录
- 记录数量: 1,496行
- 字段数量: 27个

**dufu_timeline_YYYYMMDD_HHMMSS.csv**
- 时间序列数据
- 按创作时期聚合的统计信息
- 时期数量: 69个不同时期
- 字段数量: 15个

### 分析脚本

#### extract_dufu_to_csv.py
主要数据提取脚本，功能包括：
- XML数据解析和处理
- 杜甫作品筛选和提取
- 多维度统计分析
- CSV文件生成

#### analyze_dufu_xml.py
XML数据分析脚本，用于初步探索和验证。

### 配置文件

#### dufu_xml_analysis.json
预分析结果文件，包含数据结构和统计概览。

#### data_and_api_explanation.md
数据源和API使用说明文档。

### API集合

#### postman/ 目录
包含12个Postman API集合文件，涵盖：
- 诗歌数据查询
- 人物信息检索  
- 地理位置数据
- 历史年代信息
- 其他相关数据接口

## 数据结构说明

### XML数据结构
原始XML采用层次化结构：
```
<Poems>
  <Poem Id="..." D="朝代" AU="作者" AId="作者ID" AD="创作日期" AP="地点编码" T="诗歌类型" ...>
    <Title C="标题内容">
      <Ns>注释信息</Ns>
    </Title>
    <Jus>
      <Ju C="诗句内容" T="音调" R="押韵">
        <Ns>句级注释</Ns>
      </Ju>
    </Jus>
    <As>典故信息</As>
    <Fs>文献来源</Fs>
    <SIs>句子索引</SIs>
  </Poem>
</Poems>
```

### CSV数据字段

#### 杜甫诗歌数据主要字段
- **基础信息**: poem_id, dynasty, author, author_id
- **时空信息**: creation_date_raw, place_code
- **体裁信息**: poem_type, poem_type_detail, rhyme_category
- **内容信息**: title_text, poem_content_lines
- **注释信息**: text_annotations, word_dict_annotations, char_dict_annotations
- **典故信息**: allusion_info, allusion_key_annotations
- **文献信息**: source_books
- **结构信息**: sentence_indices, line_annotations

#### 元数据关键指标
- **时间维度**: earliest_year, latest_year, most_productive_date
- **地理维度**: total_places_count, most_frequent_place, places_distribution
- **体裁维度**: poem_types_count, most_common_poem_type, poem_types_distribution
- **音韵维度**: rhyme_categories_count, most_used_rhyme, rhyme_categories_distribution
- **内容维度**: average_lines_per_poem, titled_poems_percentage, poems_with_allusions_percentage

## 使用方法

### 环境要求
- Python 3.7+
- 标准库: xml.etree.ElementTree, csv, json, collections

### 数据提取
```bash
python3 extract_dufu_to_csv.py
```

### 数据分析
```bash
python3 analyze_dufu_xml.py
```

## 数据质量

### 完整性
- 覆盖杜甫全部现存作品
- 保留原始XML所有特征
- 无数据丢失或修改

### 准确性
- 直接从权威数据库提取
- 保持原始编码和格式
- 多重验证确保一致性

### 一致性
- 统一的字段命名规范
- 标准化的数据格式
- 完整的关系映射

## 研究应用

### 文学研究
- 杜甫创作生涯分析
- 诗歌体裁演变研究
- 创作地理分布分析

### 数字人文
- 古典诗歌数据挖掘
- 文本计算分析
- 知识图谱构建

### 统计分析
- 时间序列分析
- 地理空间分析
- 文本特征统计

## 技术特性

### 性能优化
- 迭代式XML解析，内存友好
- 流式处理大文件
- 优化的数据结构设计

### 数据处理
- 支持多种字符编码
- JSON格式存储复杂结构
- 完整保留原始信息

### 扩展性
- 模块化设计
- 易于扩展到其他作者
- 支持自定义分析维度

## 更新日志

### 2025-08-30
- 完成CNKGraph.Writings.xml数据提取
- 生成四个标准化CSV文件
- 实现37维度杜甫元数据分析
- 创建69时期时间序列数据
- 完成数据质量验证

## 许可和引用

### 数据来源
请在使用时适当引用CNKGraph项目和相关数据提供方。

### 使用许可
本处理脚本和分析结果仅供学术研究使用。

## 联系信息

如有数据相关问题或改进建议，请通过项目仓库提交Issues。

---

最后更新时间: 2025年8月30日
