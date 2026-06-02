# SkillNet

AI Skills 的创建、发现与编排平台 — 构建可组合的 Agent 能力系统。

## 目录结构

```
SkillNet/
├── SkillNet/                  # 主项目
│   ├── skillnet-web-new/      # Streamlit 前端应用
│   ├── README.md              # 项目说明
│   ├── requirements-dev.txt   # Python 依赖
│   └── sync_stats.py          # 统计同步脚本
├── Skills/                    # Skills 子项目
├── papers/                    # 研究论文
├── research/                  # 调研文档
│   └── alfworld/              # ALFWorld 数据集调研
└── docs/                      # 任务笔记
```

## 前端 (skillnet-web-new)

基于 Streamlit 的 Web 应用，提供技能浏览搜索、关系图谱可视化、Agent 工作流 Demo 等功能。

### 快速启动

```bash
cd SkillNet/skillnet-web-new
pip install -r ../requirements-dev.txt
streamlit run app_new.py
```

### 配置

在 `SkillNet/skillnet-web-new/.streamlit/secrets.toml` 中配置 Supabase：

```toml
[supabase]
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "eyJ..."
```

详细说明见 `SkillNet/skillnet-web-new/README.md`。
