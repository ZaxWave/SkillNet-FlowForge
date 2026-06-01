# # pages/coding.py
# import streamlit as st
# from utils import render_navbar

# # 1. 页面配置 (必须是第一个 Streamlit 命令)
# st.set_page_config(
#     page_title="Coding Scenarios - SkillNet",
#     page_icon="👨🏻‍💻",
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
# st.title("👨🏻‍💻 Coding Scenarios ")




# pages/coding.py
import streamlit as st
import time
import json
from utils import render_navbar

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Coding Scenarios - SkillNet",
    page_icon="👨🏻‍💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS (Terminal & UI Polish) ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
        
        /* Terminal Style for Logs */
        .terminal-box {
            background-color: #0c0c0c;
            color: #00ff00;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            padding: 15px;
            border-radius: 8px;
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 10px;
            white-space: pre-wrap;
            border: 1px solid #333;
            box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        }
        
        /* Code Editor Mockup */
        .code-window {
            background-color: #1e1e1e;
            border-radius: 8px;
            border: 1px solid #444;
            margin-bottom: 15px;
        }
        .code-header {
            background-color: #2d2d2d;
            padding: 5px 15px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-size: 12px;
            color: #ccc;
            display: flex;
            align-items: center;
        }
        .dot { height: 10px; width: 10px; background-color: #bbb; border-radius: 50%; display: inline-block; margin-right: 5px;}
        .red { background-color: #ff5f56; }
        .yellow { background-color: #ffbd2e; }
        .green { background-color: #27c93f; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. Render Navbar ---
render_navbar()

# --- 4. State Management ---
if 'code_stage' not in st.session_state:
    st.session_state.code_stage = 0 
if 'code_plan' not in st.session_state:
    st.session_state.code_plan = []

# --- 5. Main Interface ---

st.title("👨🏻‍💻 SkillNet for Autonomous Coding Agent")
st.markdown("""
**Scenario**: The Agent acts as a developer. It uses **SkillNet** to find the right skills, installs them, writes the code, and executes the task.
""")

# Progress Indicator
steps = ["1. Task Definition", "2. Logic Planning", "3. Library Search", "4. Environment Setup", "5. Code Gen & Run"]
current_step_name = steps[min(st.session_state.code_stage, 4)]
st.progress(min(st.session_state.code_stage * 25, 100), text=f"Current Phase: {current_step_name}")

st.divider()

# ==============================================================================
# STAGE 0: TASK DEFINITION
# ==============================================================================
if st.session_state.code_stage == 0:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("1. Task Definition")
        default_task = "Write a Python script to scrape the latest tech news headlines from a website, structure the data, and save it as a JSON file."
        user_task = st.text_area("Dev Task Description", value=default_task, height=120)
    
    with col2:
        st.info("💡 **Agent Logic**\nThe Agent analyzes the request to determine necessary capabilities (e.g., HTTP networking, HTML parsing, File I/O).")
        if st.button("Generate Dev Plan ➔", type="primary", use_container_width=True):
            with st.spinner("Analyzing requirements..."):
                time.sleep(1.0)
                # Hardcoded Plan
                st.session_state.code_plan = [
                    {"step": 1, "task": "Fetch HTML content", "query": "http requests", "skill": "requests-lib"},
                    {"step": 2, "task": "Parse HTML DOM", "query": "html parser", "skill": "beautifulsoup-tool"},
                    {"step": 3, "task": "Data Serialization", "query": "json handler", "skill": "pandas-lite"}
                ]
                st.session_state.code_stage = 1
                st.rerun()

# ==============================================================================
# STAGE 1: PLANNING
# ==============================================================================
elif st.session_state.code_stage == 1:
    st.subheader("2. Development Planning")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("**Constructed Workflow:**")
        st.json(st.session_state.code_plan)
    with c2:
        st.success("✅ Architecture Designed")
        st.write("The Agent has split the coding task into 3 modular steps. It now needs to query SkillNet for the best-performing libraries.")
        st.markdown("---")
        if st.button("Start SkillNet Search ➔", type="primary"):
            st.session_state.code_stage = 2
            st.rerun()

# # ==============================================================================
# # STAGE 2: SEARCH (API SIMULATION)
# # ==============================================================================
# elif st.session_state.code_stage == 2:
#     st.subheader("3. Skill Discovery (Search API)")
    
#     st.markdown("The Agent searches the SkillNet registry for optimized coding libraries.")
    
#     st.markdown("### 🤖 Agent Code execution")
#     st.code("""
# # Searching for optimal libraries
# for step in workflow:
#     # SkillNet Search API
#     best_tool = client.search(
#         query=step['query'], 
#         domain="python-dev", 
#         sort="popularity"
#     )
#     print(f"Selected: {best_tool.name}")
#     """, language="python")

#     if st.button("▶ Run Search Query", type="primary"):
#         with st.status("Querying Registry...", expanded=True):
#             plan = st.session_state.code_plan
            
#             # Step 1
#             st.write(f"📡 `GET /search?q={plan[0]['query']}`")
#             time.sleep(0.5)
#             st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[0]['skill']}** (Stars: 45k) - *Standard HTTP library*")
            
#             # Step 2
#             st.write(f"📡 `GET /search?q={plan[1]['query']}`")
#             time.sleep(0.5)
#             st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[1]['skill']}** (Stars: 32k) - *Robust DOM parser*")
            
#             # Step 3
#             st.write(f"📡 `GET /search?q={plan[2]['query']}`")
#             time.sleep(0.5)
#             st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[2]['skill']}** (Stars: 28k) - *Data manipulation*")
            
#         time.sleep(1)
#         st.session_state.code_stage = 3
#         st.rerun()

# ==============================================================================
# STAGE 2: SEARCH (API SIMULATION)
# ==============================================================================
elif st.session_state.code_stage == 2:
    st.subheader("3. Skill Discovery (Search)")
    
    st.markdown("The Agent searches the SkillNet registry for optimized coding libraries.")
    
    st.markdown("### 🤖 Agent Code execution")
    st.code("""
$ pip install skillnet-ai

from skillnet_ai import SkillNetClient
client = SkillNetClient()

# Agent Loop: Searching for skills
# Searching for optimal libraries
for step in workflow:
    # SkillNet Search API
    best_skill = client.search(
        query=step['query'], 
        domain="Development", 
        sort="stars"
    )
    print(f"Selected: {best_skill.skill_name}")
    """, language="python")

    # 初始化本阶段状态变量
    if 'code_stage2_search_done' not in st.session_state:
        st.session_state.code_stage2_search_done = False

    plan = st.session_state.code_plan

    # --- 情况 A: 还没搜索 (显示运行按钮) ---
    if not st.session_state.code_stage2_search_done:
        if st.button("▶ Run SkillNet Search", type="primary"):
            with st.status("Querying Registry...", expanded=True) as status:
                # Step 1
                st.write(f"📡 `GET /search?q={plan[0]['query']}`")
                time.sleep(0.5)
                st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[0]['skill']}** (Stars: 45k) - *Standard HTTP library*")
                
                # Step 2
                st.write(f"📡 `GET /search?q={plan[1]['query']}`")
                time.sleep(0.5)
                st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[1]['skill']}** (Stars: 32k) - *Robust DOM parser*")
                
                # Step 3
                st.write(f"📡 `GET /search?q={plan[2]['query']}`")
                time.sleep(0.5)
                st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[2]['skill']}** (Stars: 28k) - *Data manipulation*")
                
                status.update(label="Query Complete", state="complete", expanded=True)
            
            # 标记完成并刷新
            time.sleep(0.5)
            st.session_state.code_stage2_search_done = True
            st.rerun()

    # --- 情况 B: 搜索已完成 (显示静态日志 + 下一步按钮) ---
    else:
        # 1. 静态渲染日志 (保持视觉上的持久化)
        with st.status("Query Complete", expanded=True, state="complete"):
            st.write(f"📡 `GET /search?q={plan[0]['query']}`")
            st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[0]['skill']}** (Stars: 45k) - *Standard HTTP library*")
            
            st.write(f"📡 `GET /search?q={plan[1]['query']}`")
            st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[1]['skill']}** (Stars: 32k) - *Robust DOM parser*")
            
            st.write(f"📡 `GET /search?q={plan[2]['query']}`")
            st.success(f"&nbsp;&nbsp;&nbsp;✅ Found: **{plan[2]['skill']}** (Stars: 28k) - *Data manipulation*")
        
        # 2. 显示下一步按钮
        st.write("") # 增加间距
        if st.button("Proceed to Installation ➔", type="primary"):
            st.session_state.code_stage = 3
            # 清除本阶段状态以便 Reset 时重置 (可选)
            # del st.session_state.code_stage2_search_done
            st.rerun()

# ==============================================================================
# STAGE 3: INSTALLATION (Download API)
# ==============================================================================
elif st.session_state.code_stage == 3:
    st.subheader("4. Environment Setup (Download & Install)")
    
    st.markdown("Acquiring the selected skills and setting up the isolated runtime environment.")
    
    st.markdown("### 🤖 Agent Code execution")
    st.code("""
# Setting up runtime
env_path = "./active_env"
for skill in selected_skills:
    # 1. Download Skill
    pkg_path = client.download(skill.skill_url, target=env_path)
    # 2. Evaluate for use
    client.evaluate(pkg_path)
    """, language="python")

    # Intermediate State Logic (to fix button nesting issue)
    if 'code_installed' not in st.session_state:
        st.session_state.code_installed = False

    if not st.session_state.code_installed:
        if st.button("▶ Install Dependencies", type="primary"):
            log_container = st.empty()
            logs = []
            
            tools = ["requests-lib", "beautifulsoup-tool", "pandas-lite"]
            
            for tool in tools:
                logs.append(f"📦 Resolving {tool}...")
                log_container.markdown(f'<div class="terminal-box">{"".join(logs)}</div>', unsafe_allow_html=True)
                time.sleep(0.4)
                
                logs.append(f"⬇️ Downloading binary... 100%")
                log_container.markdown(f'<div class="terminal-box">{"".join(logs)}</div>', unsafe_allow_html=True)
                time.sleep(0.3)
                
                logs.append(f"✅ Evaluated {tool} successfully.\n")
                log_container.markdown(f'<div class="terminal-box">{"".join(logs)}</div>', unsafe_allow_html=True)
            
            st.session_state.code_installed = True
            st.rerun()
            
    else:
        # Static logs after install
        st.markdown("""
        <div class="terminal-box">
📦 Resolving requests-lib... 
⬇️ Downloading binary... 100%
✅ Evaluated requests-lib successfully.

📦 Resolving beautifulsoup-tool...
⬇️ Downloading binary... 100%
✅ Evaluated beautifulsoup-tool successfully.

📦 Resolving pandas-lite...
⬇️ Downloading binary... 100%
✅ Evaluated pandas-lite successfully.
        </div>
        """, unsafe_allow_html=True)
        
        st.success("Runtime Environment Ready.")
        if st.button("Proceed to Coding ➔", type="primary"):
            st.session_state.code_stage = 4
            del st.session_state.code_installed # Clean up
            st.rerun()

# ==============================================================================
# STAGE 4: EXECUTION (Code Gen & Run)
# ==============================================================================
elif st.session_state.code_stage == 4:
    st.subheader("5. Autonomous Coding & Execution")
    
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.markdown("### 🛠 Active Environment")
        st.markdown("- `requests-lib` v2.31")
        st.markdown("- `beautifulsoup-tool` v4.12")
        st.markdown("- `pandas-lite` v1.5")
        
        st.write("")
        st.info("The Agent will now combine these skills to write the script script.py")
        
        st.write("")
        st.write("")
        if st.button("🔄 Reset Demo"):
            for key in ['code_stage', 'code_plan', 'code_installed', 'code_generated']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.code_stage = 0
            st.rerun()

    with col_right:
        if 'code_generated' not in st.session_state:
            st.session_state.code_generated = False
            
        if not st.session_state.code_generated:
            if st.button("▶ Generate & Run Code", type="primary"):
                with st.spinner("Writing Python script..."):
                    time.sleep(1.5)
                    st.session_state.code_generated = True
                    st.rerun()
        else:
            # 1. Show the Generated Code
            st.markdown("**📄 generated_script.py**")
            code_content = """import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_news():
    url = "https://mock-tech-news.com"
    print(f"Connecting to {url}...")
    
    # Using Skill: requests-lib
    response = requests.get(url)
    
    # Using Skill: beautifulsoup-tool
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='headline')
    
    data = []
    for art in articles[:3]:
        data.append({
            "title": art.text.strip(),
            "timestamp": time.time()
        })
    
    return data

if __name__ == "__main__":
    results = scrape_news()
    print(json.dumps(results, indent=2))
"""
            st.code(code_content, language="python")
            
            # 2. Show the Execution Output
            st.markdown("**🖥️ Execution Output**")
            st.markdown("""
            <div class="terminal-box">
$ python generated_script.py
Connecting to https://mock-tech-news.com...
[
  {
    "title": "SkillNet AI Agents outperform traditional scripts",
    "timestamp": 1716382910.23
  },
  {
    "title": "New Python release emphasizes AI integration",
    "timestamp": 1716382910.45
  },
  {
    "title": "Global GPU shortage easing up",
    "timestamp": 1716382910.67
  }
]
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Task Completed Successfully!")
            
            # 3. Download Result
            st.download_button(
                label="📥 Download Source Code (.py)",
                data=code_content,
                file_name="scraper_agent.py",
                mime="text/x-python",
                type="primary"
            )