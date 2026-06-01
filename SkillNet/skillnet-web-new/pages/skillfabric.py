import html
import json
import time
from pathlib import Path

import streamlit as st

from utils import render_navbar


st.set_page_config(
    page_title="SkillFabric Demo - SkillNet",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed",
)


ASSET_DIR = Path(__file__).resolve().parent.parent / "images"
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "skillfabric_demo" / "agentskillos_penguin_demo.json"
WORKFLOW_PLAN_PATH = Path(__file__).resolve().parent.parent / "data" / "skillfabric_demo" / "workflow_plan_penguin.json"
GRAPH_IMAGE_PATH = ASSET_DIR / "skillfabric_graph.png"
WORKFLOW_IMAGE_PATH = ASSET_DIR / "skillfabric_workflow.png"
STAGE_KEY = "skillfabric_demo_stage"
VIEW_KEY = "skillfabric_view"
SUBSTRATE_DONE_KEY = "skillfabric_substrate_done"
SEARCH_DONE_KEY = "skillfabric_search_done"
WIKI_DONE_KEY = "skillfabric_wiki_done"
WORKFLOW_DONE_KEY = "skillfabric_workflow_done"


@st.cache_data
def load_demo_data(mtime):
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


@st.cache_data
def load_workflow_plan_download(mtime):
    plan = json.loads(WORKFLOW_PLAN_PATH.read_text(encoding="utf-8"))
    return json.dumps(plan, indent=2, ensure_ascii=False)


def esc(value):
    return html.escape(str(value), quote=True)


def set_stage(stage):
    st.session_state[STAGE_KEY] = stage


def reset_demo():
    st.session_state[STAGE_KEY] = 0
    for key in (SUBSTRATE_DONE_KEY, SEARCH_DONE_KEY, WIKI_DONE_KEY, WORKFLOW_DONE_KEY):
        st.session_state.pop(key, None)


def open_demo():
    st.session_state[VIEW_KEY] = "demo"
    reset_demo()


def badge(text, tone="green"):
    classes = {
        "green": "sf-badge-green",
        "blue": "sf-badge-blue",
        "orange": "sf-badge-orange",
        "purple": "sf-badge-purple",
        "gray": "sf-badge-gray",
    }
    return f'<span class="sf-badge {classes.get(tone, "sf-badge-gray")}">{esc(text)}</span>'


def render_agent_code(code, language="python"):
    st.markdown("### Agent Code Execution")
    st.code(code.strip(), language=language)


def render_css():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
            :root {
                --sf-ink: #111827;
                --sf-muted-text: #6b7280;
                --sf-bg: #f8f9fa;
                --sf-surface: #ffffff;
                --sf-surface-soft: #f8fafc;
                --sf-border: #e5e7eb;
                --sf-primary: #667eea;
                --sf-primary-dark: #5a67d8;
                --sf-primary-soft: #eef2ff;
                --sf-purple: #764ba2;
                --sf-purple-dark: #5b3b7c;
                --sf-purple-soft: #f5f3ff;
                --sf-pink: #f5576c;
                --sf-pink-dark: #c93852;
                --sf-pink-soft: #fff1f3;
                --sf-blue: #4facfe;
                --sf-blue-dark: #2563eb;
                --sf-blue-soft: #eff6ff;
                --sf-cyan: #00f2fe;
                --sf-cyan-soft: #ecfeff;
                --sf-orange: #f59e0b;
                --sf-orange-dark: #b45309;
                --sf-orange-soft: #fff7ed;
                --sf-gray-soft: #f3f4f6;
            }
            .stApp { background-color: var(--sf-bg); }
            div[data-testid="block-container"] {
                padding-top: 18px !important;
                max-width: 1220px;
            }
            [data-testid="stStatusWidget"], .stStatusWidget {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                pointer-events: none !important;
            }
            .sf-plan-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 10px;
            }
            .sf-plan-mini {
                min-height: 86px;
                border: 1px solid var(--sf-border);
                border-left: 4px solid #667eea;
                border-radius: 8px;
                background: #ffffff;
                padding: 12px;
            }
            .sf-plan-mini strong {
                display: block;
                color: var(--sf-ink);
                font-size: 0.94rem;
                line-height: 1.25;
                margin-bottom: 7px;
            }
            .sf-plan-mini span {
                color: var(--sf-muted-text);
                font-size: 0.82rem;
                line-height: 1.35;
            }
            .sf-candidate-mini-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 10px;
                margin-top: 10px;
            }
            .sf-candidate-mini {
                border: 1px solid var(--sf-border);
                background: #ffffff;
                border-radius: 8px;
                padding: 11px 12px;
            }
            .sf-candidate-mini strong {
                display: block;
                color: var(--sf-ink);
                font-size: 0.93rem;
                margin-bottom: 4px;
            }
            .sf-candidate-mini span {
                color: var(--sf-muted-text);
                font-size: 0.8rem;
            }
            .sf-workflow-row {
                border: 1px solid var(--sf-border);
                background: #ffffff;
                border-radius: 8px;
                padding: 12px 14px;
                margin-bottom: 9px;
            }
            .sf-workflow-row strong {
                color: var(--sf-ink);
                font-size: 0.94rem;
            }
            .sf-workflow-row p {
                color: var(--sf-muted-text);
                font-size: 0.86rem;
                line-height: 1.38;
                margin: 6px 0 0;
            }
            .sf-workflow-row small {
                display: block;
                color: #6b7280;
                margin-top: 6px;
            }
            @media (max-width: 900px) {
                .sf-plan-grid,
                .sf-candidate-mini-grid {
                    grid-template-columns: 1fr;
                }
            }
            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-color: #667eea;
                color: white;
                border-radius: 8px;
                min-height: 42px;
                font-weight: 700;
            }
            div.stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #5a67d8 0%, #68408f 100%);
                border-color: #5a67d8;
                color: white;
            }
            div.stButton > button {
                border-radius: 8px;
                min-height: 42px;
                border-color: #c7d2fe;
                color: #4f46e5;
                background: #ffffff;
                font-weight: 650;
            }
            div.stButton > button:hover {
                border-color: #667eea;
                color: #4338ca;
                background: #eef2ff;
            }
            .sf-muted {
                color: var(--sf-muted-text);
                font-size: 0.9rem;
                line-height: 1.55;
            }
            .sf-badge-row {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 10px;
            }
            .sf-badge {
                display: inline-flex;
                align-items: center;
                border: 1px solid;
                border-radius: 999px;
                padding: 3px 9px;
                font-size: 0.75rem;
                font-weight: 650;
                line-height: 1.2;
                white-space: nowrap;
            }
            .sf-badge-green { background: #ecfdf5; color: #047857; border-color: #a7f3d0; }
            .sf-badge-blue { background: var(--sf-blue-soft); color: var(--sf-blue-dark); border-color: #d3dde5; }
            .sf-badge-orange { background: var(--sf-orange-soft); color: var(--sf-orange-dark); border-color: #fed7aa; }
            .sf-badge-purple { background: var(--sf-purple-soft); color: var(--sf-purple-dark); border-color: #ddd6fe; }
            .sf-badge-gray { background: var(--sf-gray-soft); color: #4b5563; border-color: var(--sf-border); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_landing():
    st.markdown(
        """
        <style>
            @keyframes sfPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">🕸️ SkillFabric</h1>
            <p style="font-size: 1.5rem; color: #666; margin-bottom: 1.5rem;">
                Skill Graph + Wiki Memory for Agent Routing
            </p>
            <div style="
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 0.75rem 2rem;
                border-radius: 50px;
                font-size: 1.2rem;
                font-weight: bold;
                animation: sfPulse 2s infinite;
            ">
                ⚠️ COMING SOON ⚠️
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; max-width: 980px; margin: 0 auto; padding: 1rem 0;">
            <p style="font-size: 1.1rem; color: #444; line-height: 1.8; max-width: 930px; margin: 0 auto;">
                <strong>SkillFabric</strong> organizes reusable agent skills with a clean skill graph and LLM-readable wiki memory,
                helping agents retrieve, reason over, and compose skills for complex tasks.
            </p>
            <p style="font-size: 1.1rem; color: #444; line-height: 1.8; margin: 1rem auto 0; max-width: 980px;">
                The demo below previews routing a task to a compact skill package and converting it into a traceable workflow plan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    demo_col_left, demo_col_mid, demo_col_right = st.columns([1.2, 1, 1.2])
    with demo_col_mid:
        if st.button("🚀 Try Interactive Demo", type="primary", width="stretch"):
            open_demo()
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎯 Core Modules")
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                color: white;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🕸️</div>
                <h3 style="margin-bottom: 0.5rem;">Skill Graph</h3>
                <p style="font-size: 0.95rem; opacity: 0.9;">Build Clean Skill-Level Knowledge Graphs</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                color: white;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
                <h3 style="margin-bottom: 0.5rem;">Wiki Memory</h3>
                <p style="font-size: 0.95rem; opacity: 0.9;">Generate LLM-Readable Skill and Community Pages</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                color: white;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔀</div>
                <h3 style="margin-bottom: 0.5rem;">Routing + Workflow</h3>
                <p style="font-size: 0.95rem; opacity: 0.9;">Select Skills and Compose Traceable Workflows</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 📋 Feature Details")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🕸️ Skill Graph - Details"):
        st.markdown(
            """
            **Build Clean Skill-Level Knowledge Graphs**

            - Compile reusable skills into SkillNode and CommunityNode structures.
            - Model relations such as similar_to, compose_with, depend_on, and member_of.
            - Use graph propagation to support candidate retrieval and workflow ordering.
            """
        )
    with st.expander("📚 Wiki Memory - Details"):
        st.markdown(
            """
            **Generate LLM-Readable Skill and Community Pages**

            - Materialize graph knowledge into concise Markdown wiki pages.
            - Build query-local wiki context for grounded LLM reasoning.
            - Preserve evidence and trace files for inspection and debugging.
            """
        )
    with st.expander("🔀 Routing and Workflow - Details"):
        st.markdown(
            """
            **Select Skills and Compose Traceable Workflows**

            - Retrieve candidate skills with semantic, graph, and wiki signals.
            - Rerank candidates through local wiki exploration.
            - Generate workflow plans with selected skills, dependencies, and validation traces.
            """
        )

    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0; color: #666;">
            <p style="font-size: 1rem;">🚀 Under active development — demo preview available now.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_substrate_items(data):
    stats = data.get("stats", {})
    wiki_skill_pages = stats.get("wiki_skill_pages", 0)
    wiki_community_pages = stats.get("wiki_community_pages", 0)
    wiki_workflow_pages = stats.get("wiki_workflow_pages", 0)
    wiki_root_pages = stats.get("wiki_root_pages", 0)
    wiki_pages = stats.get(
        "wiki_pages",
        wiki_skill_pages + wiki_community_pages + wiki_workflow_pages + wiki_root_pages,
    )
    return [
        {
            "title": "Skill KG",
            "value": f'{stats.get("skills", 0)} skills',
            "detail": f'{stats.get("communities", 0)} communities and {stats.get("graph_links", 0)} graph links',
        },
        {
            "title": "Wiki Memory",
            "value": f"{wiki_pages} pages",
            "detail": (
                f"{wiki_skill_pages} skill, "
                f"{wiki_community_pages} community, "
                f"{wiki_workflow_pages} workflow, "
                f"{wiki_root_pages} index/debug pages"
            ),
        },
        {
            "title": "Workflow Hints",
            "value": f'{stats.get("workflow_hints", 0)} accepted flows',
            "detail": (
                f'{stats.get("wiki_workflow_pages", 0)} workflow pages; '
                f'{stats.get("query_local_workflow_hints", 0)} attached in this route'
            ),
        },
        {
            "title": "Interfaces",
            "value": f'{stats.get("interfaces_accepted", 0)} accepted',
            "detail": f'{stats.get("interfaces", stats.get("interfaces_accepted", 0))} extracted contracts checked for planner use',
        },
    ]


def simplified_skill_package(data):
    return [
        {
            "skill": item.get("skill", ""),
            "role": item.get("role", ""),
            "why_selected": item.get("reason", ""),
        }
        for item in data.get("selected_skills", [])
    ]


def render_demo(data):
    scenario = data.get("scenario", {})
    stats = data.get("stats", {})
    stage = min(max(int(st.session_state.get(STAGE_KEY, 0)), 0), 4)
    st.session_state[STAGE_KEY] = stage

    st.title("🕸️ SkillFabric Routing Demo")
    st.markdown(
        "SkillFabric first builds a skill KG and wiki memory, then routes a task through graph candidates, "
        "wiki-grounded LLM reasoning, and planner-only workflow orchestration."
    )

    steps = [
        "1. Task Definition",
        "2. KG + Wiki",
        "3. Graph Routing",
        "4. Wiki Reasoning",
        "5. Workflow Plan",
    ]
    st.progress(min(stage * 25, 100), text=f"Current Phase: {steps[stage]}")
    st.divider()

    if stage == 0:
        col1, col2 = st.columns([1.55, 0.95], gap="large")
        with col1:
            st.subheader("1. Define Task")
            st.text_area(
                "User Mission",
                value=scenario.get(
                    "query",
                    "Analyze penguin morphology data, generate figures, write a report, and create slides.",
                ),
                height=128,
            )
        with col2:
            st.info(
                "💡 **Agent Logic** "
                "The agent uses SkillFabric's prebuilt skill KG and wiki memory to build a query-local routing context, "
                "then asks the wiki explorer to select the final skill package."
            )
            if st.button("Build KG + Wiki Context ➔", type="primary", width="stretch"):
                set_stage(1)
                st.rerun()

    elif stage == 1:
        st.subheader("2. KG + Wiki Substrate")
        st.markdown(
            "Before routing, SkillFabric compiles skill interfaces into a KG and materializes wiki pages for LLM-readable memory."
        )
        if SUBSTRATE_DONE_KEY not in st.session_state:
            st.session_state[SUBSTRATE_DONE_KEY] = False

        c1, c2 = st.columns([0.95, 1.05], gap="large")
        with c1:
            render_agent_code(
                """
skillfabric build --workspace demo
skillfabric build-wiki --workspace demo
                """.strip(),
                language="bash",
            )
            st.markdown("**Built Artifacts**")
            substrate_html = "".join(
                '<div class="sf-plan-mini">'
                f'<strong>{esc(item["title"])}</strong>'
                f'<span>{badge(item["value"], "blue")}<br>{esc(item["detail"])}</span>'
                '</div>'
                for item in build_substrate_items(data)
            )
            st.markdown(f'<div class="sf-plan-grid">{substrate_html}</div>', unsafe_allow_html=True)
        with c2:
            action_slot = st.empty()
            if st.session_state[SUBSTRATE_DONE_KEY]:
                if action_slot.button("Proceed to Graph Routing ➔", type="primary", width="stretch"):
                    set_stage(2)
                    st.rerun()
                with st.status("KG + Wiki Ready", expanded=True, state="complete"):
                    st.write(f"🧩 {stats.get('interfaces_accepted', 0)} planner-usable SkillContracts")
                    st.write(f"🕸️ {stats.get('skills', 0)} skills, {stats.get('communities', 0)} communities, {stats.get('graph_links', 0)} graph links")
                    st.write(
                        f"📚 {stats.get('wiki_pages', 0)} wiki pages "
                        f"({stats.get('wiki_skill_pages', 0)} skill / "
                        f"{stats.get('wiki_community_pages', 0)} community / "
                        f"{stats.get('wiki_workflow_pages', 0)} workflow / "
                        f"{stats.get('wiki_root_pages', 0)} index)"
                    )
                    st.write(
                        f"🔗 {stats.get('workflow_hints', 0)} accepted compatibility flows; "
                        f"{stats.get('query_local_workflow_hints', 0)} attached to this route"
                    )
            else:
                if action_slot.button("▶ Build Substrate", type="primary", width="stretch"):
                    with st.status("Building KG + Wiki...", expanded=True) as status:
                        st.write("🧩 extracting planner-usable SkillContracts")
                        time.sleep(0.25)
                        st.write(f"✅ {stats.get('interfaces_accepted', 0)} accepted contracts")
                        time.sleep(0.2)
                        st.write("🕸️ compiling SkillNode / CommunityNode graph")
                        time.sleep(0.25)
                        st.write(
                            f"✅ {stats.get('skills', 0)} skills, "
                            f"{stats.get('communities', 0)} communities, "
                            f"{stats.get('graph_links', 0)} graph links"
                        )
                        time.sleep(0.2)
                        st.write("📚 materializing skill, community, and workflow wiki pages")
                        time.sleep(0.25)
                        st.write(
                            f"✅ {stats.get('wiki_pages', 0)} wiki pages "
                            f"({stats.get('wiki_skill_pages', 0)} skill / "
                            f"{stats.get('wiki_community_pages', 0)} community / "
                            f"{stats.get('wiki_workflow_pages', 0)} workflow / "
                            f"{stats.get('wiki_root_pages', 0)} index)"
                        )
                        time.sleep(0.2)
                        st.write("🔗 indexing workflow compatibility hints")
                        time.sleep(0.25)
                        st.write(
                            f"✅ {stats.get('workflow_hints', 0)} accepted flows; "
                            f"{stats.get('query_local_workflow_hints', 0)} attached to this route"
                        )
                        status.update(label="KG + Wiki Ready", state="complete", expanded=True)
                    st.session_state[SUBSTRATE_DONE_KEY] = True
                    st.rerun()

    elif stage == 2:
        st.subheader("3. Graph Routing: Query-Local Candidate Bundle")
        st.markdown("The router uses the raw task query to seed semantic/lexical retrieval, expands over the KG, and attaches wiki pages plus workflow hints.")

        candidates = data.get("candidates", [])[:8]
        retrieve_code = f"""
bundle = build_router_bundle(
    RouterBundleConfig(
        workspace="demo",
        query=task,
        seed_limit=8,
        expanded_limit=16,
    )
)
"""
        if SEARCH_DONE_KEY not in st.session_state:
            st.session_state[SEARCH_DONE_KEY] = False

        code_col, trace_col = st.columns([0.95, 1.05], gap="large")
        with code_col:
            render_agent_code(retrieve_code, language="python")
            if GRAPH_IMAGE_PATH.exists():
                st.image(str(GRAPH_IMAGE_PATH), caption="Route-relevant skill graph", width="stretch")
        with trace_col:
            action_slot = st.empty()
            if not st.session_state[SEARCH_DONE_KEY]:
                if action_slot.button("▶ Run SkillFabric Retrieval", type="primary", width="stretch"):
                    with st.status("Building Query-Local Bundle...", expanded=True) as status:
                        st.write("🔎 seed candidates with semantic + lexical signals")
                        time.sleep(0.25)
                        st.write("🕸️ expand over compose_with / depend_on / similar_to edges")
                        time.sleep(0.25)
                        st.write(
                            f"📚 attach {stats.get('query_local_pages', 21)} local wiki pages "
                            f"and {stats.get('query_local_workflow_hints', 2)} workflow hints"
                        )
                        time.sleep(0.25)
                        for item in candidates[:5]:
                            st.write(f"✅ `{item.get('skill', '')}`")
                            time.sleep(0.25)
                            st.caption(f"score {item.get('score', 0):.2f} · {item.get('reason', '')}")
                        status.update(label="Candidate Bundle Ready", state="complete", expanded=True)
                    st.session_state[SEARCH_DONE_KEY] = True
                    st.rerun()
            else:
                if action_slot.button("Run LLM Wiki Reasoning ➔", type="primary", width="stretch"):
                    set_stage(3)
                    st.rerun()
                with st.status("Candidate Bundle Ready", expanded=True, state="complete"):
                    st.write("🔎 semantic + lexical seed retrieval")
                    st.write("🕸️ KG expansion with route-relevant edges")
                    st.write(
                        f"📚 {stats.get('query_local_pages', 21)} query-local wiki pages; "
                        f"{stats.get('query_local_workflow_hints', 2)} workflow hints"
                    )
                    for item in candidates[:5]:
                        st.write(f"✅ `{item.get('skill', '')}` · score {item.get('score', 0):.2f}")

                candidate_html = "".join(
                    '<div class="sf-candidate-mini">'
                    f'<strong>{esc(item.get("skill", ""))}</strong>'
                    f'<span>score {item.get("score", 0):.2f}</span>'
                    '</div>'
                    for item in candidates[:5]
                )
                st.markdown(f'<div class="sf-candidate-mini-grid">{candidate_html}</div>', unsafe_allow_html=True)
                st.success("Query-local candidate bundle ready for wiki reasoning.")

    elif stage == 3:
        st.subheader("4. LLM Wiki Reasoning: Final Route Result")
        st.markdown(
            "The wiki explorer reads query-local pages and asks the LLM to select the smallest useful skill package plus ordering edges."
        )

        pages = data.get("pages_read", [])[:10]
        selected = simplified_skill_package(data)
        wiki_code = """
route = route_task(
    RouterConfig(
        workspace="demo",
        query=task,
        explorer_mode="agentic",
    )
)
"""
        if WIKI_DONE_KEY not in st.session_state:
            st.session_state[WIKI_DONE_KEY] = False

        c1, c2 = st.columns([0.95, 1.05], gap="large")
        with c1:
            render_agent_code(wiki_code, language="python")
        with c2:
            action_slot = st.empty()
            if not st.session_state[WIKI_DONE_KEY]:
                if action_slot.button("▶ Run Wiki Explorer", type="primary", width="stretch"):
                    with st.status("LLM Reasoning Over Wiki...", expanded=True) as status:
                        for page in pages[:4]:
                            st.write(f"📖 `read_page('{page}')`")
                            time.sleep(0.25)
                        st.write("🧠 select minimal useful skill package")
                        time.sleep(0.25)
                        st.write("🔗 infer required_edges from workflow hints")
                        time.sleep(0.4)
                        for item in selected:
                            st.write(f"✅ `{item['skill']}`")
                            time.sleep(0.15)
                        status.update(label="Route Result Ready", state="complete", expanded=True)
                    st.session_state[WIKI_DONE_KEY] = True
                    st.rerun()
            else:
                if action_slot.button("Compose Workflow Plan ➔", type="primary", width="stretch"):
                    set_stage(4)
                    st.rerun()
                st.markdown("**RouteResult.selected_skills**")
                skill_html = "".join(
                    '<div class="sf-candidate-mini">'
                    f'<strong>{esc(item["skill"])}</strong>'
                    f'<span>{esc(item["role"])}</span>'
                    '</div>'
                    for item in selected
                )
                st.markdown(f'<div class="sf-candidate-mini-grid">{skill_html}</div>', unsafe_allow_html=True)
                st.success("✅ Final route result ready")
                with st.expander("Why these skills?"):
                    st.write(data.get("rerank_summary", "The local wiki produced a compact skill package."))

    else:
        st.subheader("5. Planner-only Workflow Orchestration")

        workflow = data.get("workflow", [])
        dependencies = data.get("dependencies", [])

        col1, col2 = st.columns([0.95, 1.05], gap="large")
        with col1:
            render_agent_code(
                """
result = plan_workflow(WorkflowPlanConfig(workspace="demo"), route)
validate_workflow_plan(
    result.plan,
    allowed_skill_ids=route.selected_skill_ids,
    required_edges=route.required_edges,
)
                """.strip(),
                language="python",
            )
            if WORKFLOW_IMAGE_PATH.exists():
                st.image(str(WORKFLOW_IMAGE_PATH), caption="Composed execution workflow", width="stretch")

        with col2:
            if WORKFLOW_DONE_KEY not in st.session_state:
                st.session_state[WORKFLOW_DONE_KEY] = False

            action_slot = st.empty()
            if not st.session_state[WORKFLOW_DONE_KEY]:
                if action_slot.button("▶ Generate Workflow Plan", type="primary", width="stretch"):
                    with st.status("Composing Workflow...", expanded=True) as status:
                        for step in workflow:
                            deps = ", ".join(step.get("depends_on", [])) or "root"
                            st.write(
                                f"🔗 `{step.get('id', '')}` -> `{step.get('skill', '')}` "
                                f"(depends on: {deps})"
                            )
                            time.sleep(0.3)
                        st.write("✅ `validate_workflow(workflow_plan)`")
                        status.update(label="Workflow Ready", state="complete", expanded=True)
                    st.session_state[WORKFLOW_DONE_KEY] = True
                    st.rerun()
            else:
                if action_slot.button("🔄 Reset Demo", type="primary", width="stretch"):
                    reset_demo()
                    st.rerun()
                with st.expander("Workflow Plan", expanded=True):
                    workflow_html = ""
                    for step in workflow:
                        deps = ", ".join(step.get("depends_on", [])) or "root"
                        workflow_html += (
                            '<div class="sf-workflow-row">'
                            f'<strong>{esc(step.get("id", ""))}: {esc(step.get("skill", ""))}</strong>'
                            f'<p>{esc(step.get("purpose", ""))}</p>'
                            f'<small>depends on: {esc(deps)}</small>'
                            '</div>'
                        )
                    st.markdown(workflow_html, unsafe_allow_html=True)

                with st.expander("Dependency Evidence"):
                    for dep in dependencies:
                        st.markdown(
                            f"- `{dep.get('before', '')}` → `{dep.get('after', '')}` "
                            f"({dep.get('label', '')}, confidence={dep.get('confidence', 0):.2f})"
                        )

                st.download_button(
                    label="📥 Download workflow_plan.json",
                    data=load_workflow_plan_download(WORKFLOW_PLAN_PATH.stat().st_mtime),
                    file_name="workflow_plan.json",
                    mime="application/json",
                    type="primary",
                )


def main():
    render_css()
    render_navbar()
    data = load_demo_data(DATA_PATH.stat().st_mtime)
    if STAGE_KEY not in st.session_state:
        st.session_state[STAGE_KEY] = 0
    if VIEW_KEY not in st.session_state:
        st.session_state[VIEW_KEY] = "landing"

    if st.session_state[VIEW_KEY] != "demo":
        render_landing()
        return

    render_demo(data)


if __name__ == "__main__":
    main()
