import streamlit as st
from utils import render_navbar, handle_redirects, render_logos, get_embedding
import pandas as pd
import html
import math
import urllib.parse
from supabase import create_client, Client
import textwrap

# 处理可能的跳转
handle_redirects()

# --- 页面配置 ---
st.set_page_config(
    page_title="SkillNet - Create, Evaluate, and Connect AI Skills",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed" # 默认收起侧边栏，实际上我们会清空它
)
st.markdown(
    """
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 定义分类常量 ---
CATEGORY_OPTIONS = [
    "All", "Development", "AIGC", "Research", "Science", "Business", 
    "Testing", "Productivity", "Security", "Lifestyle", "Other"
]

# --- CSS 美化 (更新为卡片网格风格) ---
st.markdown("""
<style>
    /* 全局背景微调，让白色卡片更突出 */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* 卡片样式：模仿 MCP Servers 的白色卡片风格 */
    .skill-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
        height: 380px; /* 固定高度，确保网格整齐 */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .skill-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #d1d5db;
    }

    /* 标题区域 */
    .card-header {
        margin-bottom: 10px;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .skill-title { 
        font-size: 1.1em; 
        font-weight: 700; 
        color: #111827; 
        text-decoration: none; 
        display: block;
        margin-bottom: 4px;
        white-space: normal;      /* 允许换行 */
        overflow-wrap: break-word; /* 超长单词也会换行 */
    }
    
    .skill-title:hover {
        color: #2563eb;
    }

    /* 描述文本 */
    .skill-desc { 
        margin-top: 10px;
        font-size: 0.9em; 
        color: #4b5563; 
        line-height: 1.5; 
        margin-bottom: 15px; 
        flex-grow: 1; /* 让描述占据剩余空间 */
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 5; /* 限制显示行 */
        -webkit-box-orient: vertical;
    }

    /* 底部元数据 */
    .skill-footer {
        border-top: 1px solid #f3f4f6;
        padding-top: 12px;
        font-size: 0.8em;
        color: #6b7280;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .skill-eval-bar {
        /* 关键：使用 dashed 虚线与 footer 的实线区分 */
        border-top: 0.5px dashed #efefef; 
        margin-top: auto;        /* 磁力效果：自动推到卡片底部 */
        padding: 0px 0 -1px 0;    /* 上下间距 */
        display: flex;
        flex-wrap: nowrap;       /* 强制不换行 */
        gap: 4px;                /* 徽章之间的间距 */
        overflow-x: auto;        /* 溢出时可横向滚动 */
        scrollbar-width: none;   /* 隐藏滚动条 (Firefox) */
    }


    /* 标签样式 */
    .tag { 
        margin-top: 10px;
        display: inline-block; 
        background-color: #f3f4f6; 
        border-radius: 9999px; 
        padding: 2px 8px; 
        font-size: 0.75em; 
        margin-right: 4px; 
        color: #374151; 
        font-weight: 500;
    }
    
    .star-badge { 
        background-color: #f1f5f9; /* Soft Slate Gray */
        color: #475569;            /* Darker Slate for text contrast */
        padding: 2px 8px; 
        border-radius: 9999px; 
        font-weight: 600; 
        font-size: 0.75em;
        border: 1px solid #e2e8f0; /* Optional: adds a subtle definition */
    }

    /* 搜索框居中样式调整 */
    div[data-testid="stTextInput"] input {
        border-radius: 20px;
        padding-left: 20px;
    }
    
    /* 分页居中 */
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 初始化 Supabase ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["supabase"]["SUPABASE_URL"]
        key = st.secrets["supabase"]["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        # st.error(f"连接失败: {e}") # 暂时注释，避免本地运行报错
        return None

supabase = init_connection()

# # --- 数据加载函数 (逻辑保持不变) ---
# def fetch_skills(page=1, page_size=20, search_text=None, min_stars=0, category=None, sort_option="Stars"):
#     if not supabase: 
#         # Mock data for demonstration if no DB connection
#         mock_data = [
#             {"skill_name": "Example Skill 1", "stars": 120, "category": "AIGC", "author": "UserA", "skill_description": "This is a demo description meant to simulate the card layout.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-01-01"},
#             {"skill_name": "Data Tool Pro", "stars": 85, "category": "Data & Research", "author": "UserB", "skill_description": "Another tool for data analysis.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-02-15"},
#             {"skill_name": "Web Scraper", "stars": 200, "category": "Web & GUI", "author": "UserC", "skill_description": "Scrapes the web efficiently.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-03-10"},
#             {"skill_name": "Auto Docs", "stars": 95, "category": "Documentation", "author": "UserD", "skill_description": "Generate documentation automatically.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-04-05"},
#         ] * 5
#         return pd.DataFrame(mock_data), len(mock_data)
        
#     start = (page - 1) * page_size
#     end = start + page_size - 1

#     try:
#         query = supabase.table("skills").select("*", count="exact")
        
#         if search_text:
#             query = query.or_(f"skill_name.ilike.%{search_text}%,skill_description.ilike.%{search_text}%")
        
#         if min_stars > 0:
#             query = query.gte("stars", min_stars)
        
#         if category and category not in ["All", "Featured"]:
#             query = query.eq("category", category)
#         # elif category == "Featured":
#         #     query = query.eq("author", "anthropics")

#         if sort_option == "Stars":
#             query = query.order("stars", desc=True)
#         else: # Recent
#             query = query.order("skill_date", desc=True) # 假设数据库有 skill_date 字段
            
#         response = query.range(start, end).execute()
#         return pd.DataFrame(response.data), response.count

#     except Exception as e:
#         st.error(f"查询出错: {e}")
#         return pd.DataFrame(), 0
        
# def fetch_skills(page=1, page_size=20, search_text=None, min_stars=0, category=None, sort_option="Stars"):
#     if not supabase: 
#         # Mock data for demonstration if no DB connection
#         mock_data = [
#             {"skill_name": "Example Skill 1", "stars": 120, "category": "AIGC", "author": "UserA", "skill_description": "This is a demo description meant to simulate the card layout.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-01-01"},
#             {"skill_name": "Data Tool Pro", "stars": 85, "category": "Data & Research", "author": "UserB", "skill_description": "Another tool for data analysis.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-02-15"},
#             {"skill_name": "Web Scraper", "stars": 200, "category": "Web & GUI", "author": "UserC", "skill_description": "Scrapes the web efficiently.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-03-10"},
#             {"skill_name": "Auto Docs", "stars": 95, "category": "Documentation", "author": "UserD", "skill_description": "Generate documentation automatically.", "skill_url": "#", "repo_url": "#", "skill_date": "2023-04-05"},
#         ] * 5
#         return pd.DataFrame(mock_data), len(mock_data)
#     try:
#         # ======================================================
#         # 分支 A: 向量语义搜索 (当用户输入了搜索词)
#         # ======================================================
#         if search_text:
#             # 1. 生成向量
#             query_vector = get_embedding(search_text)
            
#             # 2. 准备 RPC 参数
#             rpc_params = {
#                 "query_embedding": query_vector,
#                 "match_threshold": 0.75,       # 根据需要调整阈值
#                 "match_count": 100,            # 搜索模式下，一次性限制返回最相关的 100 个
#                 "filter_category": category if category and category not in ["All", "Featured"] else None
#             }
            
#             # 3. 调用 RPC
#             response = supabase.rpc("search_skills_by_embedding", rpc_params).execute()
#             data = response.data
            
#             # 4. 如果有额外的 Python 端排序需求（比如按相似度或 Stars 再排一次）可以在这里做
#             # RPC 默认已经按 similarity 排序了
            
#             # 5. 为了兼容现有的翻页 UI，我们在 Python 端做切片
#             # 虽然向量搜索一般看前几个就够了，但为了不破坏 UI 逻辑：
#             total_count = len(data)
#             start = (page - 1) * page_size
#             end = start + page_size
#             sliced_data = data[start:end]
            
#             return pd.DataFrame(sliced_data), total_count

#         # ======================================================
#         # 分支 B: 普通列表展示 (无搜索词，原有逻辑)
#         # ======================================================
#         else:
#             start = (page - 1) * page_size
#             end = start + page_size - 1
            
#             query = supabase.table("skills").select("*", count="exact")
            
#             # 筛选逻辑
#             if min_stars > 0:
#                 query = query.gte("stars", min_stars)
            
#             if category and category not in ["All", "Featured"]:
#                 query = query.eq("category", category)

#             # 排序逻辑
#             if sort_option == "Stars":
#                 query = query.order("stars", desc=True)
#             else: # Recent
#                 query = query.order("skill_date", desc=True)
                
#             response = query.range(start, end).execute()
#             return pd.DataFrame(response.data), response.count

#     except Exception as e:
#         st.error(f"查询出错: {e}")
#         # 打印详细错误方便调试
#         print(e)
#         return pd.DataFrame(), 0

def fetch_skills(page=1, page_size=20, search_text=None, search_mode="vector", min_stars=0, category=None, sort_option="Stars"):
    if not supabase:
        # Mock logic (省略，保持你原有的即可)
        return pd.DataFrame(), 0
        
    try:
        # 定义分页范围
        start = (page - 1) * page_size
        end = start + page_size - 1

        # ======================================================
        # 情况 1: 用户输入了搜索词
        # ======================================================
        if search_text:
            
            # --- 分支 A: 向量语义搜索 ---
            if search_mode == "vector":
                query_vector = get_embedding(search_text)
                rpc_params = {
                    "query_embedding": query_vector,
                    "match_threshold": 0.70, # 稍微降低阈值以保证有结果
                    "match_count": 100,
                    "filter_category": category if category and category not in ["All", "Featured"] else None
                }
                response = supabase.rpc("search_skills_by_embedding", rpc_params).execute()
                data = response.data
                
                # 向量搜索通常是按相似度排序的，所以这里忽略 sort_option (除非你想在相似结果中再按 Star 排序)

                
                # Python 端分页
                total_count = len(data)
                sliced_data = data[start : start + page_size]
                return pd.DataFrame(sliced_data), total_count

            # --- 分支 B: 关键词匹配 (Keyword Match) ---
            else:
                # 基础查询
                query = supabase.table("skills").select("*", count="exact")
                
                # 1. 应用关键词过滤 (Name OR Description)
                # 使用 Supabase 的 or_ 语法: column.ilike.%value%
                # 注意：Supabase-py 的 filter 语法是链式的，or 内部需要写成特定字符串格式
                or_filter = f"skill_name.ilike.%{search_text}%,skill_description.ilike.%{search_text}%,tags.cs.{{{search_text}}}"
                query = query.or_(or_filter)
                
                # 2. 应用 Category 过滤
                if category and category not in ["All", "Featured"]:
                    query = query.eq("category", category)
                
                # 3. 应用 Stars 过滤
                if min_stars > 0:
                    query = query.gte("stars", min_stars)
                
                # 4. 排序 (关键词搜索下，用户通常希望看到按 Stars 或时间排序的结果)
                if sort_option == "Stars":
                    query = query.order("stars", desc=True)
                elif sort_option == "Recent":
                    query = query.order("skill_date", desc=True)
                
                # 5. 执行分页查询
                response = query.range(start, end).execute()
                return pd.DataFrame(response.data), response.count

        # ======================================================
        # 情况 2: 无搜索词 (默认展示列表)
        # ======================================================
        else:
            # 保持原有逻辑，不做变动
            query = supabase.table("skills").select("*", count="exact")
            
            if min_stars > 0:
                query = query.gte("stars", min_stars)
            
            if category and category not in ["All", "Featured"]:
                query = query.eq("category", category)

            if sort_option == "Stars":
                query = query.order("stars", desc=True)
            else: 
                query = query.order("skill_date", desc=True)
                
            response = query.range(start, end).execute()
            return pd.DataFrame(response.data), response.count

    except Exception as e:
        st.error(f"查询出错: {e}")
        print(e)
        return pd.DataFrame(), 0

# --- 分页回调 ---
def change_page(new_page):
    st.session_state.page = new_page

# --- 主逻辑 ---
def main():
    render_navbar()

    if 'page' not in st.session_state:
        st.session_state.page = 1

    # ==========================================
    # 1. 顶部 Header 区域 (模仿截图布局)
    # ==========================================
    
    # 标题居中
    st.markdown("<h1 style='text-align: center; margin-bottom: 0; font-size: 48px;'>Create, Evaluate, and Connect AI Skills</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 20px;'>SkillNet is an open infrastructure for creating, evaluating, and organizing AI skills at scale.</p>", unsafe_allow_html=True)
    st.write("") # Spacer

    # 搜索框 (居中，宽度限制)
    col_spacer_l, col_search, col_spacer_r = st.columns([1, 2, 1])
    with col_search:
        # 当用户输入时重置页码
        def reset_page(): st.session_state.page = 1
        # search_query = st.text_input("Search skills...", placeholder="Search skills name, description...", label_visibility="collapsed", on_change=reset_page)
        
        # 1. 搜索输入框
        c_spacer_l, c_input, c_mode, c_spacer_r = st.columns([0.1, 5, 1.2, 0.1], vertical_alignment="bottom")
        with c_mode:
            # 下拉框模式
            search_mode = st.selectbox(
                "Mode",
                ["keyword", "vector"],
                index=0,
                key="search_mode_select",
                label_visibility="collapsed", # 隐藏标签以保持与左侧对齐
                on_change=reset_page
            )
        current_mode = st.session_state.get("search_mode_select", "vector")
        if current_mode == "vector":
            ph_text = "Natural language search (e.g., help me analyze financial PDF reports)..."
        else:
            ph_text = "Keywords match (Name, Description, Tags)..."
        with c_input:
            search_query = st.text_input(
                "Search", 
                placeholder=ph_text, 
                label_visibility="collapsed", 
                on_change=reset_page
            )

    st.write("")


    # ==========================================
    # Categories
    # ==========================================
    _, col_cat_main, _ = st.columns([2, 8, 2])

    with col_cat_main:
        try:
            selected_category = st.pills(
                "Category",
                CATEGORY_OPTIONS,
                default="All",
                selection_mode="single",
                label_visibility="collapsed",
                on_change=reset_page
            )
        except AttributeError:
            # Streamlit 版本较低时的降级方案
            selected_category = st.selectbox(
                "Category",
                CATEGORY_OPTIONS,
                index=0,
                label_visibility="collapsed",
                on_change=reset_page
            )

    st.divider()

    # ==========================================
    # 结果信息 + 排序（同一行）
    # ==========================================
    col_info, col_sort = st.columns([9, 1])

    with col_info:
        # 这里先占位，真实数据在 fetch 后展示
        info_placeholder = st.empty()

    with col_sort:
        # 自定义 Label 样式，使其与下方选项文字左对齐
        st.markdown(
            "<div style='font-size: 14px; color: #31333F; margin-bottom: -15px; padding-left: 12px; z-index: 100; position: relative; top: -10px;'>Sort by:</div>", 
            unsafe_allow_html=True
        )
        sort_option = st.selectbox(
            "Sort by:",
            ["Stars", "Recent"],
            index=0,
            label_visibility="collapsed",
            on_change=reset_page
        )


    # ==========================================
    # 5. 获取数据
    # ==========================================
    PAGE_SIZE = 24

    # df, total_count = fetch_skills(
    #     page=st.session_state.page,
    #     page_size=PAGE_SIZE,
    #     search_text=search_query,
    #     min_stars=0,
    #     category=selected_category,
    #     sort_option=sort_option
    # )
    df, total_count = fetch_skills(
        page=st.session_state.page,
        page_size=PAGE_SIZE,
        search_text=search_query,
        search_mode=search_mode,  # <--- 新增参数
        min_stars=0,
        category=selected_category,
        sort_option=sort_option
    )

    total_pages = math.ceil(total_count / PAGE_SIZE) if total_count > 0 else 1

    # 更新结果信息
    start_idx = (st.session_state.page - 1) * PAGE_SIZE + 1 if total_count > 0 else 0
    end_idx = start_idx + PAGE_SIZE - 1 if total_count > 0 else 0
    if end_idx > total_count: end_idx = total_count
    info_placeholder.markdown(
        f"<div style='color:#888;'>Showing {start_idx} - {end_idx} of {total_count} skills</div>",
        unsafe_allow_html=True
    )


    with st.expander("💡 Evaluation Metrics Interpretation", expanded=True):
        legend_html = """
        <style>
            .legend-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                padding: 10px 0;
            }
            .legend-item {
                display: flex;
                align-items: flex-start;
                background-color: #f9fafb; /* Gray-50 */
                border: 1px solid #e5e7eb; /* Gray-200 */
                border-radius: 8px;
                padding: 12px;
                transition: all 0.2s ease;
            }
            .legend-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                border-color: #d1d5db;
                background-color: #ffffff;
            }
            .legend-icon {
                font-size: 24px;
                margin-right: 12px;
                background: #fff;
                min-width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                border: 1px solid #f3f4f6;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }
            .legend-text h4 {
                margin: 0 0 4px 0;
                font-size: 14px;
                color: #111827; /* Gray-900 */
                font-weight: 600;
            }
            .legend-text p {
                margin: 0;
                font-size: 12px;
                color: #6b7280; /* Gray-500 */
                line-height: 1.4;
            }
            .status-dot {
                display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:4px;
            }
        </style>
        
        <div class="legend-grid">
            <div class="legend-item">
                <div class="legend-icon">🛡️</div>
                <div class="legend-text">
                    <h4>Safety (Safe)</h4>
                    <p>Ensures skill is free from malicious behavior, jailbreak risks, and security vulnerabilities.</p>
                </div>
            </div>    
            <div class="legend-item">
                <div class="legend-icon">🧩</div>
                <div class="legend-text">
                    <h4>Completeness (Compl.)</h4>
                    <p>Verifies if the skill covers all critical steps, explicitly defining prerequisites and execution conditions.</p>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">🚀</div>
                <div class="legend-text">
                    <h4>Executability (Exec.)</h4>
                    <p>Checks if the code runs successfully in a standard environment without throwing errors.</p>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">🛠️</div>
                <div class="legend-text">
                    <h4>Maintainability (Maint.)</h4>
                    <p>Assesses code structure, readability, and ease of customization or extension.</p>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">💰</div>
                <div class="legend-text">
                    <h4>Cost-Awareness (Cost)</h4>
                    <p>Quantifies execution overhead (latency, compute, API costs) for efficiency optimization.</p>
                </div>
            </div>
        </div>
        <div style="margin-top: 12px; padding-top:10px; border-top: 1px dashed #e5e7eb; font-size: 12px; color: #6b7280; display:flex; justify-content:flex-end; align-items:center; gap: 15px;">
            <span><strong>Rating Scale:</strong></span>
            <span><span class="status-dot" style="background:#22c55e;"></span>Good</span>
            <span><span class="status-dot" style="background:#eab308;"></span>Average</span>
            <span><span class="status-dot" style="background:#ef4444;"></span>Poor</span>
        </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)
    
    st.write("")


    # ==========================================
    # 3. 核心：网格卡片渲染
    # ==========================================
    if not df.empty:
        # 数据清洗
        if 'tags' in df.columns:
            df['tags'] = df['tags'].apply(lambda x: x if isinstance(x, list) else [])
        else:
            df['tags'] = [[] for _ in range(len(df))]
        
        if 'skill_date' in df.columns:
            df['skill_date'] = pd.to_datetime(df['skill_date'])

        # 定义网格列数 (例如 4 列)
        N_COLS = 4
        
        # 遍历数据行
        rows = [df.iloc[i:i+N_COLS] for i in range(0, len(df), N_COLS)]

        EVAL_CONFIG = {
            "safety": {"icon": "🛡️", "label": "Safe", "full": "Safety"},
            "completeness": {"icon": "🧩", "label": "Compl.", "full": "Completeness"},
            "executability": {"icon": "🚀", "label": "Exec.", "full": "Executability"},
            "maintainability": {"icon": "🛠️", "label": "Maint.", "full": "Maintainability"},
            "cost_awareness": {"icon": "💰", "label": "Cost", "full": "Cost-Awareness"}
        }

        # 定义等级颜色 (背景色, 文字色)
        LEVEL_STYLES = {
            "Good": ("#dcfce7", "#166534"),      # 绿色
            "Average": ("#fef9c3", "#854d0e"),   # 黄色
            "Poor": ("#fee2e2", "#991b1b"),       # 红色
            "Unknown": ("#f3f4f6", "#6b7280")    # 灰色
        }
        
        # for row_data in rows:
        #     cols = st.columns(N_COLS)
        #     for i, (_, row) in enumerate(row_data.iterrows()):
        #         with cols[i]:
        #             # 准备数据
        #             clean_name = html.escape(str(row.get('skill_name', 'Unknown')))
        #             clean_author = html.escape(str(row.get('author', 'Unknown')))
        #             clean_category = html.escape(str(row.get('category', 'Uncategorized')))
        #             raw_desc = str(row.get('skill_description', ''))
        #             if raw_desc == 'None' or not raw_desc or raw_desc == 'nan': raw_desc = "暂无描述"
        #             clean_desc = html.escape(raw_desc)

        #             # Evaluation 显示
        #             eval_data = row.get('evaluation', {})
        #             eval_html_items = ""
        #             if eval_data and isinstance(eval_data, dict):
        #                 for key, config in EVAL_CONFIG.items():
        #                     item = eval_data.get(key)
        #                     if item:
        #                         level = item.get('level', 'Unknown')                                
        #                         # 获取颜色样式，默认为灰色
        #                         bg_color, text_color = LEVEL_STYLES.get(level, LEVEL_STYLES['Unknown'])
                                
        #                         # 构造单个指标的徽章 (带 Tooltip)
        #                         eval_html_items += f"""
        #                         <span style="
        #                             display: inline-flex; align-items: center; gap: 2px;
        #                             background-color: {bg_color}; color: {text_color};
        #                             padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 500;
        #                             cursor: help; margin-right: 4px;" 
        #                             title="[{config['label']}: {level}] &#10;">
        #                             {config['icon']} {config['label']}
        #                         </span>
        #                         """
        #             # 如果没有评测数据，保持空白
        #             eval_section_html = f'<div style="margin-top:8px; margin-bottom:8px;">{eval_html_items}</div>' if eval_html_items else ""

        #             tags_html = ""
        #             if 'tags' in row and isinstance(row['tags'], list):
        #                 for tag in row['tags'][:4]:
        #                     tags_html += f'<span class="tag">{html.escape(str(tag).strip())}</span>'
        #             else:
        #                 tags_html = '<span class="tag">No Tags</span>'

        #             author_url = f"https://github.com/{clean_author}"
        #             # 安全获取日期，防止字段缺失导致 KeyError
        #             date_val = row.get('skill_date')
        #             date_str = str(date_val)[:10] if pd.notnull(date_val) else "Unknown Date"
        #             original_skill_url = row.get('skill_url', '#')
                    
        #             # 构造追踪链接：当前页面 + ?download_target=EncodedRealURL
        #             # 这样点击 Link 就会刷新当前页，触发顶部的 handle_redirects -> 计数 -> 跳转
        #             real_download_url = 'https://downgit.github.io/#/home?url=' + original_skill_url
        #             encoded_target = urllib.parse.quote(real_download_url)
        #             tracking_link = f"?download_target={encoded_target}"

        #             repo_url = row.get('repo_url', '#')
        #             skill_md_url = row.get('skill_md_url', original_skill_url)

                    
        #             # HTML 卡片结构
        #             card_html = f"""
        #             <div class="skill-card">
        #                 <div>
        #                     <div class="card-header" style="display:flex; justify-content:space-between; align-items:start;">
        #                         <a href="{original_skill_url}" target="_blank" class="skill-title" title="{clean_name}">{clean_name}</a>
        #                         <span class="star-badge">⭐ {row.get('stars', 0)}</span>
        #                     </div>
        #                     <div class="skill-desc">{clean_desc}</div>
        #                     <div style="margin-bottom:8px;">
        #                         <span class="tag" style="background-color:#e0f2fe; color:#0369a1;">{clean_category}</span>{tags_html}
        #                     </div>
        #                 </div>
        #                 <div class="skill-footer">
        #                     <div>👤 <a href="{author_url}" target="_blank" style="color:#666;">{clean_author}</a> </div>
        #                     <div>📅 {date_str} </div>
        #                     <a href="{tracking_link}" target="_blank" style="text-decoration:none; color:#2563eb; font-weight:bold;">Download ⬇️</a>
        #                 </div>
        #             </div>
        #             """
        #             st.markdown(card_html, unsafe_allow_html=True)
        for row_data in rows:
            cols = st.columns(N_COLS)
            for i, (_, row) in enumerate(row_data.iterrows()):
                with cols[i]:
                    # --- 1. 数据清洗 ---
                    clean_name = html.escape(str(row.get('skill_name', 'Unknown')))
                    clean_author = html.escape(str(row.get('author', 'Unknown')))
                    clean_category = html.escape(str(row.get('category', 'Uncategorized')))
                    
                    raw_desc = str(row.get('skill_description', ''))
                    if raw_desc in ['None', '', 'nan']: raw_desc = "Unknown"
                    clean_desc = html.escape(raw_desc)

                    # --- 2. Evaluation 逻辑 ---
                    raw_eval = row.get('evaluation', {})
                    # 容错处理：如果是 string 则解析，如果是 dict 则直接用
                    if isinstance(raw_eval, str):
                        try:
                            eval_data = json.loads(raw_eval)
                        except:
                            eval_data = {}
                    else:
                        eval_data = raw_eval if isinstance(raw_eval, dict) else {}

                    eval_html_items = ""
                    if eval_data:
                        for key, config in EVAL_CONFIG.items():
                            item = eval_data.get(key)
                            if item and isinstance(item, dict):
                                level = item.get('level', 'Unknown')
                                reason = html.escape(str(item.get('reason', '')))
                                bg_color, text_color = LEVEL_STYLES.get(level, LEVEL_STYLES['Unknown'])
                                
                                # 单行生成，避免内部缩进问题
                                eval_html_items += f"""<span style="display:inline-flex;align-items:center;gap:2px;background-color:{bg_color};color:{text_color};padding:2px 6px;border-radius:4px;font-size:11px;font-weight:500;cursor:help;margin-right:4px;" title="[{config['full']}: {level}] &#10;{reason}">{config['icon']} {config['label']}</span>"""

                    eval_section_html = f'<div style="margin-top:8px; margin-bottom:8px;">{eval_html_items}</div>' if eval_html_items else ""

                    # --- 3. Tags ---
                    tags_html = ""
                    if 'tags' in row and isinstance(row['tags'], list):
                        for tag in row['tags'][:4]:
                            tags_html += f'<span class="tag">{html.escape(str(tag).strip())}</span>'
                    else:
                        tags_html = '<span class="tag">No Tags</span>'

                    # --- 4. Links ---
                    author_url = f"https://github.com/{clean_author}"
                    date_val = row.get('skill_date')
                    date_str = str(date_val)[:10] if pd.notnull(date_val) else "Unknown Date"
                    original_skill_url = row.get('skill_url', '#')
                    
                    real_download_url = 'https://downgit.github.io/#/home?url=' + original_skill_url
                    encoded_target = urllib.parse.quote(real_download_url)
                    tracking_link = f"?download_target={encoded_target}"

                    # --- 5. HTML 生成 (关键修复) ---
                    # 使用 textwrap.dedent，这样你可以在代码里缩进，但 Streamlit 收到的是顶格的 HTML
                    # 这里的 indentation 不会报错，因为它是函数调用的一部分
                    if eval_section_html:
                        card_html = textwrap.dedent(f"""
                            <div class="skill-card">
                                <div style="flex: 1;">
                                    <div class="card-header" style="display:flex; justify-content:space-between; align-items:start;">
                                        <a href="{original_skill_url}" target="_blank" class="skill-title" title="{clean_name}">{clean_name}</a>
                                        <span class="star-badge">⭐ {row.get('stars', 0)}</span>
                                    </div>
                                    <div class="skill-desc">{clean_desc}</div>
                                    <div style="margin-bottom:8px;">
                                        <span class="tag" style="background-color:#e0f2fe; color:#0369a1;">{clean_category}</span>{tags_html}
                                    </div>
                                </div>
                                <div class="skill-eval-bar">
                                    {eval_section_html}
                                </div>
                                <div class="skill-footer">
                                    <div>👤 <a href="{author_url}" target="_blank" style="color:#666;">{clean_author}</a> </div>
                                    <div>📅 {date_str} </div>
                                    <a href="{tracking_link}" target="_blank" style="text-decoration:none; color:#2563eb; font-weight:bold;">Download ⬇️</a>
                                </div>
                            </div>
                        """)
                    else:
                        # 如果没有评测数据，保持原有结构但不插入 eval_section_html
                        card_html = textwrap.dedent(f"""
                            <div class="skill-card">
                                <div style="flex: 1;">
                                    <div class="card-header" style="display:flex; justify-content:space-between; align-items:start;">
                                        <a href="{original_skill_url}" target="_blank" class="skill-title" title="{clean_name}">{clean_name}</a>
                                        <span class="star-badge">⭐ {row.get('stars', 0)}</span>
                                    </div>
                                    <div class="skill-desc">{clean_desc}</div>
                                    <div style="margin-bottom:8px;">
                                        <span class="tag" style="background-color:#e0f2fe; color:#0369a1;">{clean_category}</span>{tags_html}
                                    </div>
                                </div>
                                <div class="skill-footer">
                                    <div>👤 <a href="{author_url}" target="_blank" style="color:#666;">{clean_author}</a> </div>
                                    <div>📅 {date_str} </div>
                                    <a href="{tracking_link}" target="_blank" style="text-decoration:none; color:#2563eb; font-weight:bold;">Download ⬇️</a>
                                </div>
                            </div>
                        """)
                    
                    st.markdown(card_html, unsafe_allow_html=True)

    else:
        st.info("No skills found matching your criteria.")
        st.write("")
        st.write("")
        st.write("")

    # ==========================================
    # 4. 底部：分页
    # ==========================================
    st.write("")
    
    if total_pages > 1:
        current_page = st.session_state.page
        
        # 简单的分页逻辑计算
        page_numbers = []
        if total_pages <= 7:
            page_numbers = list(range(1, total_pages + 1))
        else:
            if current_page <= 4:
                page_numbers = [1, 2, 3, 4, 5, "...", total_pages]
            elif current_page >= total_pages - 3:
                page_numbers = [1, "...", total_pages - 4, total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
            else:
                page_numbers = [1, "...", current_page - 1, current_page, current_page + 1, "...", total_pages]

        # 居中显示分页按钮
        # 使用空的左右列来挤压中间列
        _, mid_col, _ = st.columns([2, 8, 2]) 
        
        with mid_col:
            num_buttons = len(page_numbers) + 2
            btn_cols = st.columns(num_buttons, gap="small")
            
            # Prev
            with btn_cols[0]:
                if st.button("", icon=":material/chevron_left:", disabled=(current_page == 1), key="prev_btn", use_container_width=True):
                    change_page(current_page - 1)
                    st.rerun()
            
            # Pages
            for i, page_num in enumerate(page_numbers):
                with btn_cols[i + 1]:
                    if page_num == "...":
                        st.markdown("<div style='text-align:center; color:#888;'>...</div>", unsafe_allow_html=True)
                    else:
                        is_current = (page_num == current_page)
                        if st.button(f"{page_num}", key=f"page_{page_num}", type="primary" if is_current else "secondary", use_container_width=True):
                            change_page(page_num)
                            st.rerun()
            
            # Next
            with btn_cols[-1]:
                if st.button("", icon=":material/chevron_right:", disabled=(current_page == total_pages), key="next_btn", use_container_width=True):
                    change_page(current_page + 1)
                    st.rerun()
    
    # 5. 底部 Logo 区域
    # render_logos()


if __name__ == "__main__":
    main()
