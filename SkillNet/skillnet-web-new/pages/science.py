# # pages/science.py
# import streamlit as st
# from utils import render_navbar

# # 1. 页面配置 (必须是第一个 Streamlit 命令)
# st.set_page_config(
#     page_title="Science Scenario - SkillNet",
#     page_icon="🔬",
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
# st.title("🔬 Science Scenario")







# # pages/science.py
# import streamlit as st
# import time
# import os
# from utils import render_navbar

# # --- 1. Page Configuration ---
# st.set_page_config(
#     page_title="Science Scenario - SkillNet",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Hide Sidebar & Style Tweaks
# st.markdown(
#     """
#     <style>
#         [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
#             display: none;
#         }
#         .stStatusWidget > div {
#             box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
#             border-radius: 10px;
#         }
#         /* Custom font style for logs to look like terminal */
#         .mock-terminal {
#             font-family: 'Courier New', Courier, monospace;
#             font-size: 0.85em;
#             background-color: #f0f2f6;
#             padding: 10px;
#             border-radius: 5px;
#             white-space: pre-wrap;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # --- 2. Render Navbar ---
# render_navbar()

# # --- 3. Mock Data & Helpers ---

# def simulate_processing(seconds=1.5):
#     """Simple helper to simulate processing time."""
#     time.sleep(seconds)

# # --- 4. Main Page Content ---

# st.title("🔬 SkillNet AI Scientist: From Task to Discovery")
# st.markdown("""
# This demo illustrates the **SkillNet** workflow where an AI Agent autonomously plans and executes a scientific mission.

# 1.  **Task Definition**: User provides a high-level research goal.
# 2.  **AI Planning**: The Agent decomposes the goal into logical steps.
# 3.  **Skill Discovery**: The Agent searches the **SkillNet** for specialized skills matching each step.
# 4.  **Execution**: Skills are downloaded, validated, and composed into a pipeline.
# """)

# st.divider()

# # --- Interactive Section: Task Definition ---
# col1, col2 = st.columns([2, 1])
# with col1:
#     default_mission = "Analyze single-cell RNA-seq data to identify potential cancer therapeutic targets, validate them against clinical databases, and write a summary report."
#     user_mission = st.text_area("📝 User Mission (Task Definition)", value=default_mission, height=100)

# with col2:
#     st.info("💡 **System Status**\n\nMode: **Simulation (Demo)**\n\nAgent is online and ready.")
#     start_btn = st.button("🚀 Start Scientific Discovery Agent", type="primary", use_container_width=True)

# # --- Simulation Logic ---
# if start_btn:
    
#     # Define the mock plan (based on the notebook)
#     plan = [
#         {"step": 1, "phase": "Data Processing", "query": "cellxgene", "expected_skill": "cellxgene-census", "stars": 15976},
#         {"step": 2, "phase": "Mechanism Analysis", "query": "kegg", "expected_skill": "kegg-database", "stars": 17598},
#         {"step": 3, "phase": "Target Validation", "query": "gget", "expected_skill": "gget", "stars": 16081},
#         {"step": 4, "phase": "Reporting", "query": "scientific writing", "expected_skill": "citation-management", "stars": 16204}
#     ]

#     # --- A. ORCHESTRATION SIMULATION ---
#     with st.status("🤖 AI Agent Orchestration (Planning & Acquisition)", expanded=True) as status:
#         st.write("Initializing SkillNet Client...")
#         time.sleep(0.5)
        
#         for task in plan:
#             st.markdown(f"**Phase {task['step']}: {task['phase']}**")
            
#             # 1. Search Simulation
#             st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;🔍 Searching SkillNet for: `{task['query']}`...")
#             time.sleep(0.4)
#             st.success(f"&nbsp;&nbsp;&nbsp;&nbsp;✅ Found Skill: **{task['expected_skill']}** (⭐ {task['stars']})")
            
#             # 2. Download Simulation
#             st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;⬇️ Downloading to `./active_skills_library/{task['expected_skill']}`...")
#             time.sleep(0.3)
            
#             # 3. Evaluate Simulation
#             st.caption(f"&nbsp;&nbsp;&nbsp;&nbsp;⚖️ Quality Check: Safety: Good | Completeness: Good | Executability: Good")
#             time.sleep(0.3)
        
#         st.markdown("---")
#         st.write("🔗 **Analyzing Skill Relationships (SkillNet Analyzer)...**")
#         time.sleep(0.8)
#         st.code("""
# Found 2 dependencies between skills:
# - gget --[compose_with]--> kegg-database
# - cellxgene-census --[compose_with]--> gget
#         """, language="text")
        
#         status.update(label="✅ Orchestration Complete: 4 skills ready for execution.", state="complete", expanded=False)

#     # --- B. EXECUTION SIMULATION ---
#     st.subheader("🚀 Execution Phase")

#     # Phase 1: Data Processing
#     with st.container():
#         st.markdown("### Phase 1: Data Processing")
#         st.caption("Active Skill: `cellxgene-census`")
        
#         c1, c2 = st.columns([3, 2])
#         with c1:
#             with st.spinner("Running single-cell analysis pipeline..."):
#                 simulate_processing(1.5)
#                 # Hardcoded log from the Notebook
#                 st.code("""
# ▶️ Running Skill: [cellxgene-census]...
# normalizing counts per cell... finished
# computing PCA (n_comps=50)... finished
# computing neighbors... finished
# computing UMAP... finished
# running Leiden clustering... finished (found 3 clusters)
# ranking genes... finished
# ✅ [cellxgene-census] Completed.
# Identified Target: 'EGFR'
#                 """, language="text")
#         with c2:
#             st.success("**Target Identified**")
#             st.metric(label="Gene Symbol", value="EGFR", delta="High Confidence")
#             st.info("Source dataset: cellxgene-census (Homo sapiens, RNA)")

#     st.markdown("---")

#     # Phase 2: Mechanism Analysis
#     with st.container():
#         st.markdown("### Phase 2: Mechanism Analysis")
#         st.caption("Active Skill: `kegg-database`")
        
#         with st.spinner("Mapping gene to biological pathways..."):
#             simulate_processing(1.0)
#             st.write("The Agent uses `scripts/kegg_api.py` to map the gene.")
#             col_kegg1, col_kegg2 = st.columns(2)
#             with col_kegg1:
#                 st.code("""
# ▶️ Running Skill: [kegg-database] (Input: EGFR)...
# ✅ [kegg-database] Completed.
# Mapped EGFR to 50 pathways.
#                 """, language="text")
#             with col_kegg2:
#                 with st.expander("📂 View Retrieved Pathways", expanded=True):
#                     st.write("- `path:hsa01521` (EGFR tyrosine kinase inhibitor resistance)")
#                     st.write("- `path:hsa01522` (Endocrine resistance)")
#                     st.write("- `path:hsa03272` (Platinum drug resistance)")
#                     st.caption("...and 47 others.")

#     st.markdown("---")

#     # Phase 3: Target Validation
#     with st.container():
#         st.markdown("### Phase 3: Target Validation")
#         st.caption("Active Skill: `gget` (Open Targets)")

#         with st.spinner("Cross-referencing Open Targets Platform..."):
#             simulate_processing(1.0)
            
#             c_val1, c_val2 = st.columns([1, 1])
#             with c_val1:
#                 st.code("""
# ▶️ Running Skill: [gget]...
# Querying Open Targets GraphQL API...
# ✅ [gget] Completed.
# Validated target associations.
#                 """, language="text")
#             with c_val2:
#                 st.success("**Clinical Validation Confirmed**")
#                 st.write("Top Associated Diseases:")
#                 st.markdown("- 🫁 **Non-small cell lung carcinoma**")
#                 st.markdown("- 🫁 **Lung adenocarcinoma**")
#                 st.markdown("- 🏥 **Cancer (General)**")

#     st.markdown("---")

#     # Phase 4: Reporting
#     with st.container():
#         st.markdown("### Phase 4: Final Reporting")
#         st.caption("Active Skill: `citation-management`")

#         with st.spinner("Compiling data and formatting citations..."):
#             simulate_processing(1.2)
            
#             report_content = """
# ### Scientific Discovery Report: EGFR Analysis
# *Generated by SkillNet AI Scientist*

# #### 1. Data Processing
# **Skill**: `cellxgene-census`  
# Using standardized single-cell analysis pipelines [Wolf et al., 2018], we identified **EGFR** as a significant marker.

# #### 2. Biological Mechanism
# **Skill**: `kegg-database`  
# Pathway enrichment analysis [Kanehisa, 2000] identified 50 associated pathways, linking EGFR to key biological processes:
# - `path:hsa01521`
# - `path:hsa01522`
# - `path:hsa03272`

# #### 3. Therapeutic Validation
# **Skill**: `gget`  
# Cross-referencing with clinical databases [Open Targets, 2024] confirms therapeutic relevance for:
# - **Non-small cell lung carcinoma**
# - **Lung adenocarcinoma**
# - **Cancer**

# #### 4. References (Managed by citation-management)
# 1. Wolf, F. A., et al. (2018). Scanpy: large-scale single-cell gene expression data analysis. Genome biology.
# 2. Kanehisa, M. & Goto, S. (2000). KEGG: kyoto encyclopedia of genes and genomes. Nucleic acids research.
# 3. Open Targets Platform (2024). version 24.03.
#             """
            
#             st.success("✅ Report Generated Successfully")
#             st.markdown(report_content)
            
#             # Simulated Download Button
#             st.download_button(
#                 label="📥 Download Full PDF Report",
#                 data=report_content,
#                 file_name="EGFR_Discovery_Report.md",
#                 mime="text/markdown"
#             )




# pages/science.py
import streamlit as st
import time
import json
from utils import render_navbar

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Science Scenario - SkillNet",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Terminal-like visuals and Step progress
st.markdown(
    """
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
        
        /* Terminal Style for Logs */
        .terminal-box {
            background-color: #1e1e1e;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 10px;
            white-space: pre-wrap;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .cmd-text { color: #ebdbb2; } /* Command color */
        .log-info { color: #83a598; } /* Info color */
        
        /* Step Indicator */
        .step-container {
            padding: 10px;
            background-color: #f0f2f6;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 5px solid #ff4b4b;
        }
    </style>
    """,
    unsafe_allow_html=True
)

render_navbar()

# --- 2. State Management ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0  # 0:Start, 1:Plan, 2:Search, 3:Install, 4:Execute
if 'plan' not in st.session_state:
    st.session_state.plan = []
if 'logs' not in st.session_state:
    st.session_state.logs = ""

# --- 3. Mock Helpers ---
def type_writer_log(text, speed=0.01):
    """Simulates real-time terminal output"""
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        # Only update periodically to save render performance
        if len(full_text) % 5 == 0: 
            placeholder.markdown(f'<div class="terminal-box">{full_text}█</div>', unsafe_allow_html=True)
        time.sleep(speed)
    placeholder.markdown(f'<div class="terminal-box">{full_text}</div>', unsafe_allow_html=True)

# --- 4. Main Interface ---

st.title("🔬 SkillNet for Autonomous Scientific Discovery")
st.markdown("""
This demo demonstrates the **SkillNet** workflow where an AI Agent autonomously plans and executes a scientific mission. 
You will act as the human overseer while the Agent uses the SkillNet SDK to orchestrate a scientific discovery.
""")

# Progress Indicator
steps = ["1. Task Definition", "2. AI Planning", "3. Skill Discovery (Search)", "4. Acquisition & Eval", "5. Execution"]
current_step_name = steps[min(st.session_state.stage, 4)]
st.progress(min(st.session_state.stage * 25, 100), text=f"Current Phase: {current_step_name}")

st.divider()

# ==============================================================================
# STAGE 0: TASK DEFINITION
# ==============================================================================
if st.session_state.stage == 0:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("1. Define Research Goal")
        default_mission = "Analyze single-cell RNA-seq data to identify potential cancer therapeutic targets, validate them against clinical databases, and write a summary report."
        mission = st.text_area("User Mission", value=default_mission, height=150)
    
    with col2:
        st.info("💡 **Agent Logic**\nThe Agent will first analyze this natural language request and decompose it into a structured plan requiring specific technical skills.")
        if st.button("Generate Plan ➔", type="primary", use_container_width=True):
            with st.spinner("Decomposing task..."):
                time.sleep(1.0)
                # Hardcoded Plan
                st.session_state.plan = [
                    {"step": 1, "phase": "Data Processing", "query": "cellxgene", "expected_skill": "cellxgene-census"},
                    {"step": 2, "phase": "Mechanism Analysis", "query": "kegg pathway", "expected_skill": "kegg-database"},
                    {"step": 3, "phase": "Target Validation", "query": "gene enhancement", "expected_skill": "gget"},
                    {"step": 4, "phase": "Reporting", "query": "scientific citation", "expected_skill": "citation-management"}
                ]
                st.session_state.stage = 1
                st.rerun()

# ==============================================================================
# STAGE 1: AI PLANNING
# ==============================================================================
elif st.session_state.stage == 1:
    st.subheader("2. AI Planning & Decomposition")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("**Generated Execution Plan (JSON):**")
        st.json(st.session_state.plan)
    with c2:
        st.success("✅ Plan Generated")
        st.write("The Agent has identified 4 distinct phases. Now it needs to find the skills to execute them.")
        st.markdown("---")
        st.markdown("**Next Step: SkillNet Search**")
        st.write("The Agent will now use `client.search()` to find skills in the SkillNet registry.")
        if st.button("Proceed to Skill Discovery ➔", type="primary"):
            st.session_state.stage = 2
            st.rerun()

# # ==============================================================================
# # STAGE 2: SKILL DISCOVERY (SEARCH)
# # ==============================================================================
# elif st.session_state.stage == 2:
#     st.subheader("3. Skill Discovery (The Search API)")
    
#     st.markdown("The Agent is constructing API calls to find the best skills.")
    
#     # Display the "Simulated Code"
#     st.markdown("### 🤖 Agent Code Execution")
#     st.code("""
# # Agent Loop: Searching for skills
# found_skills = []
# for step in plan:
#     print(f"Searching for: {step['query']}...")
#     # SkillNet API Call
#     results = client.search(q=step['query'], limit=1, sort_by="stars")
#     found_skills.append(results[0])
#     """, language="python")

#     if st.button("▶ Run SkillNet Search", type="primary"):
#         log_text = ""
#         mock_results = [
#             {"name": "cellxgene-census", "stars": 15976, "desc": "API for querying single-cell data."},
#             {"name": "kegg-database", "stars": 17598, "desc": "Interface for Kyoto Encyclopedia of Genes."},
#             {"name": "gget", "stars": 16081, "desc": "Gene enhancement tool & OpenTargets wrapper."},
#             {"name": "citation-management", "stars": 16204, "desc": "BibTeX formatting and validation."}
#         ]
        
#         # Simulated Terminal Output
#         with st.status("Running Search...", expanded=True):
#             for i, item in enumerate(mock_results):
#                 query = st.session_state.plan[i]['query']
#                 st.write(f"📡 `POST /api/v1/search?q={query}`")
#                 time.sleep(0.4)
#                 st.write(f"&nbsp;&nbsp;&nbsp;✅ **Found:** `{item['name']}` (⭐ {item['stars']})")
#                 st.caption(f"&nbsp;&nbsp;&nbsp;Desc: {item['desc']}")
#                 time.sleep(0.4)
        
#         st.success("All skills located in registry.")
#         time.sleep(1)
#         st.session_state.stage = 3
#         st.rerun()

# ==============================================================================
# STAGE 2: SKILL DISCOVERY (SEARCH)
# ==============================================================================
elif st.session_state.stage == 2:
    st.subheader("3. Skill Discovery (Search)")
    
    st.markdown("The Agent is constructing API calls to find the best skills.")
    
    # Display the "Simulated Code"
    st.markdown("### 🤖 Agent Code Execution")
    st.code("""
$ pip install skillnet-ai

from skillnet_ai import SkillNetClient
client = SkillNetClient()

# Agent Loop: Searching for skills
found_skills = []
for step in plan:
    print(f"Searching for: {step['query']}...")
    # SkillNet API Call
    results = client.search(q=step['query'], limit=1, sort_by="stars")
    found_skills.append(results[0])
    """, language="python")

    # 定义数据（用于动画展示和静态保持）
    mock_results = [
        {"name": "cellxgene-census", "stars": 15976, "desc": "API for querying single-cell data."},
        {"name": "kegg-database", "stars": 17598, "desc": "Interface for Kyoto Encyclopedia of Genes."},
        {"name": "gget", "stars": 16081, "desc": "Gene enhancement tool & OpenTargets wrapper."},
        {"name": "citation-management", "stars": 16204, "desc": "BibTeX formatting and validation."}
    ]

    # 初始化本阶段状态
    if 'stage2_search_done' not in st.session_state:
        st.session_state.stage2_search_done = False

    # --- 情况 A：尚未搜索（显示搜索按钮）---
    if not st.session_state.stage2_search_done:
        if st.button("▶ Run SkillNet Search", type="primary"):
            # 运行动态搜索动画
            with st.status("Running Search...", expanded=True) as status:
                for i, item in enumerate(mock_results):
                    # 获取 plan 中的 query，防止索引越界加个保护
                    query = st.session_state.plan[i]['query'] if i < len(st.session_state.plan) else "tool"
                    
                    st.write(f"📡 `POST /api/v1/search?q={query}`")
                    time.sleep(0.4)
                    st.write(f"&nbsp;&nbsp;&nbsp;✅ **Found:** `{item['name']}` (⭐ {item['stars']})")
                    st.caption(f"&nbsp;&nbsp;&nbsp;Desc: {item['desc']}")
                    time.sleep(0.4)
                
                status.update(label="Search Complete", state="complete", expanded=True)
            
            # 关键点：标记完成并刷新，进入情况 B
            st.session_state.stage2_search_done = True
            st.rerun()

    # --- 情况 B：搜索已完成（显示静态日志 + 下一步按钮）---
    else:
        # 1. 重新渲染日志（静态），营造“日志没有消失”的视觉效果
        with st.status("Search Complete", expanded=True, state="complete"):
            for i, item in enumerate(mock_results):
                query = st.session_state.plan[i]['query'] if i < len(st.session_state.plan) else "tool"
                st.write(f"📡 `POST /api/v1/search?q={query}`")
                st.write(f"&nbsp;&nbsp;&nbsp;✅ **Found:** `{item['name']}` (⭐ {item['stars']})")
                st.caption(f"&nbsp;&nbsp;&nbsp;Desc: {item['desc']}")
        
        st.success("All skills located in registry.")
        
        # 2. 显示进入下一阶段的按钮
        st.markdown("---") # 加个分割线更好看
        if st.button("▶ Install & Evaluate Skills", type="primary"):
            st.session_state.stage = 3
            # 清理本阶段状态（可选，如果希望 Reset 时重置）
            # del st.session_state.stage2_search_done 
            st.rerun()

# ==============================================================================
# STAGE 3: ACQUISITION & EVALUATION (修复版)
# ==============================================================================
elif st.session_state.stage == 3:
    st.subheader("4. Acquisition & Evaluation (The Download/Eval API)")
    
    st.markdown("Before execution, skills must be downloaded to the local environment and evaluated for safety.")
    
    st.markdown("### 🤖 Agent Code Execution")
    st.code("""
# Agent Loop: Downloading and Validating
for skill in found_skills:
    # 1. Download to local workspace
    local_path = client.download(url=skill.url, target_dir="./skills")
    
    # 2. SkillNet Evaluation (Safety Check)
    report = client.evaluate(target=local_path)
    if report['safety'] == 'Low':
        raise SecurityError("Skill unsafe!")
    """, language="python")

    # 初始化本阶段的中间状态
    if 'stage3_installed' not in st.session_state:
        st.session_state.stage3_installed = False

    # 按钮 1：执行安装（如果尚未安装）
    if not st.session_state.stage3_installed:
        if st.button("▶ Install & Evaluate Skills", type="primary"):
            # Terminal visual for download
            log_lines = []
            container = st.empty()
            
            skill_names = ["cellxgene-census", "kegg-database", "gget", "citation-management"]
            
            for name in skill_names:
                # Download Sim
                new_line = f"⬇️ [download] {name}... "
                log_lines.append(new_line)
                container.markdown(f'<div class="terminal-box">{"".join(log_lines)}</div>', unsafe_allow_html=True)
                time.sleep(0.3)
                
                log_lines[-1] += "100% OK\n"
                container.markdown(f'<div class="terminal-box">{"".join(log_lines)}</div>', unsafe_allow_html=True)
                
                # Eval Sim
                log_lines.append(f"⚖️ [evaluate] {name}... Safety: PASS | Executability: PASS\n")
                container.markdown(f'<div class="terminal-box">{"".join(log_lines)}</div>', unsafe_allow_html=True)
                time.sleep(0.3)

            # 标记安装完成，并强制刷新以显示下一步按钮
            st.session_state.stage3_installed = True
            st.rerun()

    # 如果安装已完成，显示静态日志结果和下一步按钮
    else:
        # 显示最终状态的日志（静态，防止消失）
        st.markdown("""
        <div class="terminal-box">
⬇️ [download] cellxgene-census... 100% OK
⚖️ [evaluate] cellxgene-census... Safety: PASS | Executability: PASS
⬇️ [download] kegg-database... 100% OK
⚖️ [evaluate] kegg-database... Safety: PASS | Executability: PASS
⬇️ [download] gget... 100% OK
⚖️ [evaluate] gget... Safety: PASS | Executability: PASS
⬇️ [download] citation-management... 100% OK
⚖️ [evaluate] citation-management... Safety: PASS | Executability: PASS
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✅ Skills installed and verified. Ready for Science.")
        
        # 按钮 2：进入下一阶段
        if st.button("Proceed to Execution ➔", type="primary"):
            st.session_state.stage = 4
            # 清理中间状态，以便下次重置时能重新演示
            del st.session_state.stage3_installed 
            st.rerun()

# ==============================================================================
# STAGE 4: EXECUTION
# ==============================================================================
elif st.session_state.stage == 4:
    st.subheader("5. Scientific Execution Phase")
    
    st.info("The Agent has now assembled the Python environment. It will now chain the skills together to solve the problem.")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### Active Skills")
        st.markdown("- 🧬 `cellxgene`")
        st.markdown("- 🔬 `kegg-db`")
        st.markdown("- 🎯 `gget`")
        st.markdown("- 📄 `citation`")
        
        if st.button("🔄 Reset Demo"):
            st.session_state.stage = 0
            st.rerun()

    with col2:
        start_exec = st.button("▶ Run Scientific Pipeline", type="primary")
        
        if start_exec:
            # ---------------------------------------------------------
            # SIMULATED EXECUTION LOGIC (Similar to previous, but faster)
            # ---------------------------------------------------------
            
            # Phase 1
            with st.expander("Step 1: Data Processing (cellxgene)", expanded=True):
                with st.spinner("Processing single-cell data..."):
                    time.sleep(1)
                    st.code("Selected Marker Gene: EGFR (p-value: 1.2e-45)", language="text")
                    st.success("Target Identified: EGFR")

            # Phase 2
            with st.expander("Step 2: Mechanism Analysis (kegg)", expanded=True):
                with st.spinner("Mapping pathways..."):
                    time.sleep(1)
                    st.write("Found 3 key pathways:")
                    st.markdown("- `path:hsa01521` (EGFR tyrosine kinase inhibitor resistance)")
                    st.markdown("- `path:hsa01522` (Endocrine resistance)")

            # Phase 3 & 4 Combined for brevity
            with st.expander("Step 3 & 4: Validation & Reporting", expanded=True):
                st.write("Validating against Open Targets...")
                time.sleep(0.5)
                st.markdown("**Linked Diseases:** Non-small cell lung carcinoma")
                
                st.markdown("---")
                st.markdown("### Final Output")
                report = """
**Discovery Report**
- **Target**: EGFR
- **Mechanism**: Kinase inhibitor resistance pathways identified.
- **Validation**: Confirmed relevance in Lung Carcinoma (Open Targets).
- **Citations**: Validated via SkillNet citation manager.
                """
                st.success(report)

                full_report_content = """
# Scientific Discovery Report: EGFR Analysis
*Generated by SkillNet AI Scientist*

## 1. Data Processing
**Skill**: `cellxgene-census`
Using standardized single-cell analysis pipelines [Wolf et al., 2018], we identified **EGFR** as a significant marker (p-value < 1e-45).

## 2. Biological Mechanism
**Skill**: `kegg-database`
Pathway enrichment analysis [Kanehisa, 2000] identified associated pathways linking EGFR to:
- `path:hsa01521` (EGFR tyrosine kinase inhibitor resistance)
- `path:hsa01522` (Endocrine resistance)

## 3. Therapeutic Validation
**Skill**: `gget`
Cross-referencing with clinical databases [Open Targets, 2024] confirms therapeutic relevance for:
- Non-small cell lung carcinoma
- Lung adenocarcinoma

## 4. References
1. Wolf, F. A., et al. (2018). Scanpy: large-scale single-cell gene expression data analysis.
2. Kanehisa, M. & Goto, S. (2000). KEGG: kyoto encyclopedia of genes and genomes.
3. Open Targets Platform (2024). version 24.03.
            """

            st.download_button(
                label="📥 Download Full PDF Report",
                data=full_report_content,
                file_name="SkillNet_EGFR_Report.md", # 实际下载为MD文件，模拟PDF体验
                mime="text/markdown",
                type="primary"
            )