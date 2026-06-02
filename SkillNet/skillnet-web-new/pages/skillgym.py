# pages/skillgym.py
import streamlit as st
from utils import render_navbar

# 1. Page Configuration
st.set_page_config(
    page_title="SkillGym - Coming Soon",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default sidebar
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

# 2. Render Navbar
render_navbar(active_page="skillgym")

# 3. Hero Section
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">🏋️ SkillGym</h1>
        <p style="font-size: 1.5rem; color: #666; margin-bottom: 1.5rem;">
            Skill Lifecycle Evaluation Platform
        </p>
        <div style="
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: bold;
            animation: pulse 2s infinite;
        ">
            ⚠️ COMING SOON ⚠️
        </div>
    </div>

    <style>
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 4. Introduction
st.markdown("""
<div style="text-align: center; max-width: 800px; margin: 0 auto; padding: 1rem 0;">
    <p style="font-size: 1.1rem; color: #444; line-height: 1.8;">
        <strong>SkillGym</strong> is a comprehensive platform focused on <strong>AI Agent Skill lifecycle evaluation</strong>.
        From Skill creation, execution to adaptation, SkillGym provides an all-in-one evaluation and training environment,
        empowering developers to build more powerful and reliable AI skills.
    </p>
    <p style="font-size: 1.1rem; color: #444; line-height: 1.8; margin-top: 1rem;">
        Additionally, SkillGym provides an <strong>automated pipeline for synthesizing Harbor-type task data</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 5. Core Modules
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
            <div style="font-size: 3rem; margin-bottom: 1rem;">🛠️</div>
            <h3 style="margin-bottom: 0.5rem;">Skill Creation</h3>
            <p style="font-size: 0.95rem; opacity: 0.9;">Build & Generate High-Quality Skills</p>
        </div>
        """,
        unsafe_allow_html=True
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
            <div style="font-size: 3rem; margin-bottom: 1rem;">▶️</div>
            <h3 style="margin-bottom: 0.5rem;">Skill Execution</h3>
            <p style="font-size: 0.95rem; opacity: 0.9;">Run & Test Skill Performance</p>
        </div>
        """,
        unsafe_allow_html=True
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
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔄</div>
            <h3 style="margin-bottom: 0.5rem;">Skill Adaptation</h3>
            <p style="font-size: 0.95rem; opacity: 0.9;">Optimize & Adapt Skill Capabilities</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# 6. Feature Details (Expandable)
st.markdown("### 📋 Feature Details")
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("🛠️ Skill Creation - Details"):
    st.markdown("""
    **Build & Generate High-Quality Skills**

    - **Auto Generation**: Automatically generate Skills from code repositories, documents, and conversation logs using LLMs
    - **Template-Based Creation**: Standardized templates for quickly building structured Skills
    - **Quality Validation**: Automatic safety and completeness checks during creation
    - **Version Management**: Support for Skill version control and iteration tracking
    """)

with st.expander("▶️ Skill Execution - Details"):
    st.markdown("""
    **Run & Test Skill Performance**

    - **Sandbox Environment**: Safely execute Skills in an isolated environment
    - **Performance Monitoring**: Real-time monitoring of execution time, resource consumption, and other metrics
    - **Test Suites**: Built-in multi-dimensional test cases to validate Skill reliability
    - **Log Tracing**: Complete execution log recording and replay functionality
    """)

with st.expander("🔄 Skill Adaptation - Details"):
    st.markdown("""
    **Optimize & Adapt Skill Capabilities**

    - **Feedback-Driven**: Automatically optimize Skill behavior based on execution feedback
    - **Scenario Adaptation**: Adjust Skill parameters for different application scenarios
    - **Continuous Learning**: Support for online learning and knowledge updates
    - **Effect Evaluation**: Multi-dimensional assessment of adaptation effects with quantified improvement metrics
    """)

st.markdown("---")

# 7. Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <p style="font-size: 1rem;">
        🚀 Under active development — stay tuned!
    </p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        Follow <a href="https://github.com/zjunlp/SkillNet" style="color: #667eea; text-decoration: none;">GitHub</a> for the latest updates
    </p>
</div>
""", unsafe_allow_html=True)
