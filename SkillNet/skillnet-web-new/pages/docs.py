# # pages/docs.py
# import streamlit as st
# from utils import render_navbar

# # 1. 页面配置 (必须是第一个 Streamlit 命令)
# st.set_page_config(
#     page_title="Docs - SkillNet",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )
# st.markdown(
#     """
#     <style>
#         [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
#             display: none;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 2. 渲染导航栏 (引入公共组件)
# render_navbar()

# # 3. Docs 页面内容
# st.title("📚 SkillNet Docs")

# # 创建两列布局：左侧目录，右侧内容
# col1, col2 = st.columns([1, 3])

# with col1:
#     st.subheader("Contents")
#     st.markdown("""
#     - [Getting Started](#getting-started)
#     - [Installation](#installation)
#     - [API Reference](#api-reference)
#     - [Contributing](#contributing)
#     """)

# with col2:
#     st.markdown("## Getting Started")
#     st.info("Welcome to the SkillNet documentation. Here you will find guides and API references.")
    
#     st.markdown("""
#     SkillNet is a platform designed to empower Agent Intelligence...
    
#     ### Installation
#     You can install the client via pip:
#     ```bash
#     pip install skillnet-ai
#     ```
    
#     ### API Reference
#     Here is how you initialize the client:
#     ```python
#     from skillnet-ai import Client
#     client = Client(api_key="sk_...")
#     ```
#     """)
    
#     # 甚至可以嵌入 Markdown 文件
#     # with open("README.md", "r", encoding='utf-8') as f:
#     #     st.markdown(f.read())




# # pages/docs.py
# import streamlit as st
# from utils import render_navbar

# # 1. 页面配置
# st.set_page_config(
#     page_title="Docs - SkillNet",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # 隐藏默认侧边栏，使用自定义导航
# st.markdown(
#     """
#     <style>
#         [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
#             display: none;
#         }
#         /* 调整锚点偏移，防止标题被导航栏遮挡 */
#         h1, h2, h3 {
#             scroll-margin-top: 2rem;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 2. 渲染导航栏
# render_navbar()

# st.title("📚 SkillNet Docs")

# # 3. Docs 页面布局
# # 创建两列布局：左侧为固定的目录导航，右侧为文档内容
# # 调整比例为 [1, 4] 让内容区域更宽
# col1, col2 = st.columns([1, 4])

# # --- 左侧目录 (Table of Contents) ---
# with col1:
#     st.subheader("📖 Table of Contents")
#     st.markdown("""
#     - [Overview](#overview)
#     - [Features](#features)
#     - [API Access](#api-access)
#     - [Python Toolkit](#python-toolkit-skillnet-ai)
#         - [Installation](#installation)
#         - [Python SDK Usage](#usage-python-sdk)
#         - [CLI Usage](#cli-usage)
#     - [Skill Structure](#skill-structure)
#     - [Roadmap & Contributing](#roadmap)
#     """)
    
#     st.info("💡 Tip: Use the code snippets directly in your terminal or IDE.")

# # --- 右侧主要内容 ---
# with col2:
#     # 标题区域
#     st.markdown("""
#     <div align="center">

#     # SkillNet: Create, Evaluate, and Connect AI Skills

#     [![PyPI version](https://badge.fury.io/py/skillnet-ai.svg)](https://badge.fury.io/py/skillnet-ai)
#     [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
#     [![arXiv](https://img.shields.io/badge/arXiv-b5212f.svg?logo=arxiv)](https://arxiv.org/)
#     [![Website](https://img.shields.io/badge/Website-SkillNet.openkg.cn-0078D4.svg)](http://skillnet.openkg.cn/)

#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("---")

#     # Overview
#     st.markdown("## 📖 Overview")
#     st.write("SkillNet is an open infrastructure for creating, evaluating, and organizing AI skills at scale.")

#     # Features
#     st.markdown("## 🚀 Features")
#     st.markdown("""
#     - **🔍 Search**: Find skills using keywords match or semantic search.
#     - **📦 One-Line Installation**: Download skill packages directly from GitHub repositories.
#     - **✨ Skill Creation**: Automatically convert various sources into structured, reusable `skills` using LLMs:
#         - Execution trajectories / conversation logs
#         - GitHub repositories
#         - Office documents (PDF, PPT, Word)
#         - Direct text prompts
#     - **📊 Evaluation**: Evaluate and score skills for quality assurance (Safety, Completeness, Excutability, Maintainability, Cost-Awareness).
#     - **🕸️ Relationship Analysis**: Automatically map the connections between skills in your local library, identifying structural relationships between skills (similar_to, belong_to, compose_with, depend_on).
#     """)

#     st.markdown("---")

#     # API Access
#     st.markdown("# 🌐 API Access")
#     st.write("SkillNet provides a public API to search skills. Support both keywords match and semantic search.")
#     st.code("Base Endpoint: http://api-skillnet.openkg.cn/v1/search", language="text")

#     st.markdown("### ⚡ Quick Examples")
    
#     # st.markdown("**1. Keywords Match**")
#     # st.write('Find "development" tools sorted by stars.')
#     # st.code('curl -X GET http://api-skillnet.openkg.cn/v1/search?q=development&sort_by=stars&limit=5 \\\n      -H "accept: application/json"', language="bash")

#     # st.markdown("**2. Vector Semantic Search**")
#     # st.write('Find skills related to "reading charts" using AI similarity.')
#     # st.code('curl -X GET http://api-skillnet.openkg.cn/v1/search?q=reading%20charts&mode=vector&threshold=0.8 \\\n      -H "accept: application/json"', language="bash")
#     # Example 1
#     st.markdown("**1. Keywords Match**")
#     st.write('Find "development" tools sorted by stars.')
    
#     # 使用 Tabs 切换语言，体验更好
#     tab1_1, tab1_2 = st.tabs(["Bash (curl)", "Python"])
    
#     with tab1_1:
#         st.code('curl -X GET "http://api-skillnet.openkg.cn/v1/search?q=pdf&sort_by=stars&limit=5" \\\n      -H "accept: application/json"', language="bash")
    
#     with tab1_2:
#         st.code("""import requests

# url = "http://api-skillnet.openkg.cn/v1/search"
# params = {
#     "q": "development", 
#     "sort_by": "stars", 
#     "limit": 5
# }

# response = requests.get(url, params=params)
# print(response.json())""", language="python")

#     # Example 2
#     st.markdown("**2. Vector Semantic Search**")
#     st.write('Find skills related to "reading charts" using AI similarity.')
    
#     tab2_1, tab2_2 = st.tabs(["Bash (curl)", "Python"])
    
#     with tab2_1:
#         st.code('curl -X GET "http://api-skillnet.openkg.cn/v1/search?q=reading%20charts&mode=vector&threshold=0.8" \\\n      -H "accept: application/json"', language="bash")
        
#     with tab2_2:
#         st.code("""import requests

# url = "http://api-skillnet.openkg.cn/v1/search"
# params = {
#     "q": "reading charts", 
#     "mode": "vector", 
#     "threshold": 0.8
# }

# response = requests.get(url, params=params)
# print(response.json())""", language="python")

#     st.markdown("### 📡 Parameter Reference")
#     st.markdown("""
#     | Parameter | Type | Required | Default | Description |
#     | :--- | :--- | :---: | :--- | :--- |
#     | `q` | string | ✅ | - | The search query (Keywords or Natural Language). |
#     | `mode` | string | - | `keyword` | `keyword` (Fuzzy match) or `vector` (Semantic AI). |
#     | `category` | string | - | `None` | Filter: Development, AIGC, Research, Science, etc. |
#     | `limit` | int | - | `10` | Results per request (Max: 50). |
#     """)
#     st.markdown("""
#     **Mode Specific Parameters:**
#     * **Keyword Mode:** `page` (int), `min_stars` (int), `sort_by` (string: `stars` or `recent`)
#     * **Vector Mode:** `threshold` (float: `0.0` to `1.0`)
#     """)

#     st.markdown("### 📦 Response Structure")
#     with st.expander("Click to view JSON Response Example"):
#         st.code("""{
#   "data": [
#     {
#       "skill_name": "pdf-extractor-v1",
#       "skill_description": "Extracts text and tables from PDF documents.",
#       "author": "openkg-team",
#       "stars": 128,
#       "skill_url": "http://...",
#       "category": "Productivity"
#     }
#   ],
#   "meta": {
#     "query": "pdf",
#     "mode": "keyword",
#     "total": 1,
#     "limit": 10,
#     ...
#   },
#   "success": true
# }""", language="json")

#     st.markdown("---")

#     # Python Toolkit
#     st.markdown("# 🐍 Python Toolkit (`skillnet-ai`)")
#     st.write("**skillnet-ai** is the official Python Toolkit. It functions seamlessly as both a library and a CLI to **Create**, **Evaluate**, and **Organize** skills.")

#     st.markdown("### 📥 Installation")
#     st.code("pip install skillnet-ai", language="bash")

#     st.markdown("### 🛠 Usage (Python SDK)")
#     st.write("The `SkillNetClient` is your main entry point.")

#     st.markdown("#### 1. Initialization")
#     st.code("""from skillnet_ai import SkillNetClient

# client = SkillNetClient(
#     api_key="sk-...",       # Required for Creation, and Evaluation
#     # base_url="...",       # Optional: Custom LLM base URL
#     # github_token="ghp-..." # Optional: For private repos or higher rate limits
# )""", language="python")

#     st.markdown("#### 2. Search for Skills")
#     st.write("Perform keywords match or semantic searches to find skills. (See [Parameter Reference](#parameter-reference) for configuration details.)")
#     st.code("""# 1. Standard Keywords Match
# results = client.search(q="pdf", mode="keyword", limit=10, min_stars=5, sort_by="stars")

# # 2. Semantic Search
# results = client.search(q="Help me analyze financial PDF reports", mode="vector", threshold=0.85)

# if results:
#     top_skill = results[0]
#     print(f"Found: {top_skill.skill_name} (Stars: {top_skill.stars})")
#     print(f"URL: {top_skill.skill_url}")""", language="python")

#     st.markdown("#### 3. Install Skills")
#     st.write("Download and install a skill directly from a URL (e.g., from above search results) into your local workspace.")
#     st.code("""skill_url = "https://github.com/anthropics/skills/tree/main/skills/skill-creator"

# try:
#     # Downloads to ./my_agent_skills
#     local_path = client.download(url=skill_url, target_dir="./my_agent_skills")
#     print(f"Skill successfully installed at: {local_path}")
# except Exception as e:
#     print(f"Download failed: {e}")""", language="python")

#     st.markdown("#### 4. Create Skills")
#     st.write("Turn local Trajectory or GitHub repository into a polished Skill Package (SKILL.md, scripts, etc.).")
#     st.code("""# 1. Create skill from Local Trajectory
# # Prepare your trajectory (e.g., a conversation log string)
# trajectory_log = \"\"\"
# User: I need to rename all .jpg files in this folder to .png.
# Agent: I will write a python script to iterate through the folder...
# Agent: Script executed. Renamed 5 files.
# \"\"\"

# # Generate Skill, Returns a list of paths to the generated skill folders
# created_paths = client.create(
#     trajectory_content=trajectory_log, 
#     output_dir="./created_skills",
#     model="gpt-4o"
# )

# # 2. Create skill from GitHub Repository
# created_paths = client.create(
#     github_url="https://github.com/zjunlp/DeepKE",
#     output_dir="./created_skills",
#     model="gpt-4o"
# )

# # 3. Create skill from a office documents (PDF, Word, PPT)
# created_paths = client.create(
#     office_file="./docs/user_guide.pdf",
#     output_dir="./created_skills"
# )

# # 4. Create skill from a prompt description
# created_paths = client.create(
#     prompt="Create a skill for web scraping that extracts article titles and content",
#     output_dir="./created_skills"
# )

# print(f"Created {len(created_paths)} new skills.")
# for path in created_paths:
#     print(f"- {path}")""", language="python")

#     st.markdown("#### 5. Skill Evaluation")
#     st.write("Assess the Safety, Completeness, Executability, Maintainability and Cost-Awareness of a skill. Supports both remote GitHub URLs and local directories.")
#     st.code("""# Evaluate from local directory
# # target_skill = "./my_skills/web_search"

# # Evaluate from GitHub URL (uses github_token if provided during initialization)
# target_skill = "https://github.com/anthropics/skills/tree/main/skills/algorithmic-art"

# # Evaluates the skill using the client's API key
# result = client.evaluate(target=target_skill, model="gpt-4o", cache_dir="./evaluate_cache_dir")

# # Display results
# print(f"Evaluation Result: {result}")""", language="python")

#     st.markdown("#### 6. Skill Relationship Analysis")
#     st.write("Analyze a local directory containing multiple skills to infer a relationship graph. It identifies relationships like dependencies (depend_on), collaboration (compose_with), hierarchy (belong_to), and alternatives (similar_to).")
#     st.code("""# Directory containing multiple skill folders
# skills_directory = "./my_agent_skills"

# # Analyze relationships between skills
# # This will also save a 'relationships.json' in the directory by default
# relationships = client.analyze(skills_dir=skills_directory, save_to_file=True, model="gpt-4o")

# # Display the relationships
# for rel in relationships:
#     print(f"{rel['source']} --[{rel['type']}]--> {rel['target']}")
#     # Output: PDF_Parser --[compose_with]--> Text_Summarizer")""", language="python")

#     st.markdown("### 💻 CLI Usage")
#     st.write("The CLI is powered by `Typer` and `Rich` for a beautiful terminal experience.")

#     st.markdown("#### Common Commands")
#     st.markdown("""
#     | Command | Action | Example |
#     | :--- | :--- | :--- |
#     | **`search`** | Search skills | `skillnet search "data viz" --mode vector` |
#     | **`download`** | Install skill | `skillnet download <github_url> -d ./skills` |
#     | **`create`** | Create skill | `skillnet create log.txt --model gpt-4o` |
#     | **`evaluate`** | Evaluate skill quality | `skillnet evaluate ./my_tool` |
#     | **`analyze`** | Analyze skill relations | `skillnet analyze ./my_agent_skills` |
#     """)
#     st.caption("Tip: Use `skillnet [command] --help` to see all available options (e.g., thresholds, sorting).")

#     st.markdown("#### 1. Search Skills (`search`)")
#     st.write("Search the registry using keywords match or semantic search.")
#     st.code("""# Basic keywords match
# skillnet search "pdf"

# # Semantic/Vector search (finds skills by meaning)
# skillnet search "Help me analyze financial PDF reports" --mode vector --threshold 0.85

# # Filter by category and sort results
# skillnet search "visualization" --category "Development" --sort-by stars --limit 10""", language="bash")

#     st.markdown("#### 2. Install Skills (`download`)")
#     st.write("Download and install a skill directly from a GitHub repository subdirectory.")
#     st.code("""# Download to the current directory
# skillnet download https://github.com/anthropics/skills/tree/main/skills/algorithmic-art

# # Download to a specific target directory
# skillnet download https://github.com/anthropics/skills/tree/main/skills/algorithmic-art -d ./my_agent/skills

# # Download from a private repository
# skillnet download <private_url> --token <your_github_token>""", language="bash")

#     st.markdown("#### 3. Create Skills (`create`)")
#     st.write("Create structured Skill from various sources using LLMs.")
#     st.code("""# Requirement: Ensure API_KEY is set in your environment variables.
# export API_KEY=sk-xxxxx
# export BASE_URL= xxxxxx # Optional custom LLM base URL

# # From a trajectory file
# skillnet create ./logs/trajectory.txt -d ./generated_skills

# # From a GitHub repository
# skillnet create --github https://github.com/owner/repo

# # From an office document (PDF, PPT, Word)
# skillnet create --office ./docs/guide.pdf

# # From a direct prompt
# skillnet create --prompt "Create a skill for extracting tables from images"

# # Specify a custom model
# skillnet create --office report.pdf --model gpt-4o""", language="bash")

#     st.markdown("#### 4. Evaluate Skills (`evaluate`)")
#     st.write("Generate a comprehensive quality report (Safety, Completeness, Executability, Maintainability, Cost-Awareness) for a skill.")
#     st.code("""# Requirement: Ensure API_KEY is set in your environment variables.
# export API_KEY=sk-xxxxx
# export BASE_URL= xxxxxx # Optional custom LLM base URL

# # Evaluate a remote skill via GitHub URL
# skillnet evaluate https://github.com/anthropics/skills/tree/main/skills/algorithmic-art

# # Evaluate a local skill directory
# skillnet evaluate ./my_skills/web_search

# # Custom evaluation config
# skillnet evaluate ./my_skills/tool --category "DevOps" --model gpt-4o""", language="bash")

#     st.markdown("#### 5. Analyze Relationships (`analyze`)")
#     st.write("Scan a local directory of skills to analyze their connections using AI.")
#     st.code("""# Requirement: Ensure API_KEY is set in your environment variables.
# export API_KEY=sk-xxxxx
# export BASE_URL= xxxxxx # Optional custom LLM base URL

# # Analyze a directory containing multiple skill folders
# skillnet analyze ./my_agent_skills

# # Analyze without saving the result file (just print to console)
# skillnet analyze ./my_agent_skills --no-save

# # Specify a model for the analysis
# skillnet analyze ./my_agent_skills --model gpt-4o""", language="bash")

#     st.markdown("### Environment Configuration")
#     st.write("To use **Creation**, **Evaluation**, or **Analyze** features, set your environment variables:")
#     st.code("""export API_KEY="your_api_key"
# export BASE_URL="https://xxxxx" # Optional""", language="bash")

#     st.markdown("---")

#     # Skill Structure
#     st.markdown("## 📂 Skill Structure")
#     st.write("Standardized structure for all SkillNet packages:")
#     st.code("""skill-name/
# ├── SKILL.md          # [Required] Metadata (YAML) + Instructions
# ├── scripts/          # [Optional] Executable Python/Bash scripts
# ├── references/       # [Optional] Static docs or API specs
# └── assets/           # [Optional] Icons, templates, examples""", language="text")

#     st.markdown("---")

#     # Roadmap
#     st.markdown("## 🗺 Roadmap")
#     # 修正：直接使用 markdown 列表，而不是 st.checkbox 组件
#     st.markdown("""
#     - ✅ Keyword Match & Semantic Search
#     - ✅ Skill Installer
#     - ✅ Skill Creator (Local File & GitHub Repository)
#     - ✅ Skill Evaluation & Scoring
#     - ✅ Skill Relationship Analysis
#     """)

#     st.markdown("## 🤝 Contributing")
#     st.write("Contributions are welcome! Please submit a Pull Request or open an Issue on GitHub.")

#     st.markdown("## 📄 License")
#     st.write("This project is licensed under the [MIT License](LICENSE).")



# pages/docs.py
import streamlit as st
from utils import render_navbar

# 1. 页面配置
st.set_page_config(
    page_title="Docs - SkillNet",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏默认侧边栏，使用自定义导航
st.markdown(
    """
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none;
        }
        /* 调整锚点偏移，防止标题被导航栏遮挡 */
        h1, h2, h3 {
            scroll-margin-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 渲染导航栏
render_navbar()

st.title("📚 SkillNet Docs")

# 3. Docs 页面布局
# 创建两列布局：左侧为固定的目录导航，右侧为文档内容
# 调整比例为 [1, 4] 让内容区域更宽
col1, col2 = st.columns([1, 4])

# --- 左侧目录 (Table of Contents) ---
with col1:
    st.subheader("📖 Table of Contents")
    st.markdown("""
    - [Overview](#overview)
    - [News](#news)
    - [Key Features](#key-features)
    - [Quick Start](#quick-start)
    - [REST API](#rest-api)
    - [Python SDK](#python-sdk)
    - [CLI Reference](#cli-reference)
    - [Configuration](#configuration)
    - [Example: Scientific Discovery](#example-scientific-discovery)
    - [OpenClaw Integration](#openclaw-integration)
    - [Model Context Protocol (MCP) Integration](#model-context-protocol-mcp-integration)
    - [Contributing](#contributing)
    - [Citation](#citation)
    """)

# --- 右侧主要内容 ---
with col2:
    # 标题区域
    st.markdown("""
    <div align="center">
    
    <p><strong>Open Infrastructure for Creating, Evaluating, and Connecting AI Agent Skills</strong></p>

    <p>
    Search 300,000+ community skills · One-line install · Auto-create from repos / docs / logs<br/>
    5-dimension quality scoring · Semantic relationship graph
    </p>

    [![PyPI version](https://badge.fury.io/py/skillnet-ai.svg)](https://pypi.org/project/skillnet-ai/)
    [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
    [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
    [![arXiv](https://img.shields.io/badge/arXiv-b5212f.svg?logo=arxiv)](https://arxiv.org/abs/2603.04448)
    [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-FFD21E)](https://huggingface.co/blog/xzwnlp/skillnet)
    [![Website](https://img.shields.io/badge/🌐_Website-skillnet.openkg.cn-0078D4.svg)](http://skillnet.openkg.cn/)
    [![GitHub](https://img.shields.io/badge/GitHub-Code-black?logo=github)](https://github.com/zjunlp/SkillNet)    

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Overview
    st.markdown("## 📖 Overview")
    st.markdown("**SkillNet** is an open-source platform that treats AI agent skills as first-class, shareable packages — like npm for AI capabilities. It provides end-to-end tooling to **search**, **install**, **create**, **evaluate**, and **organize** skills, so agents can learn from the community and continuously grow.")

    # News
    st.markdown("## 📢 News")
    st.markdown("""
    - **🤖 [2026-03-26] JiuwenClaw × SkillNet Integrated!** — JiuwenClaw now natively integrates SkillNet as its built-in skill marketplace. One-click search and install from SkillNet. [View Guide →](https://github.com/zjunlp/SkillNet/tree/main/examples/JiuwenClaw)
    - **🔌 [2026-03-12] SkillNet MCP Server Released!** — We've launched the Model Context Protocol (MCP) integration (maintained by CycleChain, special thanks for this great contribution!).
    - **📄 [2026-03-04] SkillNet Technical Report Released!** — We've published the comprehensive SkillNet Technical Report, covering the system architecture, automated creation pipeline, multi-dimensional evaluation methodology, and the released open-source toolkits. [View Report →](https://arxiv.org/abs/2603.04448)
    - **🦞 [2026-02-23] OpenClaw Integration Released!** — SkillNet is now available as a built-in skill for OpenClaw. One command to install, zero config to use. The agent automatically searches, downloads, creates, evaluates, and analyzes skills on your behalf.
    """)

    # Features
    st.markdown("## ✨ Key Features")
    st.markdown("""
    | Feature | Description |
    | :--- | :--- |
    | 🔍&nbsp;**Search** | Find skills via keyword match or AI semantic search across 500+ curated skills |
    | 📦&nbsp;**One&#8209;Line&nbsp;Install** | `skillnet download <url>` — grab any skill from GitHub in seconds |
    | ✨&nbsp;**Auto&#8209;Create** | Convert GitHub repos, PDFs/PPTs/Word docs, conversation logs, or text prompts into structured skill packages using LLMs |
    | 📊&nbsp;**5&#8209;D&nbsp;Evaluation** | Score skills on **Safety · Completeness · Executability · Maintainability · Cost‑Awareness** |
    | 🕸️&nbsp;**Skill&nbsp;Graph** | Auto-discover `similar_to` · `belong_to` · `compose_with` · `depend_on` links between skills |
    """)

    st.markdown("---")

    # Quick Start
    st.markdown("## 🚀 Quick Start")
    
    st.code("pip install skillnet-ai", language="bash")

    st.code("""from skillnet_ai import SkillNetClient

client = SkillNetClient()  # No API key needed for search & download

# Search for skills
results = client.search(q="pdf", limit=5)
print(results[0].skill_name, results[0].stars)

# Install a skill
client.download(url=results[0].skill_url, target_dir="./my_skills")""", language="python")

    st.markdown("**🌐 SkillNet Web** — Search, download individual skills, and explore curated skill collections through the [SkillNet website](http://skillnet.openkg.cn/).")
    
    st.markdown("**🤖 OpenClaw + SkillNet** — See SkillNet in action with [OpenClaw](https://github.com/openclaw/openclaw). The agent automatically searches, creates, evaluates, and analyzes skills on your behalf.")

    st.markdown("---")

    # REST API
    st.markdown("## 🌐 REST API")
    st.markdown("The SkillNet search API is free, public, and requires no authentication.")
    
    st.code("""# Keyword search
curl "http://api-skillnet.openkg.cn/v1/search?q=pdf&sort_by=stars&limit=5"

# Semantic search
curl "http://api-skillnet.openkg.cn/v1/search?q=reading%20charts&mode=vector&threshold=0.8\"""", language="bash")

    with st.expander("📡 Full Parameter Reference"):
        st.markdown("**Endpoint:** `GET http://api-skillnet.openkg.cn/v1/search`")
        st.markdown("""
        | Parameter | Type | Default | Description |
        | :--- | :--- | :--- | :--- |
        | `q` | string | _required_ | Search query (keywords or natural language) |
        | `mode` | string | `keyword` | `keyword` (fuzzy match) or `vector` (semantic AI) |
        | `category` | string | — | Filter: Development, AIGC, Research, Science, etc. |
        | `limit` | int | `10` | Results per page (max 50) |
        | `page` | int | `1` | Page number _(keyword mode only)_ |
        | `min_stars` | int | `0` | Minimum star count _(keyword mode only)_ |
        | `sort_by` | string | `stars` | `stars` or `recent` _(keyword mode only)_ |
        | `threshold` | float | `0.8` | Similarity threshold 0.0–1.0 _(vector mode only)_ |
        """)
        
        st.markdown("**Response:**")
        st.code("""{
  "data": [
    {
      "skill_name": "pdf-extractor-v1",
      "skill_description": "Extracts text and tables from PDF documents.",
      "author": "openkg-team",
      "stars": 128,
      "skill_url": "https://...",
      "category": "Productivity"
    }
  ],
  "meta": { "query": "pdf", "mode": "keyword", "total": 1, "limit": 10 },
  "success": true
}""", language="json")

    st.markdown("---")

    # Python SDK
    st.markdown("## 🐍 Python SDK")

    st.markdown("### Initialize")
    st.code("""from skillnet_ai import SkillNetClient

client = SkillNetClient(
    api_key="sk-...",         # Required for create / evaluate / analyze
    # base_url="...",         # Optional: custom LLM endpoint
    # github_token="ghp-..." # Optional: for private repos
)""", language="python")

    st.markdown("### Search")
    st.code("""# Keyword search
results = client.search(q="pdf", limit=10, min_stars=5, sort_by="stars")

# Semantic search
results = client.search(q="analyze financial PDF reports", mode="vector", threshold=0.85)

if results:
    print(f"{results[0].skill_name} ⭐{results[0].stars}")""", language="python")

    st.markdown("### Install")
    st.code("""local_path = client.download(
    url="https://github.com/anthropics/skills/tree/main/skills/skill-creator",
    target_dir="./my_skills"
)""", language="python")

    st.markdown("### Create")
    st.markdown("Convert diverse sources into structured skill packages with a single call:")
    st.code("""# From conversation logs / execution traces
client.create(trajectory_content="User: rename .jpg to .png\\nAgent: Done.", output_dir="./skills")

# From GitHub repository
client.create(github_url="https://github.com/zjunlp/DeepKE", output_dir="./skills")

# From office documents (PDF / PPT / Word)
client.create(office_file="./guide.pdf", output_dir="./skills")

# From natural language prompt
client.create(prompt="A skill for web scraping article titles", output_dir="./skills")""", language="python")

    st.markdown("### Evaluate")
    st.markdown("Score any skill across 5 quality dimensions. Accepts local paths or GitHub URLs.")
    st.code("""result = client.evaluate(
    target="https://github.com/anthropics/skills/tree/main/skills/algorithmic-art"
)
# Returns: { "safety": {"level": "Good", "reason": "..."}, "completeness": {...}, ... }""", language="python")

    st.markdown("### Analyze Relationships")
    st.markdown("Map the connections between skills in a local directory — outputs `similar_to`, `belong_to`, `compose_with`, and `depend_on` edges.")
    st.code("""relationships = client.analyze(skills_dir="./my_skills")

for rel in relationships:
    print(f"{rel['source']} --[{rel['type']}]--> {rel['target']}")
# PDF_Parser --[compose_with]--> Text_Summarizer""", language="python")

    st.markdown("---")

    # CLI Reference
    st.markdown("## 💻 CLI Reference")
    st.markdown("The CLI ships with `pip install skillnet-ai` and offers the same features with rich terminal output.")
    
    st.markdown("""
    | Command | Description | Example |
    | :--- | :--- | :--- |
    | `search` | Find skills | `skillnet search "pdf" --mode vector` |
    | `download` | Install a skill | `skillnet download <url> -d ./skills` |
    | `create` | Create from any source | `skillnet create log.txt --model gpt-4o` |
    | `evaluate` | Quality report | `skillnet evaluate ./my_skill` |
    | `analyze` | Relationship graph | `skillnet analyze ./my_skills` |
    """)
    st.info("> Use `skillnet <command> --help` for full options.")

    st.markdown("### Search")
    st.code("""skillnet search "pdf"
skillnet search "analyze financial reports" --mode vector --threshold 0.85
skillnet search "visualization" --category "Development" --sort-by stars --limit 10""", language="bash")

    st.markdown("### Install")
    st.code("""skillnet download https://github.com/anthropics/skills/tree/main/skills/algorithmic-art
skillnet download <url> -d ./my_agent/skills
skillnet download <private_url> --token <your_github_token>

# Use a mirror for faster downloads in restricted networks
skillnet download <url> --mirror https://ghfast.top/""", language="bash")

    st.markdown("### Create")
    st.code("""# From trajectory file
skillnet create ./logs/trajectory.txt -d ./generated_skills

# From GitHub repo
skillnet create --github https://github.com/owner/repo

# From office document (PDF, PPT, Word)
skillnet create --office ./docs/guide.pdf

# From prompt
skillnet create --prompt "A skill for extracting tables from images\"""", language="bash")

    st.markdown("### Evaluate")
    st.code("""skillnet evaluate https://github.com/anthropics/skills/tree/main/skills/algorithmic-art
skillnet evaluate ./my_skills/web_search
skillnet evaluate ./my_skills/tool --category "Development" --model gpt-4o""", language="bash")

    st.markdown("### Analyze")
    st.code("""skillnet analyze ./my_agent_skills
skillnet analyze ./my_agent_skills --no-save   # print only, don't write file
skillnet analyze ./my_agent_skills --model gpt-4o""", language="bash")

    st.markdown("---")

    # Configuration
    st.markdown("## ⚙️ Configuration")
    
    st.markdown("### Environment Variables")
    st.markdown("""
    | Variable | Required For | Default |
    | :--- | :--- | :--- |
    | `API_KEY` | `create` · `evaluate` · `analyze` | — |
    | `BASE_URL` | Custom LLM endpoint | `https://api.openai.com/v1` |
    | `GITHUB_TOKEN` | Private repos / higher rate limits | — |
    | `SKILLNET_MODEL` | Default LLM model for all commands | `gpt-4o` |
    | `GITHUB_MIRROR` | Faster downloads in restricted networks | — |
    """)
    st.info("> `search` and `download` (public repos) work without any credentials.\n>\n> **Recommended mirror:** [`https://ghfast.top/`](https://ghfast.top/) — set `GITHUB_MIRROR` or pass `--mirror` to speed up downloads in restricted networks.")

    st.markdown("**Linux / macOS:**")
    st.code("""export API_KEY="sk-..."
export BASE_URL="https://..."  # optional""", language="bash")

    st.markdown("**Windows PowerShell:**")
    st.code("""$env:API_KEY = "sk-..."
$env:BASE_URL = "https://..."  # optional""", language="powershell")

    st.markdown("---")

    # Example: Scientific Discovery
    st.markdown("## 🔬 Example: Scientific Discovery")
    st.markdown("A complete end-to-end demo showing how an AI Agent uses SkillNet to autonomously plan and execute a complex scientific workflow — from raw scRNA-seq data to a cancer target validation report.")
    
    st.markdown("""
    | Step | Phase | Description |
    | :--- | :--- | :--- |
    | 1️⃣ | **Task** | User provides a goal: "Analyze scRNA-seq data to find cancer targets" |
    | 2️⃣ | **Plan** | Agent decomposes into: Data → Mechanism → Validation → Report |
    | 3️⃣ | **Discover** | `client.search()` finds *cellxgene-census*, *kegg-database*, etc. |
    | 4️⃣ | **Evaluate** | Skills are quality-gated via `client.evaluate()` before use |
    | 5️⃣ | **Execute** | Skills run sequentially to produce a final discovery report |
    """)

    st.markdown("👉 **[Try the Interactive Demo](http://skillnet.openkg.cn/)** (Website → Scenarios → Science)  \n📓 **[View Notebook](https://github.com/zjunlp/SkillNet/blob/main/examples/scientific_workflow_demo.ipynb)**")

    st.markdown("---")

    # OpenClaw Integration
    st.markdown("## 🤖 OpenClaw Integration")
    st.markdown("SkillNet integrates with [OpenClaw](https://github.com/openclaw/openclaw) as a built-in, lazy-loaded skill. Once installed, your agent automatically:")
    st.markdown("""
    - **Searches** existing skills before starting complex tasks
    - **Creates** new skills from repos, documents, or completed work
    - **Evaluates & analyzes** your local library for quality and inter-skill relationships
    """)
    st.info("> Community skills guide execution → successful outcomes become new skills → periodic analysis keeps the library clean.")

    st.markdown("### 📥 Installation")
    st.markdown("**Prerequisites:** [OpenClaw](https://github.com/openclaw/openclaw) installed (default workspace: `~/.openclaw/workspace`)")
    
    st.markdown("**Option A — CLI:**")
    st.code("""npm i -g clawhub
clawhub install skillnet --workdir ~/.openclaw/workspace
openclaw gateway restart""", language="bash")

    st.markdown("**Option B — Via OpenClaw chat:**")
    st.code("Install the skillnet skill from ClawHub.", language="text")

    st.markdown("### ⚙️ Configuration")
    st.markdown("The same three parameters (`API_KEY`, `BASE_URL`, `GITHUB_TOKEN`) apply here — see [Configuration](#configuration) for details.")
    st.markdown("In OpenClaw, you can pre-configure them in `openclaw.json` so the agent uses them silently — no prompts, no interruptions. If not configured, the agent only asks when a command actually needs the value, injects it for that single call, and never pollutes the global environment.")
    
    st.markdown("**Recommended: pre-configure in `openclaw.json`**:")
    st.code("""{
  "skills": {
    "entries": {
      "skillnet": {
        "enabled": true,
        "apiKey": "sk-REPLACE_ME",
        "env": {
          "BASE_URL": "https://api.openai.com/v1",
          "GITHUB_TOKEN": "ghp_REPLACE_ME"
        }
      }
    }
  }
}""", language="json")

    st.markdown("### 🧪 Quick Verification")
    st.markdown("In your OpenClaw chat, try:")
    
    st.markdown("**No credentials needed:**")
    st.code('Search SkillNet for a "docker" skill and summarize the top result.', language="text")
    
    st.markdown("**Requires API key:**")
    st.code("Create a skill from this GitHub repo: https://github.com/owner/repo (then evaluate it).", language="text")

    st.markdown("---")

    # MCP Integration
    st.markdown("## 🔌 Model Context Protocol (MCP) Integration")
    st.markdown("The **SkillNet MCP Server** (maintained by [CycleChain](https://github.com/CycleChain)) is a high-performance bridge that enables AI agents (such as Claude Desktop, Cursor, Antigravity and Windsurf) to interact with the SkillNet ecosystem using the [Model Context Protocol](https://modelcontextprotocol.io/).")
    
    st.markdown("### Installation Options")
    
    st.markdown("#### 1. Source Build (Node.js & Python)")
    st.markdown("Ideal for users who want to run the server locally with existing dependencies.")
    st.code("""git clone https://github.com/CycleChain/skillnet-mcp
cd skillnet-mcp
npm install && npm run build""", language="bash")

    st.markdown("#### 2. Docker (Dependency-free)")
    st.markdown("The most robust way to run the server using the official image from [Docker Hub](https://hub.docker.com/r/fmdogancan/skillnet-mcp).")
    st.code("docker pull fmdogancan/skillnet-mcp:latest", language="bash")

    st.markdown("### Quick Configuration (Claude Desktop)")
    st.markdown("Add the following to your `claude_desktop_config.json`:")
    
    st.markdown("#### Option A: Docker (Recommended)")
    st.code("""{
  "mcpServers": {
    "skillnet": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "fmdogancan/skillnet-mcp:latest"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}""", language="json")

    st.markdown("#### Option B: Build Locally")
    st.code("docker build -t skillnet-mcp-local .", language="bash")
    st.markdown("*(Then, replace `fmdogancan/skillnet-mcp:latest` with `skillnet-mcp-local` in the JSON config above)*")

    st.markdown("#### Option C: Source Build")
    st.code("""{
  "mcpServers": {
    "skillnet": {
      "command": "node",
      "args": ["/absolute/path/to/skillnet-mcp/build/index.js"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}""", language="json")

    st.info("> **Note:** `search_skills` and `download_skill` tools do not require an API key. An `API_KEY` is only required for `create`, `evaluate`, and `analyze` features.")

    st.markdown("### Supported Environment Variables")
    st.markdown("""
    * `API_KEY`: Your API key
    * `GITHUB_TOKEN`: GitHub token for private repositories
    """)

    st.markdown("---")

    # Contributing
    st.markdown("## 🤝 Contributing")
    st.markdown("Contributions of all kinds are welcome! Whether it's fixing a typo, adding a feature, or sharing a new skill — every contribution counts.")
    
    st.markdown("""
    1. **Fork** the repository
    2. **Create** a feature branch (`git checkout -b feat/amazing-feature`)
    3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
    4. **Push** to the branch (`git push origin feat/amazing-feature`)
    5. **Open** a Pull Request
    """)
    
    st.markdown("📤 **[Contribute skills](http://skillnet.openkg.cn/)** (Website → Contribute → Submit via URL / Upload Local Skill / Batch Upload Skills)")
    st.markdown("You can also [open an Issue](https://github.com/zjunlp/SkillNet/issues) to report bugs or suggest features.")

    st.markdown("---")

    # Citation
    st.markdown("## 📚 Citation")
    st.markdown("If you find this work useful, please kindly ⭐ the [Repo](https://github.com/zjunlp/SkillNet) and cite our paper!")
    st.code("""@misc{liang2026skillnetcreateevaluateconnect,
      title={SkillNet: Create, Evaluate, and Connect AI Skills}, 
      author={Yuan Liang and Ruobin Zhong and Haoming Xu and Chen Jiang and Yi Zhong and Runnan Fang and Jia-Chen Gu and Shumin Deng and Yunzhi Yao and Mengru Wang and Shuofei Qiao and Xin Xu and Tongtong Wu and Kun Wang and Yang Liu and Zhen Bi and Jungang Lou and Yuchen Eleanor Jiang and Hangcheng Zhu and Gang Yu and Haiwen Hong and Longtao Huang and Hui Xue and Chenxi Wang and Yijun Wang and Zifei Shan and Xi Chen and Zhaopeng Tu and Feiyu Xiong and Xin Xie and Peng Zhang and Zhengke Gui and Lei Liang and Jun Zhou and Chiyu Wu and Jin Shang and Yu Gong and Junyu Lin and Changliang Xu and Hongjie Deng and Wen Zhang and Keyan Ding and Qiang Zhang and Fei Huang and Ningyu Zhang and Jeff Z. Pan and Guilin Qi and Haofen Wang and Huajun Chen},
      year={2026},
      eprint={2603.04448},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2603.04448}, 
}""", language="bibtex")