# 杜甫生平心理变化的自然语言处理分析

> 通过现代NLP技术量化分析古代诗人的心理变化轨迹

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 项目背景

从两年前走进成都杜甫草堂、站在那幅浮雕壁画前痛哭开始，我便被一个问题萦绕：**天才是否值得一个更好的人生？**

杜甫，被誉为“诗圣”，天纵奇才，却壮志未酬，终其一生颠沛流离。他的诗作保存了中国文学史上极为饱满的痛苦与不甘。

这一份惋惜并不只属于历史。在我的心中，杜甫的经历折射了一个更普遍的问题：**当个人的才华与时局洪流相遇时，能否留下属于自我的答案？**

正因如此，我希望借助自然语言处理（NLP）的工具，追踪杜甫在不同时期的语言、意象和情感演变，重建一条属于他的心理轨迹。

与其说这是一个单纯的 NLP 项目，不如说是代码与杜甫的一次对话。

我关心的不是算法本身，而是：**在动荡的时局和人生的起伏中，人的心境究竟会有怎样的变化？**

通过数据科学的方法，我希望为“**文学的灵魂**”提供一个新的观察角度，也让人们在阅读这些曲折的数字化曲线时，更深切地感受到杜甫诗歌背后那份执着与不甘。

## 项目简介

本项目旨在通过自然语言处理技术，分析唐代著名诗人杜甫在不同生活阶段的心理状态变化。通过对杜甫诗歌作品的情感分析、主题建模和时间序列分析，揭示其人生经历对心理状态的影响。

## 研究目标

- 构建杜甫诗歌语料库，按时间顺序整理其作品
- 运用情感分析技术识别诗歌中的情感倾向
- 通过主题建模发现不同时期的创作主题变化
- 分析历史事件对杜甫心理状态的影响
- 可视化展示心理变化的时间轨迹

## 技术栈

- **数据处理**: pandas, numpy, jieba
- **机器学习**: scikit-learn, transformers
- **深度学习**: torch, tensorflow
- **可视化**: matplotlib, seaborn, plotly
- **中文NLP**: BERT-Chinese, LAC
- **统计分析**: scipy, statsmodels

## 快速开始

### 环境配置
```bash
# 克隆项目
git clone https://github.com/your-username/dufu-psychology-analysis.git
cd dufu-psychology-analysis

# 创建虚拟环境
conda create -n dufu-env python=3.11 -y
conda activate dufu-env

# 安装依赖
pip install -r requirements.txt
```

### 立即运行
```bash
# 启动Jupyter分析环境
jupyter notebook notebooks/基于自然语言处理的杜甫诗歌心理演化研究.ipynb

# 或运行命令行分析
python -m src.main --poet 杜甫 --period all
```

## 项目结构

```
├── data/                   # 数据目录
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后数据
│   └── external/          # 外部数据源
├── src/                    # 源代码
│   ├── data/              # 数据处理模块
│   ├── models/            # 机器学习模型
│   ├── analysis/          # 分析工具
│   ├── visualization/     # 可视化工具
│   └── utils/             # 工具函数
├── notebooks/              # Jupyter notebooks
├── models/                 # 训练好的模型
├── results/                # 分析结果
├── docs/                   # 文档
├── tests/                  # 测试代码
├── requirements.txt        # 依赖包
└── README.md              # 项目说明
```

## 数据说明

本项目使用的数据包括：
- 杜甫诗歌全集（按创作时间排序）
- 相关历史背景资料
- 已标注的情感倾向数据

## 贡献指南

欢迎提交Pull Request或Issue。请确保：
1. 代码符合PEP8规范
2. 添加必要的测试
3. 更新相关文档

## 许可证

MIT License

## 作者

[您的姓名] - [您的邮箱]

## 致谢

感谢所有为中国古典文学数字化做出贡献的学者和机构。
