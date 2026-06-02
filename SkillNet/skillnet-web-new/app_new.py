import streamlit as st
import streamlit.components.v1 as components
from utils import render_navbar, increment_visit, get_visit_count, get_download_count, render_logos
from icon_helper import icon
import pandas as pd
import html
import math
from supabase import create_client, Client


def render_html_embed(html_content, height):
    if hasattr(st, "iframe"):
        st.iframe(html_content, height=height)
    else:
        components.html(html_content, height=height, scrolling=False)


# --- 页面配置 ---
st.set_page_config(
    page_title="SkillNet - Create, Evaluate, and Connect AI Skills",
    page_icon="./images/skillnet_icon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# # --- 定义分类常量 ---
# CATEGORY_OPTIONS = [
#     "All", "Development", "AIGC", "Research", "Science", "Business", 
#     "Testing", "Productivity", "Security", "Lifestyle", "Benchmark", "Other"
# ]

# --- CSS 美化 ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }

    /* ---------------- Button Styles (Green Primary) ---------------- */
    div.stButton > button[kind="primary"] {
        background-color: #059669;
        border-color: #059669;
        color: white;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #047857;
        border-color: #047857;
        color: white;
    }
    div.stButton > button[kind="primary"]:focus {
        background-color: #059669;
        border-color: #059669;
        color: white;
        box-shadow: 0 0 0 0.2rem rgba(5, 150, 105, 0.5);
    }

    /* ---------------- Hero Section Styles ---------------- */
    .hero-container {
        text-align: center;
        padding: 20px 20px 10px 20px;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 15px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #6b7280;
        margin-bottom: 20px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* ---------------- Feature Section Styles ---------------- */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: transform 0.2s;
    }
    .feature-card:hover { transform: translateY(-2px); border-color: #d1d5db; }
    .feature-icon { font-size: 24px; margin-bottom: 10px; display: inline-block; padding: 10px; background: #f0fdf4; border-radius: 8px; color: #16a34a; }
    .feature-title { font-weight: 700; color: #111827; margin-bottom: 5px; font-size: 1.1rem; }
    .feature-desc { color: #6b7280; font-size: 0.9rem; line-height: 1.5; }
    
    /* ---------------- Marketplace Card Styles ---------------- */
    .skill-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
        height: 360px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .skill-card:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); border-color: #d1d5db; }
    .card-header { margin-bottom: 10px; border-bottom: 1px solid #e5e7eb; }
    .skill-title { font-size: 1.1em; font-weight: 700; color: #111827; text-decoration: none; display: block; margin-bottom: 4px; overflow-wrap: break-word; }
    .skill-title:hover { color: #2563eb; }
    .skill-desc { margin-top: 10px; font-size: 0.9em; color: #4b5563; line-height: 1.5; margin-bottom: 15px; flex-grow: 1; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 6; -webkit-box-orient: vertical; }
    .skill-footer { border-top: 1px solid #f3f4f6; padding-top: 12px; font-size: 0.8em; color: #6b7280; display: flex; justify-content: space-between; align-items: center; }
    .tag { margin-top: 10px; display: inline-block; background-color: #f3f4f6; border-radius: 9999px; padding: 2px 8px; font-size: 0.75em; margin-right: 4px; color: #374151; font-weight: 500; }
    .star-badge { background-color: #ecfccb; color: #3f6212; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 0.75em; }

    /* Search & Pagination */
    div[data-testid="stTextInput"] input { border-radius: 20px; padding-left: 20px; }
    div[data-testid="stHorizontalBlock"] { align-items: center; justify-content: center; }

</style>
""", unsafe_allow_html=True)

# --- 初始化 Supabase ---
@st.cache_resource
def init_connection():
    try:
        # Check if [supabase] section exists
        if "supabase" not in st.secrets:
            print("Secrets 'supabase' section not found in secrets.toml")
            return None
            
        url = st.secrets["supabase"]["SUPABASE_URL"]
        key = st.secrets["supabase"]["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        err_msg = str(e)
        if "socksio" in err_msg or "proxy" in err_msg:
             st.error("连接失败：缺少 SOCKS 代理支持。请在终端运行 `pip install \"httpx[socks]\"`。", icon="🚫")
        else:
             st.error(f"Supabase 连接错误: {e}")
        print(f"Supabase connection error: {e}")
        return None

supabase = init_connection()

# --- 数据加载函数 ---
def fetch_skills(page=1, page_size=20, search_text=None, min_stars=0, category=None, sort_option="Stars"):
    if not supabase:
        return pd.DataFrame(), 0
        
    start = (page - 1) * page_size
    end = start + page_size - 1

    try:
        query = supabase.table("skills").select("*", count="exact")
        if search_text:
            query = query.or_(f"skill_name.ilike.%{search_text}%,skill_description.ilike.%{search_text}%")
        if min_stars > 0:
            query = query.gte("stars", min_stars)
        if category and category != "All":
            query = query.eq("category", category)

        if sort_option == "Stars":
            query = query.order("stars", desc=True)
        else:
            query = query.order("skill_date", desc=True)
            
        response = query.range(start, end).execute()
        return pd.DataFrame(response.data), response.count

    except Exception as e:
        st.error(f"查询出错: {e}")
        return pd.DataFrame(), 0

def change_page(new_page):
    st.session_state.page = new_page


# ==================== VIEW: HOME ====================
def view_home():
    # 统计访问量
    increment_visit()
    total_visits = get_visit_count()
    total_downloads = get_download_count()
    

    # 悬浮的统计数据 (右上角，Github/Submit 下方)
    st.markdown(f"""
    <style>
        .floating-stats {{
            position: absolute;
            top: 0px; /* Navbar height is 70px */
            right: 0px; /* Aligned with navbar padding */
            background-color: transparent;
            color: #6b7280; /* Slightly darker for better visibility */
            font-size: 0.95rem; /* Larger font */
            z-index: 999;
            text-align: right;
            font-weight: 500;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
    </style>
    <div class="floating-stats">
        {icon("eye", 16, "#6b7280")} Visits: {total_visits:,} &nbsp;&nbsp; {icon("download", 16, "#6b7280")} Downloads: {total_downloads:,}
    </div>
    """, unsafe_allow_html=True)

    # 0. 获取 Skill 总数 (用于 Hero 区域展示)
    total_skills_count = 0
    if supabase:
        try:
            # 使用 limit(1) 替代 head=True，避免在某些代理环境下 HEAD 请求导致库崩溃
            # 同样能获取到 count 属性
            count_result = supabase.table("skills").select("id", count="exact").limit(1).execute()
            total_skills_count = count_result.count
        except Exception as e:
            print(f"Failed to get count: {e}")
            total_skills_count = 0
            
    # 如果没有 Supabase 或查询失败，使用 fetch_skills 的 Mock 数据计数
    if total_skills_count == 0:
        _, total_skills_count = fetch_skills()

    # # 1. Hero Section
    # # 使用组件来支持数字动画
    # hero_html = f"""
    # <!DOCTYPE html>
    # <html>
    # <head>
    # <style>
    #     body {{
    #         font-family: "Source Sans Pro", sans-serif;
    #         margin: 0;
    #         padding: 0;
    #         background-color: transparent;
    #         /* 防止内容溢出产生默认滚动条 */
    #         overflow: hidden; 
    #     }}
    #     .hero-container {{
    #         text-align: center;
    #         padding: 10px 20px;
    #     }}
    #     .hero-title {{
    #         font-size: 3.5rem;
    #         font-weight: 800;
    #         color: #111827;
    #         margin-bottom: 20px; 
    #         line-height: 1.2;
    #         margin-top: 0;
    #     }}
    #     .hero-subtitle {{
    #         font-size: 1.25rem;
    #         color: #6b7280;
    #         max-width: 900px;
    #         margin: 0 auto; /* 水平居中 */
    #         line-height: 1.6;
    #     }}
    #     .counter-badge {{
    #         color: #059669;
    #         font-weight: 700;
    #         background: #ecfdf5;
    #         padding: 4px 12px;
    #         border-radius: 99px;
    #         font-size: 0.9em;
    #         display: inline-block;
    #         margin-bottom: 20px; /* 使用 margin 代替 <br> 控制间距 */
    #     }}
    # </style>
    # </head>
    # <body>
    # <div class="hero-container">
    #     <div class="hero-title">Create, Evaluate, and Connect AI Skills</div>
        
    #     <div style="text-align: center;">
    #          <span class="counter-badge">
    #             📦 <span id="counter">0</span>+ Skills Available
    #          </span>
    #     </div>
        
    #     <div class="hero-subtitle">
    #         SkillNet is an open infrastructure for creating, evaluating, and organizing AI skills at scale.
    #     </div>
    # </div>
    
    # <script>
    #     const target = {total_skills_count};
    #     const duration = 2000; 
    #     const counter = document.getElementById('counter');
    #     const frameDuration = 1000 / 60;
    #     const totalFrames = Math.round(duration / frameDuration);
    #     const easeOutQuad = t => t * (2 - t);
        
    #     let frame = 0;
    #     const countTo = target;
        
    #     const animate = () => {{
    #         frame++;
    #         const progress = easeOutQuad(frame / totalFrames);
    #         const currentCount = Math.round(countTo * progress);
            
    #         if (counter) {{
    #             counter.innerText = currentCount.toLocaleString();
    #         }}
            
    #         if (frame < totalFrames) {{
    #             requestAnimationFrame(animate);
    #         }} else {{
    #             counter.innerText = countTo.toLocaleString();
    #         }}
    #     }};
    #     animate();
    # </script>
    # </body>
    # </html>
    # """

    hero_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{
                font-family: "Source Sans Pro", sans-serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
                overflow: hidden; 
            }}
            .hero-container {{
                text-align: center;
                padding: 10px 20px;
            }}
            .hero-title {{
                font-size: 3.5rem;
                font-weight: 800;
                color: #111827;
                margin-bottom: 20px; 
                line-height: 1.2;
                margin-top: 0;
            }}
            .hero-subtitle {{
                font-size: 1.25rem;
                color: #6b7280;
                max-width: 900px;
                margin: 0 auto; 
                line-height: 1.6;
            }}
            
            /* Badge 样式优化 */
            .counter-badge {{
                color: #047857; /* 稍微加深一点主色，增加对比度 */
                background: #ecfdf5;
                padding: 6px 16px; /* 稍微增加一点内边距 */
                border-radius: 99px;
                font-size: 0.95em;
                display: inline-flex; /* 使用 flex 布局让内部元素垂直居中 */
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                border: 1px solid #d1fae5; /* 增加一个极淡的边框增加精致感 */
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* 增加轻微立体感 */
            }}
            
            /* 辅助文字样式 */
            .badge-secondary {{
                font-weight: 500;
                opacity: 0.65; /* 降低透明度，作为次要信息 */
                font-size: 1em;
                margin-left: 8px;
            }}
            
            .badge-divider {{
                margin: 0 8px;
                color: #a7f3d0; /* 浅绿色分隔符 */
                font-weight: 300;
            }}
        </style>
        </head>
        <body>
        <div class="hero-container">
            <div class="hero-title">Create, Evaluate, and Connect AI Skills</div>
            
            <div style="text-align: center;">
                <span class="counter-badge">
                    <span style="margin-right: 6px;">{icon("sparkles", 20, "#f59e0b")}</span>

                    <span class="badge-secondary">
                        600,000+ Total
                    </span>
                    
                    <span class="badge-divider">|</span>
                    
                    <span style="font-weight: 800; font-size: 1.05em;">
                        <span id="counter">0</span>+ Curated
                    </span>
                    
                </span>
            </div>
            
            <div class="hero-subtitle">
                SkillNet is an open infrastructure for creating, evaluating, and organizing AI skills at scale.
            </div>
        </div>
        
        <script>
            const target = {total_skills_count}; /* 变量名替换为实际传入的变量 */
            const duration = 2000; 
            const counter = document.getElementById('counter');
            const frameDuration = 1000 / 60;
            const totalFrames = Math.round(duration / frameDuration);
            const easeOutQuad = t => t * (2 - t);
            
            let frame = 0;
            const countTo = target;
            
            const animate = () => {{
                frame++;
                const progress = easeOutQuad(frame / totalFrames);
                const currentCount = Math.round(countTo * progress);
                
                if (counter) {{
                    counter.innerText = currentCount.toLocaleString();
                }}
                
                if (frame < totalFrames) {{
                    requestAnimationFrame(animate);
                }} else {{
                    counter.innerText = countTo.toLocaleString();
                }}
            }};
            animate();
        </script>
        </body>
        </html>
    """

    render_html_embed(hero_html, height=190)

    # Buttons
    col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 1, 1])
    with col_btn_2:
        sub_col1, sub_col2 = st.columns([1.08, 1])
        with sub_col1:
            # 修改为直接跳转到 resources 页面，保持体验一致
            # st.switch_page 会在被触发时直接中断后续渲染，不需要放到 if 语句中显式打印返回值
            if st.button("Explore Skills →", type="primary", use_container_width=True):
                st.switch_page("pages/resources.py")
        with sub_col2:
            if st.button("Go to Demo", use_container_width=True):
                st.switch_page("pages/science.py")

    # 2. Functionality Visual Section - Split Layout
    # Left: Multi-dimensional Graph
    # Right: Code Demo
    
    # Use 4 columns to center content with equal margins
    # Left Spacer | Graph | Code | Right Spacer
    _, main_col1, main_col2, _ = st.columns([0.4, 2.6, 1.2, 0.4])

    with main_col1:
        # --- 替换方案：使用 HTML5 Canvas 实现动态粒子网络 ---
        import json
        
        # 传递数据给前端
        categories = [
           "Development", "AIGC", "Research", "Science",  
           "Business", "Testing", "Productivity", "Security", 
           "Lifestyle", "..."
        ]
        dimensions = [
            "Safety", "Completeness", "Executability", "Maintainability", "Cost-Awareness"
        ]
        
        # 将数据转换为 JSON 字符串以便嵌入 JS
        cats_json = json.dumps(categories)
        dims_json = json.dumps(dimensions)
        
        # 使用普通字符串取代 f-string，避免花括号冲突
        canvas_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body { margin: 0; overflow: hidden; background-color: transparent; font-family: "Source Sans Pro", sans-serif; }
            canvas { display: block; position: absolute; top: 0; left: 0; z-index: 0; }
            #label-container {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none; /* Let clicks pass through to canvas if needed */
                z-index: 10;
            }
            .chart-label {
                position: absolute;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                font-size: 15px;
                font-weight: 500;
                color: #4b5563;
                white-space: nowrap;
                pointer-events: auto; /* Allow selection */
                transform: translateY(-50%); /* Center vertically relative to y */
                line-height: 1;
            }
            .chart-header {
                position: absolute;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                font-size: 20px;
                font-weight: 500;
                color: #9ca3af;
                white-space: nowrap;
                pointer-events: auto; /* Allow selection */
                transform: translateY(-50%);
                line-height: 1;
            }
        </style>
        </head>
        <body>
        <canvas id="networkCanvas"></canvas>
        <div id="label-container"></div>
        <script>
            const canvas = document.getElementById('networkCanvas');
            const ctx = canvas.getContext('2d');
            const container = document.getElementById('label-container');
            
            // 数据注入
            const categories = {cats_json};
            const dimensions = {dims_json};
            
            const PARTICLE_COUNT = 80; 
            const CONNECT_DISTANCE = 110;
            const HUB_CONNECT_DISTANCE = 250; // Hub 节点吸引力更强
            
            let width, height;
            let particles = [];
            let leftHub, rightHub; // 显式引用 Hub 节点
            
            class Particle {
                constructor(isLabel = false, x = 0, y = 0, label = "", align = "left", color = null, isHub = false) {
                    this.isLabel = isLabel;
                    this.isHub = isHub;
                    this.label = label;
                    this.align = align;
                    
                    // 初始位置
                    this.x = x;
                    this.y = y;
                    
                    if (isLabel || isHub) {
                        // 静态节点 (Label 或 Hub)
                        this.size = isHub ? 4.5 : 3.5; // Hub 稍微大一点，但不过分
                        this.color = color;
                        this.vx = 0;
                        this.vy = 0;
                        
                        // Create text element for labels
                        if (isLabel) {
                            const el = document.createElement('div');
                            el.className = 'chart-label';
                            el.innerText = label;
                            el.style.top = y + 'px';
                            
                            const offsetX = 16;
                            if (align === "left") {
                                // Text on left, dot on right
                                // width - (x - offsetX)
                                // x is at 25%, text ends at x - 16
                                el.style.right = (width - (x - offsetX)) + 'px';
                                el.style.textAlign = 'right'; // Ensure text rendering aligns right internally if wrapped (won't wrap here)
                            } else {
                                // Text on right, dot on left
                                el.style.left = (x + offsetX) + 'px';
                                el.style.textAlign = 'left';
                            }
                            container.appendChild(el);
                        }
                    } else {
                        // 云团自由粒子 (覆盖传入的 x,y)
                        const centerX = width / 2;
                        const centerY = height / 2;
                        const maxR = height * 0.35; 
                        
                        const r = Math.sqrt(Math.random()) * maxR; 
                        const theta = Math.random() * Math.PI * 2;
                        
                        this.x = centerX + Math.cos(theta) * r;
                        this.y = centerY + Math.sin(theta) * r;
                        
                        this.vx = (Math.random() - 0.5) * 0.6;
                        this.vy = (Math.random() - 0.5) * 0.6;
                        this.size = Math.random() * 2 + 1;
                        this.color = (Math.random() > 0.6) ? 'rgba(16, 185, 129, ' : 'rgba(156, 163, 175, ';
                    }
                }
                
                update() {
                    if (this.isLabel || this.isHub) return; // 静态不动
                    
                    // 自由粒子运动
                    this.x += this.vx;
                    this.y += this.vy;
                    
                    // 限制在中心圆区域内
                    const centerX = width / 2;
                    const centerY = height / 2;
                    const maxR = height * 0.38;
                    const dx = this.x - centerX;
                    const dy = this.y - centerY;
                    
                    if (Math.sqrt(dx*dx + dy*dy) > maxR) {
                        if (dx * this.vx + dy * this.vy > 0) {
                            this.vx *= -1;
                            this.vy *= -1;
                        }
                    }
                }
                
                draw() {
                    // 1. 绘制圆点
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.fillStyle = this.color + '0.9)'; 
                    ctx.fill();
                    // Text is now handled by DOM
                }
            }
            
            function init() {
                // 1. 获取 CSS 逻辑宽高
                width = window.innerWidth;
                height = window.innerHeight;
                
                // 2. 处理高分屏 (Retina) 清晰度问题
                const dpr = window.devicePixelRatio || 1;
                
                // Canvas 内部物理像素放大
                canvas.width = width * dpr;
                canvas.height = height * dpr;
                
                // Canvas 显示尺寸保持不变
                canvas.style.width = width + "px";
                canvas.style.height = height + "px";
                
                // 3. 缩放绘图上下文，让后续坐标操作自动适配
                ctx.scale(dpr, dpr);
                
                particles = [];
                container.innerHTML = ''; // Clear DOM elements
                
                // --- 创建 Headers (DOM) ---
                const headerY = 25;
                
                // Header: Category (Left)
                const catHeader = document.createElement('div');
                catHeader.className = 'chart-header';
                catHeader.innerText = 'Category';
                catHeader.style.top = headerY + 'px';
                // Align right to leftX - 16
                // leftX is width * 0.25
                const leftHeaderBound = width * 0.18;
                catHeader.style.right = (width - leftHeaderBound) + 'px';
                container.appendChild(catHeader);
                
                // Header: Evaluation (Right)
                const evalHeader = document.createElement('div');
                evalHeader.className = 'chart-header';
                evalHeader.innerText = 'Evaluation';
                evalHeader.style.top = headerY + 'px';
                // Align left to rightX + 16
                // rightX is width * 0.75
                const rightHeaderBound = width * 0.82;
                evalHeader.style.left = rightHeaderBound + 'px';
                container.appendChild(evalHeader);
                
                // 1. 创建 Hub 节点 (位于 Label 和 Center 之间)
                // Left Hub: Gray (Shifted Right to 35%)
                leftHub = new Particle(false, width * 0.25, height * 0.5, "", "", 'rgba(156, 163, 175, ', true);
                particles.push(leftHub);
                
                // Right Hub: Green (Shifted Left to 65%)
                rightHub = new Particle(false, width * 0.75, height * 0.5, "", "", 'rgba(16, 185, 129, ', true);
                particles.push(rightHub);
                
                // 2. 左侧 Label List
                // Shifted Right to 25% (gives more space for text "Tools & Integration")
                const leftX = width * 0.18; 
                const leftStart = height * 0.15;
                const leftEnd = height * 0.85;
                const leftStep = (leftEnd - leftStart) / (categories.length - 1 || 1);
                
                categories.forEach((cat, i) => {
                    particles.push(new Particle(true, leftX, leftStart + i * leftStep, cat, "left", 'rgba(156, 163, 175, '));
                });
                
                // 3. 右侧 Label List
                // Shifted Left to 75%
                const rightX = width * 0.82;
                const rightStart = height * 0.3; 
                const rightEnd = height * 0.7;
                const rightStep = (rightEnd - rightStart) / (dimensions.length - 1 || 1);
                
                dimensions.forEach((dim, i) => {
                    particles.push(new Particle(true, rightX, rightStart + i * rightStep, dim, "right", 'rgba(16, 185, 129, '));
                });
                
                // 4. 中间云团
                for(let i=0; i < PARTICLE_COUNT; i++) {
                    particles.push(new Particle());
                }
            }
            
            function animate() {
                ctx.clearRect(0, 0, width, height);
                // Headers now handled by static DOM in init()

                for (let i = 0; i < particles.length; i++) {
                    let p = particles[i];
                    p.update();
                    p.draw();
                    
                    // --- 连线逻辑 A: Label -> Hub 强制连线 ---
                    if (p.isLabel) {
                        if (p.align === "left" && leftHub) {
                            ctx.beginPath();
                            ctx.strokeStyle = 'rgba(156, 163, 175, 0.2)'; // 浅灰色长线
                            ctx.lineWidth = 1;
                            ctx.moveTo(p.x, p.y);
                            ctx.lineTo(leftHub.x, leftHub.y);
                            ctx.stroke();
                        }
                        if (p.align === "right" && rightHub) {
                            ctx.beginPath();
                            ctx.strokeStyle = 'rgba(16, 185, 129, 0.2)'; // 浅绿色长线
                            ctx.lineWidth = 1;
                            ctx.moveTo(p.x, p.y);
                            ctx.lineTo(rightHub.x, rightHub.y);
                            ctx.stroke();
                        }
                        // 标签点不参与其他自由连线，保持整洁
                        continue;
                    }
                    
                    // --- 连线逻辑 B: Cloud 内部 & Hub -> Cloud ---
                    // 不再跳过 Hub，让 Hub 也能作为起点去连接 Cloud
                    
                    for (let j = i + 1; j < particles.length; j++) {
                        let p2 = particles[j];
                        if (p2.isLabel) continue; // 不连标签
                        if (p.isHub && p2.isHub) continue; // Hub 之间不连
                        
                        let dx = p.x - p2.x;
                        let dy = p.y - p2.y;
                        let dist = Math.sqrt(dx*dx + dy*dy);
                        
                        // 判定距离阈值
                        let limit = CONNECT_DISTANCE;
                        if (p.isHub || p2.isHub) limit = HUB_CONNECT_DISTANCE; // Hub 的吸引半径更大
                        
                        if (dist < limit) {
                            let opacity = 1 - (dist / limit);
                            opacity = opacity * 0.4;
                            
                            ctx.beginPath();
                            // 如果连接的是 Hub，颜色跟随 Hub
                            if (p === leftHub || p2 === leftHub) ctx.strokeStyle = `rgba(156, 163, 175, ${opacity})`;
                            else if (p === rightHub || p2 === rightHub) ctx.strokeStyle = `rgba(16, 185, 129, ${opacity})`;
                            else ctx.strokeStyle = `rgba(200, 200, 200, ${opacity})`;
                            
                            ctx.lineWidth = 1;
                            ctx.moveTo(p.x, p.y);
                            ctx.lineTo(p2.x, p2.y);
                            ctx.stroke();
                        }
                    }
                }
                requestAnimationFrame(animate);
            }
            
            window.addEventListener('resize', init);
            init();
            animate();
        </script>
        </body>
        </html>
        """
        
        # 替换占位符
        canvas_html = canvas_html.replace('{cats_json}', cats_json).replace('{dims_json}', dims_json)
        
        # 嵌入，增加高度使其更舒展
        render_html_embed(canvas_html, height=540)


    with main_col2:
        # Code Demo 部分保持不变
        # 使用负 margin 向上提，与左侧 Canvas 标题 (Y=25px) 对齐
        st.markdown(f"<h5 style='margin-top: 0px; margin-bottom: 0px; font-weight: 600; font-size: 1.25rem;'>{icon('package', 22, '#7c3aed')} Using SkillNet</h5>", unsafe_allow_html=True)
        
        # 增加代码块内部的空行，使其在视觉上更高，与左侧图谱平衡
        # 增加代码块内部的空行，使其在视觉上更高，与左侧图谱平衡
#         st.code("""
# # Install the library
# pip install skillnet-ai

# # Use a skill in your agent
# from skillnet-ai import SkillNetClient

# # Verified for Safety & Executability
# skill = SkillNetClient.search("google")
# SkillNetClient.evaluate(skill)
# SkillNetClient.install(skill)

# skill = SkillNetClient.create(trajectory)

# agent.use(skill)
#         """, language="python")

        tab1, tab2 = st.tabs(["CLI", "Python"])

        # Tab 1: Bash 内容
        with tab1:
            st.code("""
# Install
pip install skillnet-ai

# Search & Download skill
skillnet search "bioinformatics pipeline"
skillnet download https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills/biopython

# Create new skill
skillnet create ./logs/chat.txt --model gpt-5

# Evaluate skill quality
skillnet evaluate ./my_skills/biopython

# Analyze skill relations
skillnet analyze ./my_skills


    """, language="bash")

        # Tab 2: Python SDK 内容
        with tab2:
            st.code("""
# Initialize
from skillnet_ai import SkillNetClient
client = SkillNetClient()

# Search & Download skill
skills = client.search("bioinformatics pipeline")
client.download(skills[0].skill_url, target_dir="./my_skills")

# Create new skill
client.create(trajectory_log, output_dir="./my_skills")

# Evaluate skill quality
client.evaluate("./my_skills/biopython")

# Analyze skill relations
client.analyze("./my_skills")

    """, language="python")

    st.write("")

    # --- 优化版：紧凑型一行导航 ---
    st.markdown("---")
    st.markdown("<h5 style='text-align: center; color: #111827; margin-top: 0px; margin-bottom: 20px; font-family: sans-serif;'>Explore Our Platform</h3>", unsafe_allow_html=True)
    
    # 定义导航数据
    sections = [
        {"icon": icon("grid-3x3", 22, "#059669"), "title": "Ontology", "url": "/ontology", "desc": "Defined Skill Ontology for SkillNet."},
        {"icon": icon("database", 22, "#2563eb"), "title": "Resource", "url": "/resources", "desc": "Curated Skill Repository."},
        {"icon": icon("package", 22, "#7c3aed"), "title": "Collection", "url": "/package", "desc": "Bundled Skill Collections."},
        {"icon": icon("flask-conical", 22, "#e11d48"), "title": "Science", "url": "/science", "desc": "Autonomous Scientific Discovery."},
        {"icon": icon("terminal", 22, "#d97706"), "title": "Coding", "url": "/coding", "desc": "Autonomous Coding Agent."},
        {"icon": icon("book-open", 22, "#0891b2"), "title": "Docs", "url": "/docs", "desc": "Developer Guides."}
    ]

    # 创建 6 列布局
    cols = st.columns(6)

    for i, item in enumerate(sections):
        with cols[i]:
            st.markdown(f"""
                <a href="{item['url']}" target="_self" style="text-decoration: none;">
                    <div style="
                        text-align: center; 
                        padding: 10px 8px; 
                        border-radius: 10px; 
                        border: 1px solid #f3f4f6; 
                        background-color: white;
                        transition: all 0.2s ease;
                        cursor: pointer;
                    " onmouseover="this.style.borderColor='#10b981'; this.style.backgroundColor='#f0fdf4';" 
                       onmouseout="this.style.borderColor='#f3f4f6'; this.style.backgroundColor='white';">
                        <div style="font-size: 1.5rem; margin-bottom: 4px;">{item['icon']}</div>
                        <div style="font-weight: 600; color: #111827; font-size: 0.9rem; margin-bottom: 2px;">{item['title']}</div>
                        <div style="font-size: 0.75rem; color: #9ca3af; line-height: 1.2;">{item['desc']}</div>
                    </div>
                </a>
            """, unsafe_allow_html=True)

    st.write("") # 留白

    # 使用 HTML/CSS 自定义精美页脚
    st.markdown(f"""
        <style>
            .footer-container {{
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #f3f4f6;
                text-align: center;
                color: #6b7280;
                font-family: "Source Sans Pro", sans-serif;
            }}
            .footer-main {{
                font-size: 0.95rem;
                margin-bottom: 8px;
            }}
            .footer-heart {{
                font-size: 0.9rem;
                font-weight: 500;
                color: #4b5563;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
            }}
            .heart-icon {{
                color: #ef4444;
            }}
        </style>

        <div class="footer-container">
            <div class="footer-main">
                {icon("sparkles", 16, "#f59e0b")} SkillNet builds on open, in-house, and community skills.
            </div>
            <div class="footer-heart">
                <span>Thanks to Anthropic, Alibaba Group, Tencent, and OpenJiuwen.</span>
                <span class="heart-icon">{icon("heart", 16, "#ef4444")}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# # ==================== VIEW: MARKETPLACE ====================
# def view_marketplace():
#     if 'page' not in st.session_state:
#         st.session_state.page = 1

#     # Header
#     st.markdown("<h1 style='text-align: center; margin-bottom: 0; font-size: 48px;'>Create, Evaluate, and Connect AI Skills</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; color: #666; font-size: 20px;'>SkillNet is an open infrastructure for creating, evaluating, and organizing AI skills at scale.</p>", unsafe_allow_html=True)
#     st.button("← Back to Home", on_click=lambda: st.session_state.update({'current_view': 'home'}))
    
#     st.write("") 

#     # Search
#     col_spacer_l, col_search, col_spacer_r = st.columns([1, 2, 1])
#     with col_search:
#         def reset_page(): st.session_state.page = 1
#         search_query = st.text_input("Search skills...", placeholder="Search skills name, description...", label_visibility="collapsed", on_change=reset_page)

#     st.write("")

#     # Categories
#     _, col_cat_main, _ = st.columns([0.4, 10, 0.4])
#     with col_cat_main:
#         try:
#             selected_category = st.pills("Category", CATEGORY_OPTIONS, default="All", selection_mode="single", label_visibility="collapsed", on_change=reset_page)
#         except AttributeError:
#             selected_category = st.selectbox("Category", CATEGORY_OPTIONS, label_visibility="collapsed", on_change=reset_page)

#     st.divider()

#     # Sort & Info
#     col_info, col_sort = st.columns([9, 1])
#     with col_info:
#         info_placeholder = st.empty()
#     with col_sort:
#         st.markdown(
#             "<div style='font-size: 14px; color: #31333F; margin-bottom: -15px; padding-left: 12px; z-index: 100; position: relative; top: -5px;'>Sort by:</div>", 
#             unsafe_allow_html=True
#         )
#         sort_option = st.selectbox("Sort by:", ["Stars", "Recent"], index=0, label_visibility="collapsed", on_change=reset_page)

#     # Fetch Data
#     PAGE_SIZE = 24
#     df, total_count = fetch_skills(
#         page=st.session_state.page,
#         page_size=PAGE_SIZE,
#         search_text=search_query,
#         min_stars=0,
#         category=selected_category,
#         sort_option=sort_option
#     )
#     total_pages = math.ceil(total_count / PAGE_SIZE) if total_count > 0 else 1

#     start_idx = (st.session_state.page - 1) * PAGE_SIZE + 1 if total_count > 0 else 0
#     end_idx = start_idx + PAGE_SIZE - 1 if total_count > 0 else 0
#     if end_idx > total_count: end_idx = total_count
#     info_placeholder.markdown(f"<div style='color:#888;'>Showing {start_idx} - {end_idx} of {total_count} skills</div>", unsafe_allow_html=True)

#     # Grid Render
#     if not df.empty:
#         if 'tags' in df.columns:
#             df['tags'] = df['tags'].apply(lambda x: x if isinstance(x, list) else [])
#         else:
#             df['tags'] = [[] for _ in range(len(df))]
        
#         N_COLS = 4
#         rows = [df.iloc[i:i+N_COLS] for i in range(0, len(df), N_COLS)]
        
#         for row_data in rows:
#             cols = st.columns(N_COLS)
#             for i, (_, row) in enumerate(row_data.iterrows()):
#                 with cols[i]:
#                     clean_name = html.escape(str(row.get('skill_name', 'Unknown')))
#                     clean_author = html.escape(str(row.get('author', 'Unknown')))
#                     clean_category = html.escape(str(row.get('category', 'Uncategorized')))
#                     raw_desc = str(row.get('skill_description', ''))
#                     if raw_desc in ['None', 'nan', '']: raw_desc = "暂无描述"
#                     clean_desc = html.escape(raw_desc)

#                     tags_html = "".join([f'<span class="tag">{html.escape(str(t).strip())}</span>' for t in row['tags'][:4]]) if row['tags'] else '<span class="tag">No Tags</span>'

#                     author_url = f"https://github.com/{clean_author}"
#                     original_skill_url = row.get('skill_url', '#')
#                     skill_download_url = 'https://downgit.github.io/#/home?url=' + original_skill_url
                    
#                     date_val = row.get('skill_date')
#                     date_str = str(date_val)[:10] if pd.notnull(date_val) else "Unknown"

#                     card_html = f"""
#                     <div class="skill-card">
#                         <div>
#                             <div class="card-header" style="display:flex; justify-content:space-between; align-items:start;">
#                                 <a href="{original_skill_url}" target="_blank" class="skill-title" title="{clean_name}">{clean_name}</a>
#                                 <span class="star-badge">⭐ {row.get('stars', 0)}</span>
#                             </div>
#                             <div class="skill-desc">{clean_desc}</div>
#                             <div style="margin-bottom:8px;">
#                                 <span class="tag" style="background-color:#e0f2fe; color:#0369a1;">{clean_category}</span>{tags_html}
#                             </div>
#                         </div>
#                         <div class="skill-footer">
#                             <div>👤 <a href="{author_url}" target="_blank" style="color:#666;">{clean_author}</a> </div>
#                             <div>📅 {date_str} </div>
#                             <a href="{skill_download_url}" target="_blank" style="text-decoration:none; color:#2563eb; font-weight:bold;">Download ⬇️</a>
#                         </div>
#                     </div>
#                     """
#                     st.markdown(card_html, unsafe_allow_html=True)
#     else:
#         st.info("No skills found.")

#     # Pagination
#     st.write("")
#     if total_pages > 1:
#         current_page = st.session_state.page
#         page_numbers = []
#         if total_pages <= 7:
#             page_numbers = list(range(1, total_pages + 1))
#         else:
#             if current_page <= 4:
#                 page_numbers = [1, 2, 3, 4, 5, "...", total_pages]
#             elif current_page >= total_pages - 3:
#                 page_numbers = [1, "...", total_pages - 4, total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
#             else:
#                 page_numbers = [1, "...", current_page - 1, current_page, current_page + 1, "...", total_pages]

#         _, mid_col, _ = st.columns([2, 6, 2]) 
#         with mid_col:
#             num_buttons = len(page_numbers) + 2
#             btn_cols = st.columns(num_buttons, gap="small")
            
#             with btn_cols[0]:
#                 if st.button("<", disabled=(current_page == 1), key="prev_btn", use_container_width=True):
#                     change_page(current_page - 1)
#                     st.rerun()
            
#             for i, page_num in enumerate(page_numbers):
#                 with btn_cols[i + 1]:
#                     if page_num == "...":
#                         st.markdown("<div style='text-align:center; color:#888;'>...</div>", unsafe_allow_html=True)
#                     else:
#                         is_current = (page_num == current_page)
#                         if st.button(f"{page_num}", key=f"page_{page_num}", type="primary" if is_current else "secondary", use_container_width=True):
#                             change_page(page_num)
#                             st.rerun()
            
#             with btn_cols[-1]:
#                 if st.button(">", disabled=(current_page == total_pages), key="next_btn", use_container_width=True):
#                     change_page(current_page + 1)
#                     st.rerun()
                    

# ==================== MAIN ====================
def main():
    render_navbar(active_page="/")

    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'home'
        
    if st.session_state.current_view == 'home':
        view_home()
    # else:
    #     view_marketplace()

    # render_logos()

if __name__ == "__main__":
    main()
