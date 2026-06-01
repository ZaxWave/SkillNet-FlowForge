# pages/skillx_page.py
import streamlit as st
from utils import render_navbar
import os

# 1. Page Configuration
st.set_page_config(
    page_title="SkillX - Skill Knowledge Bases for Agents",
    page_icon="📚",
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
        h1, h2, h3 {
            scroll-margin-top: 2rem;
        }
        .figure-caption-wrapper {
            display: flex;
            justify-content: center;
            margin-top: 0.5rem;
            margin-bottom: 2rem;
        }
        .figure-caption {
            text-align: center;
            font-size: 1.3rem;
            color: #555;
            line-height: 1.6;
            width: 50%;
        }
        .stImage {
            text-align: center;
        }
        .stImage img {
            max-width: 50%;
            height: auto;
            margin: 0 auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. Render Navbar
render_navbar()

# 3. Hero Section
st.markdown(
    """
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">📚 SkillX</h1>
        <p style="font-size: 1.3rem; color: #666; margin-bottom: 1rem;">
            Automatically Constructing Skill Knowledge Bases for Agents
        </p>
        <p style="font-size: 1.3rem; color: #888;">
            <strong>Chenxi Wang</strong><sup>*1,2</sup> &nbsp;
            <strong>Zhuoyun Yu</strong><sup>*1,2</sup> &nbsp;
            <strong>Xin Xie</strong><sup>2</sup> &nbsp;
            <strong>Wuguannan Yao</strong><sup>2</sup> &nbsp;
            <strong>Runnan Fang</strong><sup>1</sup> &nbsp;
            <strong>Shuofei Qiao</strong><sup>1</sup> &nbsp;
            <strong>Kexin Cao</strong><sup>1</sup><br/>
            <strong>Guozhou Zheng</strong><sup>1</sup> &nbsp;
            <strong>Xiang Qi</strong><sup>2</sup> &nbsp;
            <strong>Peng Zhang</strong><sup>2</sup> &nbsp;
            <strong>Shumin Deng</strong><sup>1</sup>
        </p>
        <p style="font-size: 0.85rem; color: #999;">
            <sup>1</sup>Zhejiang University &nbsp;&nbsp; <sup>2</sup>Ant Digital Technologies, Ant Group
        </p>
        <p style="margin-top: 1rem;">
            <a href="https://github.com/zjunlp/SkillX" style="text-decoration: none;">
                <img src="https://img.shields.io/badge/GitHub-Code-black?logo=github" alt="GitHub"/>
            </a>
            <a href="https://arxiv.org/abs/2604.04804" style="text-decoration: none;">
                <img src="https://img.shields.io/badge/arXiv-2604.04804-b5212f.svg?logo=arxiv" alt="arXiv"/>
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 4. Abstract
st.markdown("## 📝 Abstract")
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
                padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea;">
    <p style="font-size: 1rem; line-height: 1.8; color: #333; margin: 0;">
        Learning from experience is critical for building capable large language model (LLM) agents, yet prevailing self-evolving paradigms remain inefficient: agents learn in isolation, repeatedly re-discover similar behaviors from limited experience, resulting in redundant exploration and poor generalization. <strong>SkillX</strong> is a fully automated framework for constructing a <strong>plug-and-play skill knowledge base</strong> that can be reused across agents and environments. SkillX operates through a fully automated pipeline built on <strong>three synergistic innovations</strong>: (i) Multi-Level Skills Design, (ii) Iterative Skills Refinement, and (iii) Exploratory Skills Expansion.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 5. Three Core Innovations
st.markdown("## 🎯 Three Core Innovations")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            color: white;
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">📊</div>
            <h3 style="margin-bottom: 0.8rem;">Multi-Level Skills Design</h3>
            <p style="font-size: 0.9rem; opacity: 1.3; line-height: 1.6;">
                Distills raw trajectories into <strong>three-tiered hierarchy</strong>:
                <br/>• Planning Skills
                <br/>• Functional Skills
                <br/>• Atomic Skills
            </p>
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
            padding: 1.5rem;
            text-align: center;
            color: white;
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🔄</div>
            <h3 style="margin-bottom: 0.8rem;">Iterative Skills Refinement</h3>
            <p style="font-size: 0.9rem; opacity: 1.3; line-height: 1.6;">
                Automatically revises skills based on <strong>execution feedback</strong>:
                <br/>• Skills Merge
                <br/>• Skills Filter
                <br/>• Continuous Quality Improvement
            </p>
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
            padding: 1.5rem;
            text-align: center;
            color: white;
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🚀</div>
            <h3 style="margin-bottom: 0.8rem;">Exploratory Skills Expansion</h3>
            <p style="font-size: 0.9rem; opacity: 1.3; line-height: 1.6;">
                Proactively generates and validates <strong>novel skills</strong>:
                <br/>• Beyond seed training data
                <br/>• Experience-guided exploration
                <br/>• Broader skill coverage
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# 6. Key Results Highlight
st.markdown("## 📈 Key Results")
st.markdown(
    """
    <div style="text-align: center; padding: 1rem 0;">
        <p style="font-size: 1.1rem; color: #444; line-height: 1.8;">
            Using a strong backbone agent (<strong>GLM-4.6</strong>), SkillX builds a reusable skill library
            and evaluates its transferability on challenging benchmarks:
            <strong>AppWorld</strong>, <strong>BFCL-v3</strong>, and <strong>τ²-Bench</strong>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Performance Gain (Qwen3-32B)", value="~10%", delta="Avg improvement")
with col2:
    st.metric(label="Benchmarks Tested", value="3", delta="AppWorld, BFCL-v3, τ²-Bench")
with col3:
    st.metric(label="Plug-and-Play", value="✓", delta="Directly reusable")

st.markdown("---")

# 7. Figures Section
st.markdown("## 📊 Figures & Results")

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
skillx_dir = os.path.join(script_dir, "skillx")

# Figure 1: Pipeline
st.markdown("### Figure 1: SkillX Pipeline")
col_left, col_img, col_right = st.columns([1, 2, 1])
with col_img:
    st.image(os.path.join(skillx_dir, "overview.png"))
st.markdown(
    """
    <div class="figure-caption-wrapper">
        <div class="figure-caption">
            <strong>Figure 1.</strong> SkillX provides an <strong>automated, iterative pipeline</strong> for constructing
            a skills library, integrating skills extraction, skills expansion and skills refinement. The skills library
            is organized into three levels: <strong>planning skills</strong>, <strong>functional skills</strong>,
            and <strong>atomic skills</strong>.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Figure 2: Main Results (Table 1)
st.markdown("### Table 1: Main Results")
col_left, col_img, col_right = st.columns([1, 2, 1])
with col_img:
    st.image(os.path.join(skillx_dir, "main_result.png"))
st.markdown(
    """
    <div class="figure-caption-wrapper">
        <div class="figure-caption">
            <strong>Table 1.</strong> Main results of SkillX on three benchmarks: <strong>BFCL-V3</strong>,
            <strong>AppWorld</strong>, and <strong>τ²-Bench</strong>. Methods with ∗ mean that the experience
            extraction model is aligned with the inference model. Methods with ‡ mean that <strong>GLM-4.6</strong>
            is used for experience extraction, while inference still relies on the original model.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Figure 3: Analysis (Comprehensive)
st.markdown("### Figure 3: Comprehensive Analysis")
col_left, col_img, col_right = st.columns([1, 2, 1])
with col_img:
    st.image(os.path.join(skillx_dir, "analysis.png"))
st.markdown(
    """
    <div class="figure-caption-wrapper">
        <div class="figure-caption">
            <strong>Figure 3.</strong> Comprehensive Analysis of SkillX.
            <strong>(a)</strong> Performance of Multi-skills.
            <strong>(b)</strong> Execution efficiency.
            <strong>(c)</strong> Iterative optimization.
            <strong>(d)</strong> Skill expansion strategies.
            <strong>(e)</strong> Analysis of Input tokens.
            <strong>(f)</strong> Analysis of Execution steps.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Further Analysis: Table 2 & Table 3 stacked and centered
st.markdown("### Further Analysis")

# Table 2
st.markdown("**Table 2: Performance on Other Base Models**")
_, col_img, _ = st.columns([1.8, 2, 1.2])
with col_img:
    st.image(os.path.join(skillx_dir, "othermodels.png"))
st.markdown(
    """
    <div class="figure-caption-wrapper">
        <div class="figure-caption">
            Performance of SkillX on other base models (<strong>DeepSeek-V3.2</strong>, <strong>GPT-4.1</strong>).
            SkillX provides consistent performance gains.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Table 3
st.markdown("**Table 3: Ablation Study**")
_, col_img, _ = st.columns([1.7, 2, 1.3])
with col_img:
    st.image(os.path.join(skillx_dir, "ablation.png"))
st.markdown(
    """
    <div class="figure-caption-wrapper">
        <div class="figure-caption">
            Ablation results on three components. <strong>Vanilla-Iter1</strong> uses only multi-level skills design;
            <strong>Expand-Iter3</strong> combines all three components.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 8. Conclusion
st.markdown("## 📝 Conclusion")
st.markdown(
    """
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px;">
        <p style="font-size: 1rem; line-height: 1.8; color: #333; margin: 0;">
            SkillX introduces a fully automated framework for building a <strong>plug-and-play skill library</strong>
            for LLM-based agents. The multi-level skills design (planning, functional, and atomic skills) enables
            efficient experience transfer across agents and environments. Experimental results demonstrate that
            SkillX transfers effectively to other models and provides significant advantages in experience representation.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 9. Citation
st.markdown("## 📚 Citation")
st.code("""@article{wang2026skillx,
  author     = {Chenxi Wang and 
                Zhuoyun Yu and 
                Xin Xie and 
                Wuguannan Yao and 
                Runnan Fang and 
                Shuofei Qiao and 
                Kexin Cao and 
                Guozhou Zheng and 
                Xiang Qi and 
                Peng Zhang and 
                Shumin Deng},
  title      = {SkillX: Automatically Constructing Skill Knowledge Bases for Agents},
  year       = {2026},
  eprint     = {2604.04804},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL},
  url        = {https://arxiv.org/abs/2604.04804}
}""", language="bibtex")

st.markdown("---")

# 10. Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <p style="font-size: 1rem;">
        🔗 <a href="https://github.com/zjunlp/SkillX" style="color: #667eea; text-decoration: none;">GitHub Repository</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        📄 <a href="https://arxiv.org/abs/2604.04804" style="color: #667eea; text-decoration: none;">arXiv Paper</a>
    </p>
    <p style="font-size: 0.9rem; margin-top: 1rem; color: #888;">
        © 2026 Zhejiang University & Ant Group
    </p>
</div>
""", unsafe_allow_html=True)
