# import streamlit as st
# from utils import render_navbar
# from PIL import Image
# import os

# # 1. 页面配置
# st.set_page_config(
#     page_title="Ontology - SkillNet",
#     page_icon="🧬",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # 隐藏默认侧边栏的 CSS (与参考代码一致)
# st.markdown(
#     """
#     <style>
#         [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
#             display: none;
#         }
#         .ontology-header {
#             text-align: center;
#             margin-bottom: 2rem;
#         }
#         .layer-box {
#             background-color: #f0f2f6;
#             padding: 20px;
#             border-radius: 10px;
#             height: 100%;
#             border-left: 5px solid #4e8cff;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 2. 渲染导航栏
# render_navbar()

# # 3. 页面内容

# # --- 头部介绍 ---
# st.title("🧬 Skill Ontology")
# st.markdown(
#     """
#     <div style="font-size: 1.1em; color: #666; margin-bottom: 30px;">
#     Skill Ontology organizes individual skills into a structured, composable network, enabling agents to reason, plan, and execute complex tasks as an extensible, maintainable capability system.
#     </div>
#     """, 
#     unsafe_allow_html=True
# )

# # --- 图片展示区 ---
# col_spacer1, col_img, col_spacer2 = st.columns([1, 4, 1])

# with col_img:
#     image_path = "images/ontology.png"
#     if os.path.exists(image_path):
#         st.image(image_path, caption="Figure: The Skill Ontology for SkillNet", width='stretch')
#     else:
#         st.error(f"Image not found at {image_path}")

# st.markdown("---")

# # --- 分层详解 (三列布局对应图中的三层) ---
# st.subheader("Architecture")

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown('<div class="layer-box">', unsafe_allow_html=True)
#     st.markdown("### 1. Skill Taxonomy")
#     st.markdown("**The Abstraction Layer**")
#     st.write("""
#     The top layer defines the broad categorization of skills. It organizes capabilities into domains such as:
#     """)
#     st.markdown("""
#     * **Development**: Engineering, coding, DBs (SQL), DevOps & deployment.
#     * **AIGC**: GenAI content: text-to-image, video, voice & creative writing.
#     * **Research**: Info retrieval, web scraping, summarization & intelligence.
#     * **Science**: Math solving, simulations (physics/bio) & academic modeling.
#     * **Business**: Enterprise ops, finance, marketing (CRM) & data analytics.
#     * **Testing**: QA, bug verification, unit & integration testing.
#     * **Productivity**: Efficiency tools: email, calendar, docs & translation.
#     * **Security**: Cybersecurity, auth, encryption & vulnerability scanning.
#     * **Lifestyle**: Personal tasks: travel, shopping, health & smart home.
#     """)
#     st.caption("Purpose: To provide a structured vocabulary for skill classification.")
#     st.markdown('</div>', unsafe_allow_html=True)

# with col2:
#     st.markdown('<div class="layer-box">', unsafe_allow_html=True)
#     st.markdown("### 2. Skill Relation Graph")
#     st.markdown("**The Semantic Layer**")
#     st.write("""
#     The middle layer instantiates specific skills and defines how they interact. It maps relationships using edges like:
#     """)
#     st.markdown("""
#     * **`compose_with`**: Combining patterns (e.g., nextjs-expert + react-patterns).
#     * **`similar_to`**: Mapping alternatives (e.g., seaborn ↔ matplotlib).
#     * **`depend_on`**: Establishing prerequisites. (e.g., react-patterns → react).
#     * **`belong_to`**: A sub-component within a larger workflow (e.g., playwright → browser-automation).
#     """)
#     st.caption("Purpose: To enable reasoning about skill compatibility and composition.")
#     st.markdown('</div>', unsafe_allow_html=True)

# with col3:
#     st.markdown('<div class="layer-box">', unsafe_allow_html=True)
#     st.markdown("### 3. Skill Package Library")
#     st.markdown("**The Execution Layer**")
#     st.write("""
#     The bottom layer groups related skills into deployable packages. These serve as functional units for agents:
#     """)
#     st.markdown("""
#     * **`react-nextjs-fullstack`**: Complete web dev stack.
#     * **`data-science-visualization`**: Analysis & plotting tools.
#     * **`e2e-browser-testing`**: Automation workflows.
#     * ...
#     """)
#     st.caption("Purpose: To provide ready-to-use toolkits for specific agent tasks.")
#     st.markdown('</div>', unsafe_allow_html=True)

# # --- 底部 Call to Action 或 额外说明 ---
# st.markdown("<br>", unsafe_allow_html=True)
# st.info("💡 **Ontology in Action**: When a user queries for a specific task, SkillNet traverses this graph to identify the necessary packages and skills to construct a capable agent.")



# import streamlit as st
# from utils import render_navbar
# from PIL import Image
# import os

# # 1. 页面配置
# st.set_page_config(
#     page_title="Ontology - SkillNet",
#     page_icon="🧬",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # CSS 优化：
# # 1. 隐藏侧边栏
# # 2. 优化图片样式，增加圆角和阴影
# # 3. 调整标题间距
# st.markdown(
#     """
#     <style>
#         [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
#             display: none;
#         }
#         .stImage img {
#             border-radius: 10px;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         }
#         h3 {
#             padding-bottom: 10px;
#         }
#         /* 增加一些微小的各列间距优化 */
#         [data-testid="column"] {
#             padding: 0.5rem;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 2. 渲染导航栏
# render_navbar()

# # 3. 页面内容

# # --- 头部区域：左文右图 (解决图片突兀的问题) ---
# st.markdown("<br>", unsafe_allow_html=True) # 顶部留白

# top_col1, top_col2 = st.columns([5, 4], gap="large")

# with top_col1:
#     st.title("🧬 Skill Ontology")
#     # st.markdown("#### The Brain of the Agent System")
#     st.write("") # Spacer
#     st.markdown(
#         """
#         Skill Ontology organizes individual skills into a **structured, composable network**. 
#         It acts as the semantic map that enables agents to:
        
#         * **Reason** about what tools are needed.
#         * **Plan** complex execution paths.
#         * **Extend** capabilities without breaking existing logic.
#         """
#     )
    
#     # 底部 Call to Action 移到这里，作为原本介绍的补充
#     st.info("💡 **Ontology in Action**: When a user queries for a task, SkillNet traverses this graph to identify the necessary packages and skills to construct a capable agent.")

# with top_col2:
#     image_path = "images/ontology.png"
#     if os.path.exists(image_path):
#         st.image(image_path, caption="Figure: The Skill Ontology Structure", width='stretch')
#     else:
#         # 如果找不到图片，使用占位符，避免报错破坏布局
#         st.warning(f"Image placeholder (File not found: {image_path})")

# st.markdown("---")

# # --- 分层详解 (三列布局) ---
# st.subheader("Architecture Layers")

# # 使用 st.container(border=True) 替代原来的 CSS box
# # 这会让内容看起来像是一个干净的面板，而不是可点击的按钮
# col1, col2, col3 = st.columns(3, gap="medium")

# # --- Layer 1: Taxonomy (精简版) ---
# with col1:
#     with st.container(border=True):
#         st.markdown("### 1. Taxonomy")
#         st.caption("The Abstraction Layer")
        
#         st.markdown("""
#         The foundational dictionary of skills. It categorizes capabilities into high-level domains to provide a structured vocabulary.
#         """)
        
#         # 优化：不列出所有，而是用粗体突出核心领域，节省空间
#         st.markdown("**Core Domains:**")
#         st.markdown("""
#         * 💻 **Tech**: Dev, DevOps, DBs, Security
#         * 🧠 **Intelligence**: AIGC, Research, Science
#         * 🏢 **Ops**: Business, Productivity, Testing
#         * 🏠 **Life**: Lifestyle, Smart Home
#         """)
        
#         st.markdown("<br>", unsafe_allow_html=True) # 稍微占位保持对齐
#         st.caption("Purpose: Classification & Vocabulary.")

# # --- Layer 2: Relation Graph ---
# with col2:
#     with st.container(border=True):
#         st.markdown("### 2. Relation Graph")
#         st.caption("The Semantic Layer")
        
#         st.markdown("""
#         Defines how skills interact and connect. It maps logical relationships to enable reasoning about compatibility.
#         """)
        
#         st.markdown("**Key Relationships:**")
#         # 使用代码块展示关系，显得更专业且紧凑
#         st.code("""
# compose_with  # Combination
# similar_to    # Alternatives
# depend_on     # Prerequisites
# belong_to     # Hierarchy
#         """, language="yaml")
        
#         st.caption("Purpose: Reasoning & Composition.")

# # --- Layer 3: Package Library ---
# with col3:
#     with st.container(border=True):
#         st.markdown("### 3. Package Library")
#         st.caption("The Execution Layer")
        
#         st.markdown("""
#         Groups related skills into deployable units. These are the actual functional toolkits agents load at runtime.
#         """)
        
#         st.markdown("**Deployable Units:**")
#         st.markdown("""
#         * 📦 `react-nextjs-fullstack`
#         * 📊 `data-science-viz`
#         * 🧪 `e2e-browser-testing`
#         * 🔒 `security-audit-tools`
#         """)
        
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.caption("Purpose: Deployment & Execution.")


import streamlit as st
from utils import render_navbar
from icon_helper import icon
from PIL import Image
import os
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent

# 1. 页面配置
st.set_page_config(
    page_title="Ontology - SkillNet",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS 样式定义 (核心修改部分)
st.markdown(
    """
    <style>
        /* 隐藏侧边栏 */
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* 顶部图片样式 */
        .stImage img {
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        /* --- 卡片特效核心 CSS --- */
        .skill-card {
            background-color: #FFFFFF; /* 纯白背景 */
            border-radius: 15px;       /* 圆角 */
            padding: 25px;             /* 内边距 */
            height: 100%;              /* 撑满高度 */
            color: #31333F;            /* 强制字体颜色（防止深色模式下看不清） */
            border: 1px solid #E0E0E0; /* 极细的边框 */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); /* 默认轻微阴影 */
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); /* 平滑过渡动画 */
        }

        /* 鼠标悬停时的效果 */
        .skill-card:hover {
            transform: translateY(-8px); /* 向上浮动 */
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15); /* 加深阴影，制造悬浮感 */
            border-color: #4e8cff; /* 边框变色，增加交互感 */
        }

        /* 卡片内部标题样式 */
        .skill-card h3 {
            margin-top: 0;
            margin-bottom: 5px;
            font-size: 1.3rem;
            color: #1f77b4; /* 标题蓝色 */
        }
        
        .skill-card .caption {
            font-size: 0.9rem;
            color: #888;
            margin-bottom: 15px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* 卡片内部代码块模拟 */
        .code-box {
            background-color: #f5f7f9;
            border-radius: 6px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            color: #333;
            border: 1px solid #eee;
        }
        
        /* 列表样式优化 */
        .skill-card ul {
            padding-left: 20px;
            margin-bottom: 0;
        }
        .skill-card li {
            margin-bottom: 8px;
            font-size: 0.95rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 渲染导航栏
render_navbar(active_page="ontology")

# 3. 页面内容

# --- 头部区域：左文右图 ---
# st.markdown("<br>", unsafe_allow_html=True) 

top_col1, top_col2 = st.columns([4, 4], gap="large")

with top_col1:
    st.markdown(f"<h1 style='font-size:2.5rem;font-weight:700;'>{icon('grid-3x3', 28, '#1f77b4')} Skill Ontology</h1>", unsafe_allow_html=True)
    st.write("") 
    st.markdown(
        """
        <div style="font-size: 1.25em; color: #444; line-height: 1.6;">
        Skill Ontology organizes individual skills into a <b>structured, composable network</b>, 
        enabling agents to reason, plan, and execute complex tasks as an <b>extensible, maintainable capability system</b>.
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write("")
    st.write("")
    st.markdown(f"""<div style="background-color:#f0f9ff;border-left:4px solid #3b82f6;padding:12px 16px;border-radius:6px;font-size:0.95rem;color:#1e3a5f;">
    {icon('zap', 16, '#f59e0b')} <b>Ontology in Action</b>: When a user queries for a task, SkillNet traverses this graph to identify the necessary collections and skills to construct a capable agent.
    </div>""", unsafe_allow_html=True)

with top_col2:
    image_path = _PROJECT / "images" / "ontology.png"
    if image_path.exists():
        st.image(str(image_path), caption="Figure: The Skill Ontology for SkillNet", width='stretch')
    else:
        st.warning(f"Image placeholder (File not found: {image_path})")

st.markdown("---")

# --- 分层详解 (自定义 HTML 卡片) ---
st.subheader("Architecture")
st.markdown("<br>", unsafe_allow_html=True) # 微调间距

col1, col2, col3 = st.columns(3, gap="medium")

# --- Layer 1: Taxonomy ---
with col1:
    st.markdown(f"""
    <div class="skill-card">
        <h3>{icon('code-2', 18, '#1f77b4')} 1. Skill Taxonomy</h3>
        <div class="caption">The Abstraction Layer</div>
        <p>The top layer defines the broad categorization and detailed tags of skills. It organizes capabilities into categories such as:</p>
        <ul>
            <li>{icon('code-2', 14, '#6b7280')} Development, AIGC, Testing, Security</li>
            <li>{icon('flask-conical', 14, '#6b7280')} Research, Science</li>
            <li>{icon('bar-chart-3', 14, '#6b7280')} Business, Productivity</li>
            <li>{icon('heart', 14, '#6b7280')} Lifestyle</li>
        </ul>
        <br>
        <small style="color:#999">Purpose: Classification & Vocabulary</small>
    </div>
    """, unsafe_allow_html=True)

# --- Layer 2: Relation Graph ---
with col2:
    st.markdown(f"""
    <div class="skill-card">
        <h3>{icon('link', 18, '#1f77b4')} 2. Skill Relation Graph</h3>
        <div class="caption">The Semantic Layer</div>
        <p>The middle layer instantiates specific skills and defines how they interact. It maps relationships using edges like:</p>
        <ul>
            <li>compose_with: Combining patterns.</li>
            <li>similar_to: Mapping alternatives.</li>
            <li>depend_on: Establishing prerequisites.</li>
            <li>belong_to: A sub-component within a larger skill.</li>
        </ul>
        <br>
        <small style="color:#999">Purpose: Reasoning & Composition</small>
    </div>
    """, unsafe_allow_html=True)

# --- Layer 3: Package Library ---
with col3:
    st.markdown(f"""
    <div class="skill-card">
        <h3>{icon('package', 18, '#1f77b4')} 3. Skill Collection</h3>
        <div class="caption">The Execution Layer</div>
        <p>Groups related skills into deployable units. These are the actual functional toolkits agents load at runtime. Examples:</p>
        <ul>
            <li>{icon('package', 14, '#6b7280')} react-nextjs-fullstack</li>
            <li>{icon('bar-chart-3', 14, '#6b7280')} data-science-viz</li>
            <li>{icon('flask-conical', 14, '#6b7280')} e2e-browser-testing</li>
            <li>{icon('shield-check', 14, '#6b7280')} security-audit-tools</li>
        </ul>
        <br>
        <small style="color:#999">Purpose: Deployment & Execution</small>
    </div>
    """, unsafe_allow_html=True)