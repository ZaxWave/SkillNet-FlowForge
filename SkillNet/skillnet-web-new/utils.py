import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime
import base64
from pathlib import Path
import requests
from retry import retry

# ==================== STATS UTILS ====================

# --- Supabase 统计客户端（复用前端已有的 secrets 配置） ---
@st.cache_resource
def _get_stats_client():
    """获取用于统计的 Supabase 客户端"""
    try:
        from supabase import create_client
        if "supabase" not in st.secrets:
            return None
        url = st.secrets["supabase"]["SUPABASE_URL"]
        key = st.secrets["supabase"]["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        print(f"[Stats] Supabase client init failed: {e}")
        return None

# --- Fallback: 文件存储（Supabase 不可用时降级使用） ---
STATS_FILE = "site_stats.json"

def _load_stats_file():
    if not os.path.exists(STATS_FILE):
        return {"visits": 0, "downloads": 0, "last_updated": str(datetime.now())}
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"visits": 0, "downloads": 0}

def _save_stats_file(stats):
    stats["last_updated"] = str(datetime.now())
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

# --- 公开接口（签名完全不变，对外透明） ---

def increment_visit():
    """使用 session_state 防止同一次会话重复计数"""
    if "visit_counted" not in st.session_state:
        client = _get_stats_client()
        if client:
            try:
                client.rpc("increment_stat_visits", {"amount": 1}).execute()
            except Exception as e:
                print(f"[Stats] increment_visit RPC failed, fallback to file: {e}")
                stats = _load_stats_file()
                stats["visits"] = stats.get("visits", 0) + 1
                _save_stats_file(stats)
        else:
            stats = _load_stats_file()
            stats["visits"] = stats.get("visits", 0) + 1
            _save_stats_file(stats)
        st.session_state.visit_counted = True

def increment_download(count=1):
    client = _get_stats_client()
    if client:
        try:
            client.rpc("increment_stat_downloads", {"amount": count}).execute()
        except Exception as e:
            print(f"[Stats] increment_download RPC failed, fallback to file: {e}")
            stats = _load_stats_file()
            stats["downloads"] = stats.get("downloads", 0) + count
            _save_stats_file(stats)
    else:
        stats = _load_stats_file()
        stats["downloads"] = stats.get("downloads", 0) + count
        _save_stats_file(stats)

@st.cache_data(ttl=60)
def _fetch_total_stats():
    """从 Supabase 获取合计统计，缓存 60 秒"""
    client = _get_stats_client()
    if client:
        try:
            result = client.rpc("get_total_stats").execute()
            if result.data and len(result.data) > 0:
                row = result.data[0]
                return {
                    "visits": row.get("total_visits", 0),
                    "downloads": row.get("total_downloads", 0)
                }
        except Exception as e:
            print(f"[Stats] get_total_stats RPC failed, fallback to file: {e}")
    return None

def get_visit_count():
    stats = _fetch_total_stats()
    if stats is not None:
        return stats["visits"]
    return _load_stats_file().get("visits", 0)

def get_download_count():
    stats = _fetch_total_stats()
    if stats is not None:
        return stats["downloads"]
    return _load_stats_file().get("downloads", 0)

def handle_redirects():
    """检测 URL 参数并处理统计跳转"""
    if "download_target" in st.query_params:
        target = st.query_params["download_target"]

        # 记录下载
        increment_download()

        # 执行跳转 (HTML Meta Refresh 最稳定)
        st.markdown(f'<meta http-equiv="refresh" content="0;url={target}">', unsafe_allow_html=True)
        st.write("Redirecting context...")
        st.stop()


# ==================== UI UTILS ====================

# --- 自定义导航栏 ---
# def render_navbar():
#     st.markdown("""
#     <style>
#         /* 1. 隐藏 Streamlit 默认顶部 Header */
#         header[data-testid="stHeader"] {
#             display: none;
#         }

#         /* 2. 关键调整：强制减少 Streamlit 主容器的顶部空白
#            原本它是 6rem (约96px)，我们改成 0 或者很小的值，
#            完全由下面的占位符 div 来控制起始位置
#         */
#         div[data-testid="block-container"] {
#             padding-top: 20px !important; /* 只留一点点边距 */
#         }

#         /* 3. 自定义导航栏样式 (保持不变) */
#         .custom-navbar {
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 70px;
#             background-color: #ffffff;
#             border-bottom: 1px solid #e5e7eb;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding: 0 40px;
#             z-index: 99999;
#             font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
#         }

#         .nav-left {
#             display: flex; align-items: center; font-size: 20px; font-weight: 700; color: #111827; text-decoration: none; gap: 10px;
#         }
#         .nav-center {
#             display: flex; gap: 30px; display: none;
#         }
#         @media (min-width: 768px) { .nav-center { display: flex; } }

#         .nav-link { color: #6b7280; text-decoration: none; font-size: 15px; font-weight: 500; transition: color 0.2s; }
#         .nav-link:hover { color: #111827; }

#         .nav-right { display: flex; align-items: center; gap: 15px; }
#         .btn-text { color: #374151; text-decoration: none; font-size: 15px; font-weight: 500; }
#         .btn-text:hover { color: #111827; }
#         .btn-primary { background-color: #111827; color: white !important; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 600; transition: opacity 0.2s; }
#         .btn-primary:hover { opacity: 0.9; }
#         .custom-navbar a { text-decoration: none !important; }
#     </style>

#     <nav class="custom-navbar">
#         <a href="/" target="_self" class="nav-left">
#             <span>🕸️ SkillNet</span>
#         </a>
#         <div class="nav-center">
#             <a href="/" target="_self" class="nav-link">Home</a>
#             <a href="docs" target="_self" class="nav-link">Docs</a>
#         </div>
#         <div class="nav-right">
#             <a href="advertise" target="_self" class="btn-text">Advertise</a>
#             <a href="submit" target="_self" class="btn-primary">Submit</a>
#         </div>
#     </nav>

#     <div style="height: 2px;"></div>
#     """, unsafe_allow_html=True)


# def render_navbar():
#     st.markdown("""
#     <style>
#         /* 1. 隐藏 Streamlit 默认顶部 Header */
#         header[data-testid="stHeader"] { display: none; }

#         /* 2. 调整主容器顶部空白 */
#         div[data-testid="block-container"] { padding-top: 20px !important; }

#         /* 3. 自定义导航栏 */
#         .custom-navbar {
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 70px;
#             background-color: #ffffff;
#             border-bottom: 1px solid #e5e7eb;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding: 0 40px;
#             z-index: 99999;
#             font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
#         }

#         /* 左侧：SkillNet + Home/Docs */
#         .nav-left {
#             display: flex;
#             align-items: center;
#             font-size: 20px;
#             font-weight: 700;
#             color: #111827;
#             text-decoration: none;
#             gap: 30px; /* SkillNet 与 Home/Docs 间距 */
#         }

#         /* 左侧的 Home/Docs 小链接 */
#         .nav-left a.nav-link {
#             font-size: 15px;
#             font-weight: 500;
#             color: #6b7280;
#             text-decoration: none;
#             transition: color 0.2s;
#         }
#         .nav-left a.nav-link:hover { color: #111827; }

#         /* 右侧按钮 */
#         .nav-right {
#             display: flex;
#             align-items: center;
#             gap: 15px;
#         }
#         .btn-text { color: #374151; text-decoration: none; font-size: 15px; font-weight: 500; }
#         .btn-text:hover { color: #111827; }

#         /* Github Icon */
#         .github-icon { display: flex; align-items: center; transition: opacity 0.2s; }
#         .github-icon:hover { opacity: 0.7; }

#         .btn-primary { background-color: #111827; color: white !important; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 600; transition: opacity 0.2s; }
#         .btn-primary:hover { opacity: 0.9; }
#         .custom-navbar a { text-decoration: none !important; }
#     </style>

#     <nav class="custom-navbar">
#         <div class="nav-left">
#             <a href="/" target="_self" class="skillnet-title">🕸️ SkillNet</a>
#             <a href="/" target="_self" class="nav-link">Home</a>
#             <a href="resources" target="_self" class="nav-link">Resources</a>
#             <a href="docs" target="_self" class="nav-link">Docs</a>
#         </div>
#         <div class="nav-right">
#             <a href="https://github.com/zjunlp" target="_blank" class="github-icon" title="View on GitHub">   
#                 <svg height="28" viewBox="0 0 16 16" version="1.1" width="28" aria-hidden="true" style="fill: #374151;">
#                     <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
#                 </svg>
#             </a>
#             <a href="submit" target="_self" class="btn-primary">Submit</a>
#         </div>
#     </nav>

#     <div style="height: 2px;"></div>
#     """, unsafe_allow_html=True)


# def render_logos():
#     st.write("")
#     st.divider()
#     st.markdown("""
#     <h5 style='text-align: center; color: #888; margin-bottom: 10px;'>Partners</h5>
# <style>
#     /* Logo Section */
#     .logo-container { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 40px; padding: 20px 0; }
#     .logo-item img { height: 40px; object-fit: contain; opacity: 1; transition: all 0.3s ease; cursor: pointer; }
#     .logo-item img:hover { transform: scale(1.1); }
# </style>
# """, unsafe_allow_html=True)
#     logos = [
#         {"name": "Zhejiang University", "url": "https://www.science.org/cms/asset/16dc26db-dd1c-407e-83be-3bc25a683d32/ZJU%20logo%20HD.png"},
#         {"name": "Tongji University", "url": "https://cdn.urongda.com//images/normal/medium/tongji-university-logo-1024px.png"},
#         {"name": "The University of Edinburgh", "url": "https://upload.wikimedia.org/wikipedia/zh/8/85/University_of_Edinburgh_Coat_of_Arm.svg"},
#         {"name": "NUS", "url": "https://upload.wikimedia.org/wikipedia/zh/thumb/9/9e/National_University_of_Singapore.svg/2560px-National_University_of_Singapore.svg.png"},
#         {"name": "Monash University", "url": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Monash_University_logo.svg"},
#         {"name": "UCLA", "url": "https://upload.wikimedia.org/wikipedia/commons/6/6c/University_of_California%2C_Los_Angeles_logo.svg"},
#         {"name": "UCSD", "url": "https://upload.wikimedia.org/wikipedia/commons/f/f6/UCSD_logo.png"},
#         {"name": "SUSTech", "url": "https://upload.wikimedia.org/wikipedia/zh/thumb/6/61/Southern_University_of_Science_and_Technology_logo.svg/500px-Southern_University_of_Science_and_Technology_logo.svg.png"},
#         {"name": "ZJHU", "url": "https://upload.wikimedia.org/wikipedia/zh/f/f9/%E6%B9%96%E5%B7%9E%E5%B8%88%E8%8C%83%E5%AD%A6%E9%99%A2%E6%A0%A1%E5%BE%BD.png"}
#     ]
#     logo_items = "".join([f'<div class="logo-item"><img src="{l["url"]}" title="{l["name"]}"></div>' for l in logos])
#     st.markdown(f'<div class="logo-container">{logo_items}</div>', unsafe_allow_html=True)

def get_base64_image(path):
    """将图片转为 base64 字符串"""
    path = Path(path)
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# def render_navbar():
#     # --- 新增步骤 1 & 2: 获取图片 Base64 并构建 src ---
#     # 假设图片是 jpg 格式。如果是 png，请将 image/jpeg 改为 image/png
#     logo_path = "./images/skillnet.png"
#     logo_base64 = get_base64_image(logo_path)
#     # 如果成功获取到 base64，则构建完整 src，否则留空（显示 alt 文本）
#     logo_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""
#     openkg_path = "./images/openkg.png"
#     openkg_base64 = get_base64_image(openkg_path)
#     openkg_src = f"data:image/png;base64,{openkg_base64}" if openkg_base64 else ""
#     # --------------------------------------------------

#     # 注意：这里使用了 f-string (f"""...""") 以便插入变量
#     st.markdown(f"""
#     <style>
#         /* 1. 隐藏 Streamlit 默认顶部 Header */
#         header[data-testid="stHeader"] {{ display: none; }}

#         /* 2. 调整主容器顶部空白 */
#         div[data-testid="block-container"] {{ padding-top: 20px !important; }}

#         /* 3. 自定义导航栏 */
#         .custom-navbar {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 70px;
#             background-color: #ffffff;
#             border-bottom: 1px solid #e5e7eb;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding: 0 40px;
#             z-index: 99999;
#             font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
#         }}

#         /* 左侧容器 */
#         .nav-left {{
#             display: flex;
#             align-items: center;
#             /* 移除了原先用于文本标题的 font-size/weight 样式 */
#             gap: 30px; /* Logo 与链接之间的间距 */
#         }}

#         /* --- 新增样式: Logo 图片样式 --- */
#         .nav-logo-img {{
#             height: 50px; /* 设置高度，根据导航栏高度(70px)适当调整 */
#             width: auto;  /* 保持图片比例 */
#             object-fit: contain; /* 确保图片完整显示 */
#             display: block; /* 修复图片底部的对齐间隙 */
#         }}
#         /* 包含 Logo 的链接样式，消除默认下划线等 */
#         .logo-link-wrapper {{
#              text-decoration: none;
#              display: flex;
#              align-items: center;
#         }}
#         /* ----------------------------- */

#         /* 左侧的 Home/Docs 小链接样式保持不变 */
#         .nav-left a.nav-link {{
#             font-size: 15px;
#             font-weight: 500;
#             color: #6b7280;
#             text-decoration: none;
#             transition: color 0.2s;
#         }}
#         .nav-left a.nav-link:hover {{ color: #111827; }}

#         /* 右侧按钮样式保持不变 */
#         .nav-right {{
#             display: flex;
#             align-items: center;
#             gap: 15px;
#         }}
#         .btn-text {{ color: #374151; text-decoration: none; font-size: 15px; font-weight: 500; }}
#         .btn-text:hover {{ color: #111827; }}

#         /* Github Icon */
#         .github-icon {{ display: flex; align-items: center; transition: opacity 0.2s; }}
#         .github-icon:hover {{ opacity: 0.7; }}

#         .btn-primary {{ background-color: #111827; color: white !important; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 600; transition: opacity 0.2s; }}
#         .btn-primary:hover {{ opacity: 0.9; }}
#         .custom-navbar a {{ text-decoration: none !important; }}
#     </style>

#     <nav class="custom-navbar">
#         <div class="nav-left">
#             <a href="/" target="_self" class="logo-link-wrapper">
#                 <img src="{logo_src}" alt="SkillNet Logo" class="nav-logo-img">
#             </a>
#             <a href="/" target="_self" class="nav-link">Home</a>
#             <a href="resources" target="_self" class="nav-link">Resources</a>
#             <a href="docs" target="_self" class="nav-link">Docs</a>
#             <a href="scenarios" target="_self" class="nav-link">Scenarios</a>
#         </div>
#         <div class="nav-right">
#             <a href="http://openkg.cn" target="_blank" class="logo-link-wrapper" title="Visit OpenKG.CN">     
#                 <img src="{openkg_src}" alt="OpenKG Logo" class="nav-logo-img">
#             </a>
#             <a href="https://github.com/zjunlp/SkillNet" target="_blank" class="github-icon" title="View on GitHub">
#                 <svg height="28" viewBox="0 0 16 16" version="1.1" width="28" aria-hidden="true" style="fill: #374151;">
#                     <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
#                 </svg>
#             </a>
#             <a href="contribute" target="_self" class="btn-primary">Contribute</a>
#         </div>
#     </nav>

#     <div style="height: 2px;"></div>
#     """, unsafe_allow_html=True)

def render_navbar():
    # --- 图片处理逻辑保持不变 ---
    logo_path = "./images/skillnet.png"
    logo_base64 = get_base64_image(logo_path)
    logo_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""
    openkg_path = "./images/openkg.png"
    openkg_base64 = get_base64_image(openkg_path)
    openkg_src = f"data:image/png;base64,{openkg_base64}" if openkg_base64 else ""
    # -------------------------

    st.markdown(f"""
    <style>
        header[data-testid="stHeader"] {{ display: none; }}
        div[data-testid="block-container"] {{ padding-top: 20px !important; }}

        .custom-navbar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70px;
            background-color: #ffffff;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 40px;
            z-index: 99999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;   
        }}

        /* --- 左侧容器 --- */
        .nav-left {{
            display: flex;
            align-items: center;
            gap: 30px;
            height: 100%; /* 关键：让左侧容器也撑满高度 */
        }}

        .nav-logo-img {{
            height: 50px;
            width: auto;
            object-fit: contain;
            display: block;
        }}
        .logo-link-wrapper {{
             text-decoration: none;
             display: flex;
             align-items: center;
        }}

        /* 普通链接样式 */
        .nav-left a.nav-link {{
            font-size: 15px;
            font-weight: 500;
            color: #6b7280;
            text-decoration: none;
            transition: color 0.2s;
            /* 增加一点上下内边距，增加鼠标交互面积 */
            padding: 10px 0;
        }}
        .nav-left a.nav-link:hover {{ color: #111827; }}

        /* ========== 修复核心：下拉菜单样式 ========== */

        /* 1. 下拉容器：设置为高度 100%，填满导航栏高度 */
        .dropdown {{
            position: relative;
            height: 100%;          /* 关键：填满导航栏高度(70px) */
            display: flex;         /* 使用 flex 布局 */
            align-items: center;   /* 让内部文字垂直居中 */
            cursor: pointer;
        }}

        /* 2. 按钮样式 */
        .dropbtn {{
            background-color: transparent;
            color: #6b7280;
            padding: 0;            /* 移除 padding，由父容器控制布局 */
            font-size: 15px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            font-family: inherit;
            transition: color 0.2s;
            height: 100%;          /* 按钮高度撑满 */
            display: flex;
            align-items: center;
        }}

        /* 悬停时按钮颜色 */
        .dropdown:hover .dropbtn {{
            color: #111827;
        }}

        /* 3. 下拉内容：无缝连接 */
        .dropdown-content {{
            display: none;
            position: absolute;
            background-color: #ffffff;
            min-width: 140px;      /* 稍微加宽一点，更好看 */
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            z-index: 100000;
            border: 1px solid #e5e7eb;
            border-radius: 0 0 8px 8px; /* 下方圆角 */

            /* 关键修复：top: 100% 意味着它紧贴着父容器(.dropdown)的底部 */
            top: 100%;
            left: -10px; /*稍微往左调整对齐，根据视觉微调 */

            padding: 5px 0; /* 给内部列表一点上下留白 */
        }}

        .dropdown-content a {{
            color: #374151;
            padding: 12px 20px;
            text-decoration: none;
            display: block;
            font-size: 14px;
            text-align: left;
            white-space: nowrap; /* 防止文字换行 */
        }}

        .dropdown-content a:hover {{
            background-color: #f9fafb;
            color: #111827;
        }}

        /* 显示逻辑 */
        .dropdown:hover .dropdown-content {{
            display: block;
        }}
        /* ======================================== */

        .nav-right {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .github-icon {{ display: flex; align-items: center; transition: opacity 0.2s; }}
        .github-icon:hover {{ opacity: 0.7; }}

        .btn-primary {{ background-color: #111827; color: white !important; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 600; transition: opacity 0.2s; }}
        .btn-primary:hover {{ opacity: 0.9; }}
        .custom-navbar a {{ text-decoration: none !important; }}
    </style>

    <nav class="custom-navbar">
        <div class="nav-left">
            <a href="/" target="_self" class="logo-link-wrapper">
                <img src="{logo_src}" alt="SkillNet Logo" class="nav-logo-img">
            </a>
            <a href="/" target="_self" class="nav-link">Home</a>
            <a href="ontology" target="_self" class="nav-link">Ontology</a>
            <a href="resources" target="_self" class="nav-link">Resource</a>
            <a href="package" target="_self" class="nav-link">Collection</a>
            <a href="skillx" target="_self" class="nav-link">SkillX</a >
            <a href="skillgym" target="_self" class="nav-link">SkillGym</a >
            <a href="skillfabric" target="_self" class="nav-link">SkillFabric</a >
            <div class="dropdown">
                <button class="dropbtn">Application&nbsp;<small>&#9662;</small></button>
                <div class="dropdown-content">
                    <a href="science" target="_self">Science</a>
                    <a href="coding" target="_self">Coding</a>
                </div>
            </div>
            <a href="docs" target="_self" class="nav-link">Docs</a>
        </div>
        <div class="nav-right">
            <a href="http://openkg.cn" target="_blank" class="logo-link-wrapper" title="Visit OpenKG.CN">       
                <img src="{openkg_src}" alt="OpenKG Logo" class="nav-logo-img">
            </a>
            <a href="https://github.com/zjunlp/SkillNet" target="_blank" class="github-icon" title="View on GitHub">
                <svg height="28" viewBox="0 0 16 16" version="1.1" width="28" aria-hidden="true" style="fill: #374151;">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            </a>
            <a href="contribute" target="_self" class="btn-primary">Contribute</a>
        </div>
    </nav>
    <div style="height: 2px;"></div>
    """, unsafe_allow_html=True)

def render_logos():
    # st.write("")
    st.divider()
    st.markdown("""
    <h5 style='text-align: center; color: #888; margin-bottom: 10px; margin-top: -10px;'>Partners</h5>
<style>
    /* Logo Section */
    .logo-container { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 40px; padding: 20px 0; }
    .logo-item img { height: 40px; object-fit: contain; opacity: 1; transition: all 0.3s ease; cursor: pointer; }
    .logo-item img:hover { transform: scale(1.1); }
</style>
""", unsafe_allow_html=True)

    # 本地图片列表
    logos = [
        {"name": "Zhejiang University", "path": "./images/zju.png"},
        {"name": "Tongji University", "path": "./images/tongji.png"},
        {"name": "Southeast University", "path": "./images/seu.png"},
        {"name": "The University of Edinburgh", "path": "./images/edinburgh.png"},
        {"name": "NUS", "path": "./images/nus.png"},
        {"name": "NTU", "path": "./images/ntu.png"},
        {"name": "Monash University", "path": "./images/monash.png"},
        {"name": "Fudan University", "path": "./images/fudan.png"},
        {"name": "UCLA", "path": "./images/ucla.png"},
        {"name": "UCSD", "path": "./images/ucsd.png"},
        {"name": "ZJHU", "path": "./images/zjhu.png"},
        {"name": "Alibaba", "path": "./images/alibaba.png"},
        {"name": "Tencent", "path": "./images/tencent.png"},
        {"name": "Ant", "path": "./images/ant.png"},
        {"name": "oppo", "path": "./images/oppo.png"},
        {"name": "readever", "path": "./images/readever.png"},
        {"name": "memtensor", "path": "./images/memtensor.png"},
        {"name": "Honor", "path": "./images/honor.png"},
        {"name": "UCAS", "path": "./images/ucas.png"}
    ]

    # 生成 HTML
    logo_items = ""
    for l in logos:
        img_b64 = get_base64_image(l["path"])
        if img_b64:
            logo_items += f'<div class="logo-item" style="display:inline-block;margin:10px;"><img src="data:image/png;base64,{img_b64}" title="{l["name"]}" style="height:60px;"></div>'

    st.markdown(f'<div style="text-align:center;">{logo_items}</div>', unsafe_allow_html=True)


@retry(tries=5, delay=2)
def get_embedding(text):
    url = "http://121.41.117.246:8000/v1/embeddings"
    payload = {
        "model": "/data/liangyuan/Qwen3-Embedding-0.6B",
        "input": text,
        "dimensions": 512
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()
    return result['data'][0]['embedding']
