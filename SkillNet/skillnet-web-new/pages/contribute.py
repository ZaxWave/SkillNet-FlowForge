import streamlit as st
import json
import os
import zipfile
import shutil
import uuid
from datetime import datetime
from utils import render_navbar 

# ==========================================
# 0. 初始化配置与目录
# ==========================================
UPLOAD_DIR = "uploaded_skills"
TEMP_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# 1. 页面配置
st.set_page_config(
    page_title="Contribute Skill - SkillNet",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏侧边栏
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

# ==========================================
# 2. 核心逻辑函数
# ==========================================
def save_submission(data, filename="submitted_skills.jsonl"):
    """将提交的数据追加到本地 JSONL 文件"""
    try:
        data["submission_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

def verify_and_save_local_skill(extract_path, skill_name, author, category, contact_email):
    """校验单个本地 Skill 文件夹并保存"""
    # 查找是否有 SKILL.md (处理有些 zip 直接打包文件，有些打包了外层文件夹的情况)
    skill_md_path = None
    skill_folder = extract_path
    
    for root, dirs, files in os.walk(extract_path):
        if "SKILL.md" in files:
            skill_md_path = os.path.join(root, "SKILL.md")
            skill_folder = root
            break
            
    if not skill_md_path:
        return False, "No `SKILL.md` found in the uploaded zip."

    # 将有效的 skill 移动到最终的存储目录
    final_skill_path = os.path.join(UPLOAD_DIR, authorslug := author.replace(" ", "_"), f"{skill_name}")
    os.makedirs(os.path.dirname(final_skill_path), exist_ok=True)
    shutil.copytree(skill_folder, final_skill_path)

    submission_data = {
        "skill_name": skill_name,
        "category": category,
        "author": author,
        "contact_email": contact_email,
        "skill_url": f"local://{final_skill_path}", # 用 local:// 标识这是本地存储
        "is_local": True
    }
    
    if save_submission(submission_data):
        return True, "Skill uploaded and saved successfully!"
    return False, "Failed to save submission records."

def process_batch_skills(extract_path, author, contact_email):
    """处理批量上传的 Skills"""
    success_count = 0
    failed_folders = []

    # 遍历解压后的第一层或第二层目录寻找 skill 文件夹
    for root, dirs, files in os.walk(extract_path):
        if "SKILL.md" in files:
            skill_name = os.path.basename(root) # 使用文件夹名字作为 Skill Name
            final_skill_path = os.path.join(UPLOAD_DIR, authorslug := author.replace(" ", "_"), skill_name)
            os.makedirs(os.path.dirname(final_skill_path), exist_ok=True)
            shutil.copytree(root, final_skill_path)
            
            submission_data = {
                "skill_name": skill_name,
                # "skill_description": "Batch Local Skill Upload",
                "author": author,
                "contact_email": contact_email,
                "skill_url": f"local://{final_skill_path}",
                "is_local": True
            }
            if save_submission(submission_data):
                success_count += 1
            # 停止向下遍历此文件夹的子文件夹
            dirs.clear() 

    if success_count > 0:
        return True, f"Successfully processed {success_count} skills!"
    else:
        return False, "Could not find any valid skill folders (missing SKILL.md)."


# 3. 渲染导航栏
render_navbar()

# ==========================================
# 4. 页面表单 UI
# ==========================================
_, col_form, _ = st.columns([1, 2, 1])

with col_form:
    st.title("📤 Submit a Skill")
    st.info("Contributions are welcome! Choose how you want to submit your skill below.")

    # 使用 Tabs 分离三种上传方式
    tab_url, tab_single, tab_batch = st.tabs([
        "🔗 Submit via URL", 
        "📁 Upload Local Skill", 
        "📚 Batch Upload Skills"
    ])

    # -----------------------------------------
    # Tab 1: 原有的 URL 提交方式
    # -----------------------------------------
    with tab_url:
        with st.form("url_submit_form", clear_on_submit=True):
            skill_name = st.text_input("Skill Name *", placeholder="e.g. contextual-pattern-learning")
            skill_description = st.text_area("Skill Description *", placeholder="What does this skill do?", height=120)
            skill_url = st.text_input("Skill URL *", placeholder="e.g. https://github.com/anthropics/skills/tree/main...")
            category = st.selectbox("Category", ["Development", "AIGC", "Research", "Science", "Business", "Testing", "Productivity", "Security", "Lifestyle", "Other"], key="cat1")
            
            c1, c2 = st.columns(2)
            with c1: author = st.text_input("Author / Organization", placeholder="e.g. your_github_username", key="auth1")
            with c2: contact_email = st.text_input("Contact Email", placeholder="name@example.com", key="mail1")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted_url = st.form_submit_button("Submit Link", type="primary", use_container_width=True)

            if submitted_url:
                if not skill_name or not skill_url or not skill_description:
                    st.warning("Please fill in at least the **Skill Name**, **Skill Description** and **Skill URL**.")
                else:
                    submission_data = {
                        "skill_name": skill_name, "category": category, 
                        "skill_description": skill_description, "author": author, 
                        "contact_email": contact_email, "skill_url": skill_url, "is_local": False
                    }
                    if save_submission(submission_data):
                        st.success("🎉 Link submission received! Thank you.")
                        st.balloons()

    # -----------------------------------------
    # Tab 2: 单个本地 Skill 上传 (ZIP)
    # -----------------------------------------
    with tab_single:
        st.markdown("**Upload a `.zip` file** of your skill. The folder inside must contain a `SKILL.md` file.")
        with st.form("single_upload_form", clear_on_submit=True):
            skill_name_local = st.text_input("Skill Name *", placeholder="e.g. my-local-skill")
            category_local = st.selectbox("Category", ["Development", "AIGC", "Research", "Science", "Business", "Testing", "Productivity", "Security", "Lifestyle", "Other"], key="cat2")
            
            c1, c2 = st.columns(2)
            with c1: author_local = st.text_input("Author / Organization *", key="auth2")
            with c2: email_local = st.text_input("Contact Email", key="mail2")
            
            uploaded_file = st.file_uploader("Upload Skill Folder (ZIP format) *", type=["zip"], key="file_single")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted_single = st.form_submit_button("Upload Skill", type="primary", use_container_width=True)

            if submitted_single:
                if not skill_name_local or not uploaded_file or not author_local:
                    st.warning("Please fill in the required fields (*) and upload a ZIP file containing your skill.")              
                else:
                    # 创建临时解压目录
                    temp_extract_dir = os.path.join(TEMP_DIR, uuid.uuid4().hex)
                    os.makedirs(temp_extract_dir, exist_ok=True)
                    
                    try:
                        # 解压文件
                        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                            zip_ref.extractall(temp_extract_dir)
                        
                        # 校验并保存
                        success, msg = verify_and_save_local_skill(
                            temp_extract_dir, skill_name_local, author_local, category_local, email_local
                        )
                        
                        if success:
                            st.success(f"🎉 {msg}")
                            st.balloons()
                        else:
                            st.error(f"❌ {msg}")
                    except Exception as e:
                        st.error(f"Error processing zip file: {e}")
                    finally:
                        # 清理临时目录
                        if os.path.exists(temp_extract_dir):
                            shutil.rmtree(temp_extract_dir)

    # -----------------------------------------
    # Tab 3: 批量上传 (ZIP)
    # -----------------------------------------
    with tab_batch:
        st.markdown("**Batch Upload:** Upload a `.zip` containing **multiple skill folders**. We will use the folder names as the Skill Names.")
        with st.form("batch_upload_form", clear_on_submit=True):
            
            c1, c2 = st.columns(2)
            with c1: author_batch = st.text_input("Author / Organization *", key="auth3")
            with c2: email_batch = st.text_input("Contact Email", key="mail3")
            
            uploaded_batch_file = st.file_uploader("Upload Batch Folders (ZIP format) *", type=["zip"], key="file_batch")

            st.markdown("<br>", unsafe_allow_html=True)
            submitted_batch = st.form_submit_button("Upload Batch", type="primary", use_container_width=True)

            if submitted_batch:
                if not uploaded_batch_file or not author_batch:
                    st.warning("Please fill in the required fields (*) and upload a ZIP file containing your skill folders.")
                
                else:
                    temp_extract_dir = os.path.join(TEMP_DIR, uuid.uuid4().hex)
                    os.makedirs(temp_extract_dir, exist_ok=True)
                    
                    try:
                        with zipfile.ZipFile(uploaded_batch_file, 'r') as zip_ref:
                            zip_ref.extractall(temp_extract_dir)
                        
                        success, msg = process_batch_skills(
                            temp_extract_dir, author_batch, email_batch
                        )
                        
                        if success:
                            st.success(f"🎉 {msg}")
                            st.balloons()
                        else:
                            st.error(f"❌ {msg}")
                    except Exception as e:
                        st.error(f"Error processing zip file: {e}")
                    finally:
                        if os.path.exists(temp_extract_dir):
                            shutil.rmtree(temp_extract_dir)