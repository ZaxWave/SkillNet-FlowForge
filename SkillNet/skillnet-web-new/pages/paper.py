import streamlit as st
import os
from utils import render_navbar
from streamlit_pdf_viewer import pdf_viewer  # 引入新组件

# 1. 页面配置
st.set_page_config(
    page_title="Paper - SkillNet",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏默认侧边栏
st.markdown(
    """
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
        h1, h2, h3 { scroll-margin-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 渲染导航栏
render_navbar()

st.title("📄 SkillNet Technical Report")
st.markdown("Read our comprehensive technical report on creating, evaluating, and connecting AI skills.")

# 3. 获取 PDF 文件的绝对路径
pdf_path = os.path.join(os.path.dirname(__file__), "SkillNet_report.pdf")

try:
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # # 下载按钮
    # st.download_button(
    #     label="📥 Download PDF",
    #     data=pdf_bytes,
    #     file_name="SkillNet_Technical_Report.pdf",
    #     mime="application/pdf"
    # )
    col1, col2, col3 = st.columns([1, 1, 6])  # 调整列宽，第三列占更多空间

    with col1:
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name="SkillNet_Technical_Report.pdf",
            mime="application/pdf"
        )
        
    with col2:
        # 使用 link_button 直接跳转到 arXiv
        st.link_button(
            label="🔗 View on arXiv", 
            url="https://arxiv.org/abs/2603.04448"
        )
        
    st.markdown("---")

    # 4. 直接渲染 PDF (不用转 Base64，不用写 HTML)
    # width 设置为 1000 或其他数值来适配你的网页宽度
    pdf_viewer(pdf_path, width=800, height=1000)

except FileNotFoundError:
    st.error(f"Error: Could not find the PDF file at {pdf_path}.")