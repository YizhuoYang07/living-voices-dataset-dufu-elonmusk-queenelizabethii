# 数据目录说明

## 目录结构

### raw/
存放原始数据文件
- `poems_raw.csv` - 杜甫诗歌原始数据
- `historical_events.csv` - 相关历史事件数据
- `biographical_timeline.csv` - 杜甫生平时间线数据

### processed/
存放预处理后的数据
- `poems_cleaned.csv` - 清洗后的诗歌数据
- `poems_segmented.csv` - 分词后的诗歌数据
- `emotion_labeled.csv` - 已标注情感的数据
- `timeline_features.csv` - 时间线特征数据

### external/
存放外部数据源
- `sentiment_dict.txt` - 情感词典
- `stopwords.txt` - 停用词表
- `historical_context.json` - 历史背景数据

## 数据获取

1. 从古籍数据库获取杜甫诗歌全集
2. 整理历史文献中的相关事件
3. 构建情感分析所需的词典资源

## 数据格式

### 诗歌数据格式
```csv
poem_id,title,content,year,period,location,background
1,春望,国破山河在...,757,安史之乱期,长安,战乱背景
```

### 情感标注格式
```csv
poem_id,sentence,emotion_label,intensity
1,国破山河在,悲伤,0.8
```
