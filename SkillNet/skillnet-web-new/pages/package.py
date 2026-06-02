# # pages/package.py
# import streamlit as st
# from utils import render_navbar, render_logos, increment_download
# import json
# import os
# import io
# import zipfile
# import html as html_mod
# from pathlib import Path

# # ============================================================
# # 1. 页面配置
# # ============================================================
# st.set_page_config(
#     page_title="Packages - SkillNet",
#     page_icon="📦",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )
# st.markdown(
#     """<style>[data-testid="stSidebar"],[data-testid="stSidebarNav"]{display:none;}</style>""",
#     unsafe_allow_html=True,
# )

# # ============================================================
# # 路径配置
# # ============================================================
# BASE_DIR = Path(__file__).parent.parent  # skillnet-web-new/
# PACKAGES_DIR = BASE_DIR / "data" / "packages"
# DOWNLOADED_SKILLS_DIR = BASE_DIR / "data" / "downloaded_package_skills"

# # ============================================================
# # 分类映射
# # ============================================================
# CATEGORY_MAP = {
#     "react-nextjs-fullstack": "Development",
#     "frontend-ui-engineering": "Development",
#     "typescript-node-backend": "Development",
#     "rust-systems-programming": "Development",
#     "database-design-management": "Development",
#     "mobile-cross-platform": "Development",
#     "code-quality-refactoring": "Development",
#     "git-workflow-collaboration": "Development",
#     "ai-agent-building": "AIGC",
#     "llm-app-development": "AIGC",
#     "prompt-engineering-optimization": "AIGC",
#     "ai-audio-speech": "AIGC",
#     "bioinformatics-compbio": "Science",
#     "cheminformatics-drug-design": "Science",
#     "data-science-visualization": "Research",
#     "ml-model-pipeline": "Research",
#     "e2e-browser-testing": "Testing",
#     "devops-cicd-pipeline": "Productivity",
#     "cloud-infrastructure-iac": "Productivity",
#     "technical-documentation": "Productivity",
#     "security-audit-compliance": "Security",
#     "alfworld": "Benchmark",
#     "scienceworld": "Benchmark",
#     "toolathlon": "Benchmark",
#     "webshop": "Benchmark",
# }

# CATEGORY_ORDER = [
#     "Development", "AIGC", "Research", "Science",
#     "Testing", "Productivity", "Security",
# ]

# RELATION_COLORS = {
#     "belong_to": "#059669",
#     "compose_with": "#2563eb",
#     "similar_to": "#d97706",
#     "depend_on": "#dc2626",
# }
# RELATION_LABELS = {
#     "belong_to": "Belong To",
#     "compose_with": "Compose With",
#     "similar_to": "Similar To",
#     "depend_on": "Depend On",
# }

# # ============================================================
# # 数据加载
# # ============================================================
# @st.cache_data(ttl=3600)
# def load_all_packages():
#     packages = []
#     if not PACKAGES_DIR.exists():
#         return packages
#     for f in sorted(PACKAGES_DIR.glob("*.json")):
#         if f.name == "packages_index.json":
#             continue
#         try:
#             data = json.loads(f.read_text(encoding="utf-8"))
#             pkg_name = data.get("package_name", f.stem)
#             data["category"] = CATEGORY_MAP.get(pkg_name, "Other")
#             packages.append(data)
#         except Exception:
#             continue
#     return packages


# def create_package_zip(package_name: str) -> bytes | None:
#     pkg_dir = DOWNLOADED_SKILLS_DIR / package_name
#     pkg_json = PACKAGES_DIR / f"{package_name}.json"
#     buf = io.BytesIO()
#     with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
#         if pkg_json.exists():
#             zf.write(pkg_json, f"{package_name}/package.json")
#         if pkg_dir.exists():
#             for root, _dirs, files in os.walk(pkg_dir):
#                 for file in files:
#                     fp = Path(root) / file
#                     arc = f"{package_name}/{fp.relative_to(pkg_dir)}"
#                     zf.write(fp, arc)
#     buf.seek(0)
#     return buf.getvalue()


# def build_graph_html(skills: list, relationships: list) -> str:
#     """Build vis.js interactive relationship graph HTML."""
#     skill_names = {s["skill_name"] for s in skills}
#     node_degree = {}
#     for rel in relationships:
#         s, t = rel.get("source", ""), rel.get("target", "")
#         node_degree[s] = node_degree.get(s, 0) + 1
#         node_degree[t] = node_degree.get(t, 0) + 1

#     skill_info = {
#         s["skill_name"]: {
#             "desc": s.get("skill_description", ""),
#             "stars": s.get("stars", 0),
#         }
#         for s in skills
#     }

#     PALETTE = [
#         {"bg": "#059669", "bd": "#047857"},
#         {"bg": "#2563eb", "bd": "#1d4ed8"},
#         {"bg": "#7c3aed", "bd": "#6d28d9"},
#         {"bg": "#db2777", "bd": "#be185d"},
#         {"bg": "#d97706", "bd": "#b45309"},
#         {"bg": "#0891b2", "bd": "#0e7490"},
#         {"bg": "#4f46e5", "bd": "#4338ca"},
#         {"bg": "#16a34a", "bd": "#15803d"},
#     ]

#     nodes_js = []
#     for i, name in enumerate(sorted(skill_names)):
#         info = skill_info.get(name, {})
#         deg = node_degree.get(name, 0)
#         size = 16 + deg * 5
#         p = PALETTE[i % len(PALETTE)]
#         desc_safe = info.get("desc", "")[:100].replace('"', "&quot;").replace("'", "&#39;")
#         label = name if len(name) <= 20 else name[:18] + "…"
#         nodes_js.append({
#             "id": name, "label": label, "size": size,
#             "title": f"<div style='max-width:240px;font-family:Segoe UI,sans-serif;'>"
#                      f"<b>{name}</b><br><span style='font-size:11px;color:#555;'>{desc_safe}…</span>"
#                      f"<br><span style='font-size:11px;color:#999;'>⭐ {info.get('stars',0):,}</span></div>",
#             "color": {
#                 "background": p["bg"], "border": p["bd"],
#                 "highlight": {"background": "#dc2626", "border": "#b91c1c"},
#                 "hover": {"background": p["bg"] + "DD", "border": p["bd"]},
#             },
#             "font": {"size": 12, "color": "#374151", "face": "Segoe UI,sans-serif", "strokeWidth": 3, "strokeColor": "#fff"},
#         })

#     EDGE_DASH = {"similar_to": [8, 4]}
#     edges_js = []
#     for rel in relationships:
#         rtype = rel.get("type", "unknown")
#         color = RELATION_COLORS.get(rtype, "#999")
#         reason_safe = rel.get("reason", "")[:150].replace('"', "&quot;").replace("'", "&#39;")
#         edges_js.append({
#             "from": rel.get("source", ""), "to": rel.get("target", ""),
#             "color": {"color": color + "AA", "highlight": color, "hover": color},
#             "arrows": {"to": {"enabled": rtype in ("belong_to", "depend_on"), "scaleFactor": 0.7}},
#             "dashes": EDGE_DASH.get(rtype, False),
#             "width": 2,
#             "title": f"<div style='font-family:Segoe UI;max-width:220px;'>"
#                      f"<b style='color:{color};'>{RELATION_LABELS.get(rtype,rtype)}</b><br>"
#                      f"<span style='font-size:11px;color:#666;'>{reason_safe}</span></div>",
#             "smooth": {"type": "curvedCW", "roundness": 0.15},
#         })

#     nodes_json = json.dumps(nodes_js, ensure_ascii=False)
#     edges_json = json.dumps(edges_js, ensure_ascii=False)

#     return f"""<!DOCTYPE html>
# <html><head><meta charset="utf-8">
# <script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
# <style>
# *{{margin:0;padding:0;box-sizing:border-box}}
# body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:transparent}}
# #legend{{padding:10px 16px;font-size:12px;color:#6b7280;display:flex;flex-wrap:wrap;gap:16px;align-items:center}}
# .lg-item{{display:flex;align-items:center;gap:6px}}
# .lg-line{{width:24px;height:3px;border-radius:2px}}
# .lg-line.dashed{{background:repeating-linear-gradient(90deg,currentColor 0,currentColor 6px,transparent 6px,transparent 10px);height:2px}}
# #graph{{width:100%;height:520px;border:1px solid #e5e7eb;border-radius:12px;background:linear-gradient(135deg,#f8fafb 0%,#f0f4f3 100%)}}
# #ctrls{{display:flex;gap:6px;padding:6px 16px 0;justify-content:flex-end}}
#graph:fullscreen{{width:100vw;height:100vh;border-radius:0;background:#fff}}
#graph:-webkit-full-screen{{width:100vw;height:100vh;border-radius:0;background:#fff}}
# .cbtn{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:4px 12px;font-size:13px;cursor:pointer;color:#374151;transition:all .2s}}
# .cbtn:hover{{border-color:#059669;color:#059669}}
# </style></head><body>
# <div id="legend">
#   <div class="lg-item"><div class="lg-line" style="background:#059669"></div><span>Belong To</span></div>
#   <div class="lg-item"><div class="lg-line" style="background:#2563eb"></div><span>Compose With</span></div>
#   <div class="lg-item"><div class="lg-line dashed" style="color:#d97706"></div><span>Similar To</span></div>
#   <div class="lg-item"><div class="lg-line" style="background:#dc2626"></div><span>Depend On</span></div>
# </div>
# <div id="ctrls">
#   <button class="cbtn" onclick="net.fit({{animation:true}})">⊞ Fit</button>
#   <button class="cbtn" onclick="net.moveTo({{scale:1,animation:true}})">1:1</button>
# </div>
# <div id="graph"></div>
# <script>
# var nodes=new vis.DataSet({nodes_json});
# var edges=new vis.DataSet({edges_json});
# var c=document.getElementById("graph");
# var net=new vis.Network(c,{{nodes:nodes,edges:edges}},{{
#   physics:{{solver:"forceAtlas2Based",forceAtlas2Based:{{gravitationalConstant:-55,centralGravity:0.01,springLength:190,springConstant:0.015,damping:0.5,avoidOverlap:0.8}},stabilization:{{iterations:280,fit:true}},maxVelocity:30}},
#   interaction:{{hover:true,tooltipDelay:80,zoomView:true,dragView:true,dragNodes:true}},
#   nodes:{{shape:"dot",borderWidth:4,borderWidthSelected:5,shadow:{{enabled:true,color:"rgba(0,0,0,0.22)",size:18,x:0,y:4}}}},
#   edges:{{selectionWidth:1.5,hoverWidth:1}}
# }});
# net.on("click",function(p){{if(p.nodes.length>0){{var n=p.nodes[0];net.selectNodes(net.getConnectedNodes(n).concat([n]));net.selectEdges(net.getConnectedEdges(n))}}}});
# </script></body></html>"""


# # ============================================================
# # CSS — 完全对齐 resources.py 设计系统
# # ============================================================
# PAGE_CSS = """
# <style>
#     .stApp { background-color: #f8f9fa; }

#     /* Package card */
#     .pkg-card {
#         background-color: #ffffff;
#         border-radius: 12px;
#         padding: 20px;
#         margin-bottom: 20px;
#         border: 1px solid #e5e7eb;
#         box-shadow: 0 1px 2px rgba(0,0,0,0.05);
#         transition: all 0.2s ease-in-out;
#         height: 280px;
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#         cursor: pointer;
#     }
#     .pkg-card:hover {
#         transform: translateY(-4px);
#         box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
#         border-color: #d1d5db;
#     }

#     .pkg-card .card-header {
#         display: flex;
#         justify-content: space-between;
#         align-items: start;
#         margin-bottom: 8px;
#     }
#     .pkg-title {
#         font-size: 1.05em;
#         font-weight: 700;
#         color: #111827;
#         text-decoration: none;
#         display: block;
#         overflow-wrap: break-word;
#     }
#     .pkg-title:hover { color: #059669; }
#     .pkg-desc {
#         font-size: 0.88em;
#         color: #4b5563;
#         line-height: 1.5;
#         flex-grow: 1;
#         overflow: hidden;
#         display: -webkit-box;
#         -webkit-line-clamp: 3;
#         -webkit-box-orient: vertical;
#         margin-bottom: 10px;
#     }
#     .pkg-footer {
#         border-top: 1px solid #f3f4f6;
#         padding-top: 10px;
#         font-size: 0.8em;
#         color: #6b7280;
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#     }

#     .tag {
#         display: inline-block;
#         background-color: #f3f4f6;
#         border-radius: 9999px;
#         padding: 2px 8px;
#         font-size: 0.75em;
#         margin-right: 4px;
#         margin-bottom: 4px;
#         color: #374151;
#         font-weight: 500;
#     }
#     .cat-tag {
#         background-color: #e0f2fe;
#         color: #0369a1;
#     }
#     .count-badge {
#         background-color: #ecfdf5;
#         color: #047857;
#         padding: 2px 10px;
#         border-radius: 9999px;
#         font-weight: 600;
#         font-size: 0.8em;
#         white-space: nowrap;
#     }

#     /* Green primary buttons */
#     div.stButton > button[kind="primary"] {
#         background-color: #059669;
#         border-color: #059669;
#         color: white;
#     }
#     div.stButton > button[kind="primary"]:hover {
#         background-color: #047857;
#         border-color: #047857;
#         color: white;
#     }
#     div.stButton > button[kind="primary"]:focus {
#         background-color: #059669;
#         border-color: #059669;
#         color: white;
#         box-shadow: 0 0 0 0.2rem rgba(5, 150, 105, 0.5);
#     }

#     /* Detail page */
#     .detail-banner {
#         background: #f0fdf4;
#         border: 1px solid #d1fae5;
#         border-radius: 14px;
#         padding: 28px 32px;
#         margin-bottom: 24px;
#     }
#     .detail-banner h2 {
#         margin: 0 0 8px 0;
#         font-size: 1.6rem;
#         font-weight: 800;
#         color: #111827;
#     }
#     .detail-banner p {
#         margin: 0;
#         color: #4b5563;
#         font-size: 0.95rem;
#         line-height: 1.6;
#     }
#     .detail-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
#     .detail-tag {
#         font-size: 0.78em;
#         background: #ecfdf5;
#         color: #047857;
#         padding: 3px 10px;
#         border-radius: 9999px;
#         font-weight: 500;
#     }
#     .stats-row {
#         display: flex;
#         gap: 28px;
#         margin-top: 16px;
#     }
#     .stat-box { text-align: center; }
#     .stat-val { font-size: 1.4rem; font-weight: 800; color: #059669; }
#     .stat-lbl { font-size: 0.78rem; color: #6b7280; }

#     .skill-item {
#         background: #fff;
#         border: 1px solid #e5e7eb;
#         border-radius: 10px;
#         padding: 14px 18px;
#         margin-bottom: 10px;
#         transition: border-color 0.2s;
#     }
#     .skill-item:hover { border-color: #059669; }
#     .skill-item-name { font-weight: 600; font-size: 0.9em; color: #111827; }
#     .skill-item-name a { text-decoration: none; color: #111827; }
#     .skill-item-name a:hover { color: #059669; }
#     .skill-item-desc { font-size: 0.82em; color: #4b5563; margin-top: 4px; line-height: 1.4; }
#     .skill-item-meta { font-size: 0.75em; color: #9ca3af; margin-top: 6px; }

#     /* Section Headers */
#     .section-header {
#         font-size: 1.15rem;
#         font-weight: 700;
#         color: #111827;
#         margin-bottom: 16px;
#         padding-bottom: 8px;
#         border-bottom: 2px solid #d1fae5;
#         display: inline-block;
#     }
# </style>
# """


# # ============================================================
# # Main
# # ============================================================
# def main():
#     render_navbar()
#     st.markdown(PAGE_CSS, unsafe_allow_html=True)

#     all_packages = load_all_packages()
#     params = st.query_params
#     selected_pkg = params.get("pkg", None)

#     if selected_pkg:
#         render_detail_page(all_packages, selected_pkg)
#     else:
#         render_overview_page(all_packages)


# # ============================================================
# # Overview Page
# # ============================================================
# def render_overview_page(all_packages):
#     total_skills = sum(p.get("skill_count", len(p.get("skills", []))) for p in all_packages)

#     # Hero
#     st.markdown(
#         "<h1 style='text-align:center; margin-bottom:0; font-size:48px;'>Skill Library</h1>",
#         unsafe_allow_html=True,
#     )
#     st.markdown(
#         "<p style='text-align:center; color:#6b7280; font-size:18px; max-width:700px; margin:8px auto 0;'>"
#         "Pre-built collections of curated skills for real-world scenarios, "
#         "each with a relationship graph showing how skills connect.</p>",
#         unsafe_allow_html=True,
#     )

#     # Counter badges
#     st.markdown(f"""
#     <div style="text-align:center; margin: 16px 0 8px;">
#         <span style="color:#047857;background:#ecfdf5;padding:6px 16px;border-radius:99px;font-size:0.95em;
#               display:inline-flex;align-items:center;border:1px solid #d1fae5;box-shadow:0 1px 2px rgba(0,0,0,0.05);">
#             <span style="margin-right:6px;">{icon("package", 14, "#047857")}</span>
#             <span style="font-weight:800;font-size:1.05em;">{len(all_packages)}</span>
#             <span style="font-weight:500;opacity:0.65;margin-left:4px;">Packages</span>
#             <span style="margin:0 8px;color:#a7f3d0;font-weight:300;">|</span>
#             <span style="font-weight:800;font-size:1.05em;">{total_skills}</span>
#             <span style="font-weight:500;opacity:0.65;margin-left:4px;">Total Skills</span>
#         </span>
#     </div>
#     """, unsafe_allow_html=True)

#     st.divider()

#     N_COLS = 4

#     for row_start in range(0, len(all_packages), N_COLS):
#         cols = st.columns(N_COLS)
#         for col_idx, col in enumerate(cols):
#             idx = row_start + col_idx
#             if idx >= len(all_packages):
#                 break
#             pkg = all_packages[idx]
#             pkg_name = pkg.get("package_name", "")
#             desc = html_mod.escape(pkg.get("scene_description", ""))
#             skill_count = pkg.get("skill_count", len(pkg.get("skills", [])))
#             tags = pkg.get("tags", [])[:4]
#             tags_html = "".join(
#                 f'<span class="tag">{html_mod.escape(t)}</span>' for t in tags
#             )

#             with col:
#                 st.markdown(f"""
#                 <a href="?pkg={pkg_name}" target="_self" style="text-decoration:none;">
#                 <div class="pkg-card">
#                     <div>
#                         <div class="card-header">
#                             <span class="pkg-title">{pkg_name}</span>
#                             <span class="count-badge">{icon("book-open", 14, "#6b7280")} {skill_count}</span>
#                         </div>
#                         <div class="pkg-desc">{desc}</div>
#                         <div>
#                             <span class="tag cat-tag">{pkg.get('category','')}</span>
#                             {tags_html}
#                         </div>
#                     </div>
#                     <div class="pkg-footer">
#                         <div>{icon("link", 14, "#6b7280")} {skill_count} skills</div>
#                         <span style="color:#059669; font-weight:600;">View Details →</span>
#                     </div>
#                 </div>
#                 </a>
#                 """, unsafe_allow_html=True)

#     # render_logos()


# # ============================================================
# # Detail Page
# # ============================================================
# def render_detail_page(all_packages, selected_pkg):
#     pkg_data = None
#     for p in all_packages:
#         if p.get("package_name") == selected_pkg:
#             pkg_data = p
#             break

#     if pkg_data is None:
#         st.error(f"Package '{selected_pkg}' not found.")
#         st.stop()

#     # Back button
#     if st.button("← Back to Packages", type="primary"):
#         st.query_params.clear()
#         st.rerun()

#     skills = pkg_data.get("skills", [])
#     relationships = pkg_data.get("relationships", [])
#     total_stars = sum(s.get("stars", 0) for s in skills)

#     # Banner
#     tags_html = "".join(f'<span class="detail-tag">{html_mod.escape(t)}</span>' for t in pkg_data.get("tags", []))
#     st.markdown(f"""
#     <div class="detail-banner">
#         <h2>📦 {pkg_data['package_name']}</h2>
#         <p>{html_mod.escape(pkg_data.get('scene_description', ''))}</p>
#         <div class="detail-tags">{tags_html}</div>
#         <div class="stats-row">
#             <div class="stat-box"><div class="stat-val">{len(skills)}</div><div class="stat-lbl">Skills</div></div>
#             <div class="stat-box"><div class="stat-val">{len(relationships)}</div><div class="stat-lbl">Relations</div></div>
#             <div class="stat-box"><div class="stat-val">{total_stars:,}</div><div class="stat-lbl">Total {icon("star", 14, "#d97706")}</div></div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Download button
#     zip_bytes = create_package_zip(selected_pkg)
#     if zip_bytes:
#         st.download_button(
#             label=f"⬇️  Download Package ({len(skills)} skills)",
#             data=zip_bytes,
#             file_name=f"{selected_pkg}.zip",
#             mime="application/zip",
#             use_container_width=True,
#             on_click=lambda: increment_download(len(skills))
#         )

#     # Two columns: skills list | relationship graph
#     col_left, col_right = st.columns([2, 3])

#     with col_left:
#         st.markdown("<div class='section-header'>📋 Skills in this Package</div>", unsafe_allow_html=True)
#         for idx, s in enumerate(skills, 1):
#             s_name = html_mod.escape(s.get("skill_name", ""))
#             s_desc = html_mod.escape(s.get("skill_description", ""))
#             s_desc_short = s_desc[:180] + ("…" if len(s_desc) > 180 else "")
#             s_url = s.get("skill_url", "#")
#             s_stars = s.get("stars", 0)
#             s_cat = html_mod.escape(s.get("category", ""))
#             s_tags = "".join(f'<span class="tag">{html_mod.escape(t)}</span>' for t in s.get("tags", [])[:3])
#             st.markdown(f"""
#             <div class="skill-item">
#                 <div class="skill-item-name">
#                     {idx}. <a href="{s_url}" target="_blank">{s_name}</a>
#                 </div>
#                 <div class="skill-item-desc">{s_desc_short}</div>
#                 <div class="skill-item-meta">
#                     {icon("star", 14, "#d97706")} {s_stars:,} &nbsp;|&nbsp; {s_cat} &nbsp;|&nbsp; {s_tags}
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#     with col_right:
#         st.markdown("<div class='section-header'>🕸️ Skill Knowledge Graph</div>", unsafe_allow_html=True)
#         if relationships:
#             graph_html = build_graph_html(skills, relationships)
#         else:
#             st.info("No relationship data available for this package.")

#         if relationships:
#             with st.expander(f"📊 View all {len(relationships)} relationships"):
#                 for rel in relationships:
#                     rtype = rel.get("type", "unknown")
#                     color = RELATION_COLORS.get(rtype, "#999")
#                     st.markdown(
#                         f'<span style="color:{color};font-weight:600;">[{RELATION_LABELS.get(rtype, rtype)}]</span> '
#                         f'**{rel["source"]}** → **{rel["target"]}**  \n'
#                         f'<small style="color:#9ca3af;">{rel.get("reason", "")}</small>',
#                         unsafe_allow_html=True,
#                     )
#                     st.markdown("---")


# if __name__ == "__main__":
#     main()



# pages/library.py
import streamlit as st
import streamlit.components.v1 as components
from utils import render_navbar, increment_download
from icon_helper import icon
import json
import os
import io
import zipfile
import html as html_mod
from pathlib import Path


def render_html_embed(html_content, height):
    if hasattr(st, "iframe"):
        st.iframe(html_content, height=height)
    else:
        components.html(html_content, height=height, scrolling=False)


# ============================================================
# 1. 页面配置
# ============================================================
st.set_page_config(
    page_title="Skill Collection - SkillNet",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(
    """<style>[data-testid="stSidebar"],[data-testid="stSidebarNav"]{display:none;}</style>""",
    unsafe_allow_html=True,
)

# ============================================================
# 路径配置
# ============================================================
BASE_DIR = Path(__file__).parent.parent  # skillnet-web-new/
PACKAGES_DIR = BASE_DIR / "data" / "packages"
DOWNLOADED_SKILLS_DIR = BASE_DIR / "data" / "downloaded_package_skills"

# ============================================================
# 分类映射
# ============================================================
CATEGORY_MAP = {
    "react-nextjs-fullstack": "Development",
    "frontend-ui-engineering": "Development",
    "typescript-node-backend": "Development",
    "rust-systems-programming": "Development",
    "database-design-management": "Development",
    "mobile-cross-platform": "Development",
    "code-quality-refactoring": "Development",
    "git-workflow-collaboration": "Development",
    "ai-agent-building": "AIGC",
    "llm-app-development": "AIGC",
    "prompt-engineering-optimization": "AIGC",
    "ai-audio-speech": "AIGC",
    "bioinformatics-compbio": "Science",
    "cheminformatics-drug-design": "Science",
    "data-science-visualization": "Research",
    "ml-model-pipeline": "Research",
    "e2e-browser-testing": "Testing",
    "devops-cicd-pipeline": "Productivity",
    "cloud-infrastructure-iac": "Productivity",
    "technical-documentation": "Productivity",
    "security-audit-compliance": "Security",
    "alfworld": "Benchmark",
    "scienceworld": "Benchmark",
    "toolathlon": "Benchmark",
    "webshop": "Benchmark",
}

CATEGORY_ORDER = [
    "Development", "AIGC", "Research", "Science",
    "Benchmark", "Testing", "Productivity", "Security",
]

RELATION_COLORS = {
    "belong_to": "#059669",
    "compose_with": "#2563eb",
    "similar_to": "#d97706",
    "depend_on": "#dc2626",
    "contain": "#8b5cf6",
}
RELATION_LABELS = {
    "belong_to": "Belong To",
    "compose_with": "Compose With",
    "similar_to": "Similar To",
    "depend_on": "Depend On",
    "contain": "Contain",
}

# ============================================================
# 数据加载
# ============================================================
@st.cache_data(ttl=3600)
def load_all_packages():
    packages = []
    if not PACKAGES_DIR.exists():
        return packages
    for f in sorted(PACKAGES_DIR.glob("*.json")):
        if f.name == "packages_index.json":
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            pkg_name = data.get("package_name", f.stem)
            data["category"] = CATEGORY_MAP.get(pkg_name, "Other")
            packages.append(data)
        except Exception:
            continue
    return packages


def create_package_zip(package_name: str) -> bytes | None:
    pkg_dir = DOWNLOADED_SKILLS_DIR / package_name
    pkg_json = PACKAGES_DIR / f"{package_name}.json"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        if pkg_json.exists():
            zf.write(pkg_json, f"{package_name}/package.json")
        if pkg_dir.exists():
            for root, _dirs, files in os.walk(pkg_dir):
                for file in files:
                    fp = Path(root) / file
                    arc = f"{package_name}/{fp.relative_to(pkg_dir)}"
                    zf.write(fp, arc)
    buf.seek(0)
    return buf.getvalue()


def build_graph_html(skills: list, relationships: list, package_name: str = "") -> str:
    """Build vis.js interactive relationship graph with category coloring & bidirectional linking."""
    skill_names = {s["skill_name"] for s in skills}
    node_degree = {}
    for rel in relationships:
        s, t = rel.get("source", ""), rel.get("target", "")
        node_degree[s] = node_degree.get(s, 0) + 1
        node_degree[t] = node_degree.get(t, 0) + 1
    if package_name:
        node_degree[package_name] = len(skill_names)

    # ── Category → Color (bg + lighter border for glow rim) ──
    CATEGORY_PALETTE = {
        "Development":    {"bg": "#2563eb", "bd": "#60a5fa"},
        "AIGC":           {"bg": "#7c3aed", "bd": "#a78bfa"},
        "Science":        {"bg": "#059669", "bd": "#34d399"},
        "Business":       {"bg": "#d97706", "bd": "#fbbf24"},
        "Security":       {"bg": "#dc2626", "bd": "#f87171"},
        "Productivity":   {"bg": "#0891b2", "bd": "#22d3ee"},
        "Testing":        {"bg": "#4f46e5", "bd": "#818cf8"},
        "Research":       {"bg": "#db2777", "bd": "#f472b6"},
        "Lifestyle":      {"bg": "#16a34a", "bd": "#4ade80"},
        "Documentation":  {"bg": "#ea580c", "bd": "#fb923c"},
        "Data & Research": {"bg": "#9333ea", "bd": "#c084fc"},
        "Other":          {"bg": "#6b7280", "bd": "#9ca3af"},
    }

    skill_info = {
        s["skill_name"]: {
            "desc": s.get("skill_description", ""),
            "stars": s.get("stars", 0),
            "category": s.get("category", "Other"),
        }
        for s in skills
    }

    nodes_js = []
    if package_name:
        pkg_label = package_name if len(package_name) <= 22 else package_name[:20] + "…"
        nodes_js.append({
            "id": package_name, "label": pkg_label, "size": 34,
            "title": "<b>" + package_name + "</b><br>Package",
            "color": {
                "background": "#8b5cf6", "border": "#7c3aed",
                "highlight": {"background": "#fbbf24", "border": "#f59e0b"},"selected": {"background": "#fbbf24", "border": "#f59e0b"},
                "hover": {"background": "#a78bfa", "border": "#7c3aed"},
            },
            "font": {"size": 14, "color": "#1f2937", "face": "Segoe UI,sans-serif", "strokeWidth": 3, "strokeColor": "#fff", "bold": True},
            "shape": "dot",
        })

    for name in sorted(skill_names):
        info = skill_info.get(name, {})
        deg = node_degree.get(name, 0)
        size = 20 + deg * 5  # slightly larger base for glow border
        cat = info.get("category", "Other")
        p = CATEGORY_PALETTE.get(cat, CATEGORY_PALETTE["Other"])
        label = name if len(name) <= 22 else name[:20] + "…"
        stars = info.get("stars", 0)
        desc_preview = info.get("desc", "")[:120].replace('"', "&quot;").replace("'", "&#39;")
        nodes_js.append({
            "id": name, "label": label, "size": size,
            "title": f"<b>{html_mod.escape(name)}</b><br>⭐ {stars:,} &nbsp;|&nbsp; {cat}<br><small>{html_mod.escape(desc_preview)}</small>",
            "borderWidth": 4,
            "color": {
                "background": p["bg"], "border": p["bd"],
                "highlight": {"background": "#fbbf24", "border": "#f59e0b"},"selected": {"background": "#fbbf24", "border": "#f59e0b"},
                "hover": {"background": p["bg"], "border": "#ffffff"},
            },
            "font": {"size": 12, "color": "#374151", "face": "Segoe UI,sans-serif", "strokeWidth": 3, "strokeColor": "#fff"},
        })

    EDGE_DASH = {"similar_to": [8, 4]}
    edges_js = []
    # Contain edges: solid, lighter purple, thinner than inter-skill edges
    if package_name:
        for skill_name in skill_names:
            edges_js.append({
                "from": package_name, "to": skill_name,
                "color": {"color": "#c4b5fd", "highlight": "#a78bfa", "hover": "#8b5cf6"},
                "arrows": {"to": {"enabled": True, "scaleFactor": 0.35}},
                "dashes": False,
                "width": 1,
                "title": "Contain",
                "smooth": {"type": "continuous"},
            })

    for rel in relationships:
        rtype = rel.get("type", "unknown")
        color = RELATION_COLORS.get(rtype, "#999")
        edges_js.append({
            "from": rel.get("source", ""), "to": rel.get("target", ""),
            "color": {"color": color + "AA", "highlight": color, "hover": color},
            "arrows": {"to": {"enabled": rtype in ("belong_to", "depend_on"), "scaleFactor": 0.7}},
            "dashes": EDGE_DASH.get(rtype, False),
            "width": 2.5 if rtype == "compose_with" else 2,
            "title": RELATION_LABELS.get(rtype, rtype),
            "smooth": {"type": "curvedCW", "roundness": 0.15},
        })

    nodes_json = json.dumps(nodes_js, ensure_ascii=False)
    edges_json = json.dumps(edges_js, ensure_ascii=False)
    pkg_safe = package_name.replace("'", "\\'").replace('"', "&quot;")

    # Collect unique categories for legend
    cats_seen = {}
    for s in skills:
        c = s.get("category", "Other")
        if c not in cats_seen:
            cp = CATEGORY_PALETTE.get(c, CATEGORY_PALETTE["Other"])
            cats_seen[c] = cp["bg"]

    cat_legend = "".join(
        f'<span style="display:inline-flex;align-items:center;gap:4px;margin-right:12px;"><span class="cat-dot" style="background:{bg}"></span>{html_mod.escape(c)}</span>'
        for c, bg in sorted(cats_seen.items())
    )

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{
	font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
	background:transparent;
	overflow:hidden;
}}
#wrapper{{
	display:flex;flex-direction:column;height:100vh;
}}
#legend{{
	flex-shrink:0;
	padding:8px 16px 4px;font-size:12px;color:#5b5d6b;
	display:flex;flex-wrap:wrap;gap:16px;align-items:center;
}}
.lg-item{{display:flex;align-items:center;gap:5px;font-weight:500}}
.lg-line{{width:22px;height:3px;border-radius:3px}}
.lg-line.dashed{{background:repeating-linear-gradient(90deg,currentColor 0,currentColor 6px,transparent 6px,transparent 10px);height:2.5px}}
#bottom-bar{{
	flex-shrink:0;
	display:flex;align-items:center;justify-content:space-between;
	padding:4px 16px 6px;
}}
#cat-legend{{font-size:11px;color:#6b7280;line-height:1.8}}
.cat-dot{{width:10px;height:10px;border-radius:50%;display:inline-block;border:1px solid rgba(0,0,0,0.10);box-shadow:0 0 4px rgba(0,0,0,0.08)}}
#graph{{
	flex:1;width:100%;position:relative;overflow:hidden;
	border:1px solid rgba(255,255,255,0.55);
	border-radius:16px;
	background:
		radial-gradient(ellipse at 30% 20%, rgba(147,197,253,0.18) 0%, transparent 50%),
		radial-gradient(ellipse at 70% 60%, rgba(196,181,253,0.15) 0%, transparent 50%),
		radial-gradient(ellipse at 50% 80%, rgba(167,243,208,0.12) 0%, transparent 45%),
		rgba(255,255,255,0.12);
	box-shadow:
		0 4px 24px rgba(0,0,0,0.04),
		inset 0 1px 0 rgba(255,255,255,0.5);
	backdrop-filter:blur(4px);
	-webkit-backdrop-filter:blur(4px);
}}
/* glass sheen overlay */
#graph::after{{
	content:"";position:absolute;inset:0;z-index:10;pointer-events:none;border-radius:16px;
	background:linear-gradient(135deg,rgba(255,255,255,0.08) 0%,transparent 40%,transparent 70%,rgba(255,255,255,0.04) 100%);
}}
#ctrls{{display:flex;gap:8px}}
.cbtn{{
	background:transparent;
	border:1px solid #e5e7eb;
	border-radius:8px;padding:4px 12px;font-size:12px;cursor:pointer;color:#6b7280;
	font-weight:500;transition:all .2s;
}}
.cbtn:hover{{border-color:#7c3aed;color:#7c3aed;background:rgba(139,92,246,0.06)}}
</style></head><body>
<div id="wrapper">
<div id="legend">
  <div class="lg-item"><div class="lg-line" style="background:#c4b5fd"></div><span>Contain</span></div>
  <div class="lg-item"><div class="lg-line" style="background:#059669"></div><span>Belong To</span></div>
  <div class="lg-item"><div class="lg-line" style="background:#2563eb"></div><span>Compose</span></div>
  <div class="lg-item"><div class="lg-line dashed" style="color:#d97706"></div><span>Similar</span></div>
  <div class="lg-item"><div class="lg-line" style="background:#dc2626"></div><span>Depend</span></div>
</div>
<div id="bottom-bar">
<div id="cat-legend">{cat_legend}</div>
<div id="ctrls">
  <button class="cbtn" onclick="var el=document.getElementById('graph');if(el.requestFullscreen){{el.requestFullscreen()}}else if(el.webkitRequestFullscreen){{el.webkitRequestFullscreen()}}">⛶ Fullscreen</button>
  <button class="cbtn" onclick="net.fit({{animation:true}})">⊞ Fit</button>
  <button class="cbtn" onclick="net.moveTo({{scale:1,animation:true}})">1:1</button>
</div>
</div>
<div id="graph"></div>
</div>
<script>
var nodes=new vis.DataSet({nodes_json});
var edges=new vis.DataSet({edges_json});
var c=document.getElementById("graph");
var net=new vis.Network(c,{{nodes:nodes,edges:edges}},{{
  configure:{{enabled:false}},
  physics:{{solver:"forceAtlas2Based",forceAtlas2Based:{{gravitationalConstant:-80,centralGravity:0.005,springLength:260,springConstant:0.012,damping:0.6,avoidOverlap:1.0}},stabilization:{{iterations:500,fit:true,updateInterval:25}},maxVelocity:20,minVelocity:0.5}},
  interaction:{{hover:true,tooltipDelay:80,zoomView:true,dragView:true,dragNodes:true,navigationButtons:false}},
  nodes:{{shape:"dot",borderWidth:2.5,borderWidthSelected:5,shadow:{{enabled:true,color:"rgba(99,102,241,0.18)",size:24,x:0,y:4}}}},
  edges:{{selectionWidth:1.5,hoverWidth:1.5,color:{{inherit:false}}}},
}});
var _selNode=null;
var _styledIds=[];
var _origData={{}};
function clearStyle(){{for(var i=0;i<_styledIds.length;i++){{var id=_styledIds[i];var d=_origData[id];if(d){{nodes.update({{id:id,color:d.color,borderWidth:d.borderWidth||2.5,shadow:d.shadow||{{enabled:true,size:24,color:'rgba(99,102,241,0.18)',x:0,y:4}}}});delete _origData[id];}}}}_styledIds=[];}}
function setStyle(ids){{_styledIds=ids.slice();for(var i=0;i<ids.length;i++){{var id=ids[i];if(!_origData[id]){{var n=nodes.get(id);_origData[id]={{color:n.color,borderWidth:n.borderWidth,shadow:n.shadow}};}}nodes.update({{id:id,color:{{border:'#f59e0b',highlight:{{border:'#f59e0b'}}}},borderWidth:5,shadow:{{enabled:true,size:32,color:'rgba(245,158,11,0.55)',x:0,y:4}}}});}}}}
net.on("click",function(p){{if(p.nodes.length>0){{var n=p.nodes[0];if(_selNode===n){{_selNode=null;clearStyle();window.parent.postMessage({{type:"graphNodeClick",nodeId:null}},"*");return;}}clearStyle();_selNode=n;var conn=net.getConnectedNodes(n);conn.push(n);setStyle(conn);window.parent.postMessage({{type:"graphNodeClick",nodeId:n}},"*");}}else{{_selNode=null;clearStyle();window.parent.postMessage({{type:"graphNodeClick",nodeId:null}},"*");}}}});
window.addEventListener("message",function(e){{if(e.data&&e.data.type==="selectNode"){{clearStyle();_selNode=e.data.nodeId;var conn=net.getConnectedNodes(e.data.nodeId);conn.push(e.data.nodeId);setStyle(conn);net.focus(e.data.nodeId,{{animation:{{duration:800,easingFunction:"easeInOutQuad"}},scale:1.3}});}}}});
</script></body></html>"""


# ============================================================
# CSS — 完全对齐 resources.py 设计系统
# ============================================================
PAGE_CSS = """
<style>
    .stApp { background-color: #f8f9fa; }

    /* Package card */
    .pkg-card {
        background: linear-gradient(135deg, #e0f0ff 0%, #f0f7ff 15%, #f8fafc 40%, #ffffff 100%);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(186,210,235,0.5);
        box-shadow: 0 2px 8px rgba(59,130,246,0.06), 0 1px 2px rgba(0,0,0,0.04);
        transition: all 0.25s ease-in-out;
        height: 380px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        cursor: pointer;
    }
    .pkg-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 20px -4px rgba(59,130,246,0.15), 0 4px 8px -2px rgba(0,0,0,0.06);
        border-color: rgba(147,197,253,0.8);
    }

    .pkg-card .card-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 10px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e5e7eb;
    }
    .pkg-title {
        font-size: 1.05em;
        font-weight: 700;
        color: #111827;
        text-decoration: none;
        display: block;
        overflow-wrap: break-word;
    }
    .pkg-title:hover { color: #059669; }
    .pkg-desc {
        font-size: 0.88em;
        color: #4b5563;
        line-height: 1.5;
        flex-grow: 1;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 5;
        -webkit-box-orient: vertical;
        margin-bottom: 15px;
    }
    .pkg-footer {
        border-top: 1px solid #e5e7eb;
        padding-top: 10px;
        margin-top: auto;
        font-size: 0.8em;
        color: #6b7280;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .tag {
        display: inline-block;
        background-color: #f3f4f6;
        border-radius: 9999px;
        padding: 2px 8px;
        font-size: 0.75em;
        margin-right: 4px;
        margin-bottom: 4px;
        color: #374151;
        font-weight: 500;
    }
    .cat-tag {
        background-color: #e0f2fe;
        color: #0369a1;
    }
    .count-badge {
        background-color: #ecfdf5;
        color: #047857;
        padding: 2px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8em;
        white-space: nowrap;
    }

    /* Green primary buttons */
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

    /* Detail page */
    .detail-banner {
        background: #f0fdf4;
        border: 1px solid #d1fae5;
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .detail-banner h2 {
        margin: 0 0 8px 0;
        font-size: 1.6rem;
        font-weight: 800;
        color: #111827;
    }
    .detail-banner p {
        margin: 0;
        color: #4b5563;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .detail-tags { display: flex; flex-wrap: wrap; gap: 0; margin-top: 12px; align-items: center; }
    .detail-tag {
        font-size: 0.82em;
        color: #047857;
        padding: 0;
        font-weight: 500;
    }
    .detail-tag + .detail-tag::before {
        content: '|';
        margin: 0 10px;
        color: #9ca3af;
    }
    .stats-row {
        display: flex;
        gap: 28px;
        margin-top: 16px;
    }
    .stat-box { text-align: center; }
    .stat-val { font-size: 1.4rem; font-weight: 800; color: #059669; }
    .stat-lbl { font-size: 0.78rem; color: #6b7280; }

    .skill-item {
        background: #fff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        transition: border-color 0.2s;
    }
    .skill-item:hover { border-color: #059669; }
    .skill-item-name { font-weight: 600; font-size: 0.9em; color: #111827; }
    .skill-item-name a { text-decoration: none; color: #111827; }
    .skill-item-name a:hover { color: #059669; }
    .skill-item-desc { font-size: 0.82em; color: #4b5563; margin-top: 4px; line-height: 1.4; }
    .skill-item-meta { font-size: 0.75em; color: #9ca3af; margin-top: 6px; }

    /* Section Headers */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #d1fae5;
        display: inline-block;
    }
</style>
"""


# ============================================================
# Main
# ============================================================
def main():
    render_navbar()
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    all_packages = load_all_packages()
    params = st.query_params
    selected_pkg = params.get("pkg", None)

    if selected_pkg:
        render_detail_page(all_packages, selected_pkg)
    else:
        render_overview_page(all_packages)


# ============================================================
# Overview Page
# ============================================================
def render_overview_page(all_packages):
    total_skills = sum(p.get("skill_count", len(p.get("skills", []))) for p in all_packages)

    # Hero
    st.markdown(
        "<h1 style='text-align:center; margin-bottom:0; font-size:48px;'>Skill Collection</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:#6b7280; font-size:18px; max-width:700px; margin:8px auto 0;'>"
        "Curated skill collections for real-world scenarios, each paired with a skill relation graph.</p>",
        unsafe_allow_html=True,
    )

    # Counter badges
    st.markdown(f"""
    <div style="text-align:center; margin: 16px 0 8px;">
        <span style="color:#047857;background:#ecfdf5;padding:6px 16px;border-radius:99px;font-size:0.95em;
              display:inline-flex;align-items:center;border:1px solid #d1fae5;box-shadow:0 1px 2px rgba(0,0,0,0.05);">
            <span style="margin-right:6px;">{icon("package", 14, "#047857")}</span>
            <span style="font-weight:800;font-size:1.05em;">{len(all_packages)}</span>
            <span style="font-weight:500;opacity:0.65;margin-left:4px;">Collections</span>
            <span style="margin:0 8px;color:#a7f3d0;font-weight:300;">|</span>
            <span style="font-weight:800;font-size:1.05em;">{total_skills}</span>
            <span style="font-weight:500;opacity:0.65;margin-left:4px;">Total Skills</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        f"<div style='color:#888; margin-bottom:16px;'>Showing {len(all_packages)} collections | {total_skills} total skills</div>",
        unsafe_allow_html=True,
    )

    N_COLS = 4

    for row_start in range(0, len(all_packages), N_COLS):
        cols = st.columns(N_COLS)
        for col_idx, col in enumerate(cols):
            idx = row_start + col_idx
            if idx >= len(all_packages):
                break
            pkg = all_packages[idx]
            pkg_name = pkg.get("package_name", "")
            desc_raw = pkg.get("scene_description", "").strip()
            if desc_raw and desc_raw[-1] not in '.!?。！？':
                desc_raw += '.'
            desc = html_mod.escape(desc_raw)
            skill_count = pkg.get("skill_count", len(pkg.get("skills", [])))
            tags = pkg.get("tags", [])[:4]
            tags_html = "".join(
                f'<span class="tag">{html_mod.escape(t)}</span>' for t in tags
            )

            with col:
                st.markdown(f"""
                <a href="?pkg={pkg_name}" target="_self" style="text-decoration:none;">
                <div class="pkg-card">
                    <div>
                        <div class="card-header">
                            <span class="pkg-title">{pkg_name}</span>
                            <span class="count-badge">{icon("book-open", 14, "#6b7280")} {skill_count}</span>
                        </div>
                        <div class="pkg-desc">{desc}</div>
                        <div style="margin-bottom:8px;">
                            <span class="tag cat-tag">{pkg.get('category','')}</span>
                            {tags_html}
                        </div>
                    </div>
                    <div class="pkg-footer">
                        <div>{icon("link", 14, "#6b7280")} {skill_count} skills</div>
                        <span style="color:#059669; font-weight:600;">View Details →</span>
                    </div>
                </div>
                </a>
                """, unsafe_allow_html=True)

# ============================================================
# Detail Page
# ============================================================
def render_detail_page(all_packages, selected_pkg):
    pkg_data = None
    for p in all_packages:
        if p.get("package_name") == selected_pkg:
            pkg_data = p
            break

    if pkg_data is None:
        st.error(f"Package '{selected_pkg}' not found.")
        st.stop()

    # Back button
    if st.button("← Back to Collections", type="primary"):
        st.query_params.clear()
        st.rerun()

    skills = pkg_data.get("skills", [])
    relationships = pkg_data.get("relationships", [])
    total_stars = sum(s.get("stars", 0) for s in skills)

    # Banner
    tags_html = "".join(f'<span class="detail-tag">{html_mod.escape(t)}</span>' for t in pkg_data.get("tags", []))
    st.markdown(f"""
    <div class="detail-banner">
        <h2>{pkg_data['package_name']}</h2>
        <p>{html_mod.escape((pkg_data.get('scene_description', '').strip() + '.') if pkg_data.get('scene_description', '').strip() and pkg_data.get('scene_description', '').strip()[-1] not in '.!?。！？' else pkg_data.get('scene_description', ''))}</p>
        <div class="detail-tags">{tags_html}</div>
        <div class="stats-row">
            <div class="stat-box"><div class="stat-val">{len(skills)}</div><div class="stat-lbl">Skills</div></div>
            <div class="stat-box"><div class="stat-val">{len(relationships)}</div><div class="stat-lbl">Relations</div></div>
            <div class="stat-box"><div class="stat-val">{total_stars:,}</div><div class="stat-lbl">Total {icon("star", 14, "#d97706")}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Download button
    zip_bytes = create_package_zip(selected_pkg)
    if zip_bytes:
        st.download_button(
            label=f"⬇️  Download Collection ({len(skills)} skills)",
            data=zip_bytes,
            file_name=f"{selected_pkg}.zip",
            mime="application/zip",
            use_container_width=True,
            on_click=lambda: increment_download(len(skills))
        )

    # Two columns: skills list | relationship graph
    col_left, col_right = st.columns([2, 3])

    with col_left:
        st.markdown("<div class='section-header'>Skills in this Collection</div>", unsafe_allow_html=True)
        for idx, s in enumerate(skills, 1):
            s_name_raw = s.get("skill_name", "")
            s_name = html_mod.escape(s_name_raw)
            s_name_js = s_name_raw.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
            s_desc_raw = s.get("skill_description", "").strip()
            if s_desc_raw and s_desc_raw[-1] not in '.!?。！？':
                s_desc_raw += '.'
            s_desc = html_mod.escape(s_desc_raw)
            s_desc_short = s_desc[:180] + ("…" if len(s_desc) > 180 else "")
            s_url = s.get("skill_url", "#")
            s_stars = s.get("stars", 0)
            s_cat = html_mod.escape(s.get("category", ""))
            s_tags = "".join(f'<span class="tag">{html_mod.escape(t)}</span>' for t in s.get("tags", [])[:3])
            st.markdown(f"""
            <div class="skill-item" data-skill-name="{s_name_raw}" onclick="var ifr=document.querySelector('#graph-wrapper iframe');if(ifr)ifr.contentWindow.postMessage({{type:'selectNode',nodeId:'{s_name_js}'}},'*');this.style.background='#f0fdf4';setTimeout(function(){{this.style.background=''}}.bind(this),1500)" style="cursor:pointer;">
                <div class="skill-item-name">
                    {idx}. <a href="{s_url}" target="_blank" onclick="event.stopPropagation()">{s_name}</a>
                </div>
                <div class="skill-item-desc">{s_desc_short}</div>
                <div class="skill-item-meta">
                    {icon("star", 14, "#d97706")} {s_stars:,} &nbsp;|&nbsp; {s_cat} &nbsp;|&nbsp; {s_tags}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-header'>Skill Relation Graph</div>", unsafe_allow_html=True)
        if relationships:
            st.markdown('<div id="graph-wrapper">', unsafe_allow_html=True)
            graph_html = build_graph_html(skills, relationships, pkg_data['package_name'])
            render_html_embed(graph_html, height=600)
            st.markdown('</div>', unsafe_allow_html=True)
            # Bridge: listen for graph → list messages
            st.markdown("""
            <script>
            (function(){
                var _last=null;
                window.addEventListener("message",function(e){
                    if(e.data&&e.data.type==="graphNodeClick"){
                        if(_last){_last.style.background="";_last=null;}
                        if(e.data.nodeId){
                            var items=document.querySelectorAll("[data-skill-name]");
                            for(var i=0;i<items.length;i++){
                                if(items[i].getAttribute("data-skill-name")===e.data.nodeId){
                                    _last=items[i];
                                    items[i].scrollIntoView({behavior:"smooth",block:"center"});
                                    items[i].style.background="#f0fdf4";
                                    items[i].style.transition="background 0.3s";
                                    break;
                                }
                            }
                        }
                    }
                });
            })();
            </script>
            """, unsafe_allow_html=True)
        else:
            st.info("No relationship data available for this collection.")

        if relationships:
            with st.expander(f"📊 View all {len(relationships)} relationships"):
                for rel in relationships:
                    rtype = rel.get("type", "unknown")
                    color = RELATION_COLORS.get(rtype, "#999")
                    st.markdown(
                        f'<span style="color:{color};font-weight:600;">[{RELATION_LABELS.get(rtype, rtype)}]</span> '
                        f'**{rel["source"]}** → **{rel["target"]}**  \n'
                        f'<small style="color:#9ca3af;">{rel.get("reason", "")}</small>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("---")


if __name__ == "__main__":
    main()
