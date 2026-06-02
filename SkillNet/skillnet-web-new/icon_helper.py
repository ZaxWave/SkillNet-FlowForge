"""
SkillNet Lucide SVG Icon Helper.
Zero-dependency inline SVG icons from Lucide (MIT). Stroke-based, consistent 24px grid.
Usage: from icon_helper import icon; st.markdown(icon("star", 18, "#d97706"), unsafe_allow_html=True)
"""

_ICONS: dict[str, str] = {}

# ── Navigation / Feature Cards ──
_ICONS["package"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>'
    '<path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>'
)
_ICONS["database"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
    '<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
)
_ICONS["book-open"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
    '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>'
)
_ICONS["terminal"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>'
)
_ICONS["flask-conical"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M10 2v7.31"/><path d="M14 9.3V1.99"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/></svg>'
)
_ICONS["grid-3x3"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/>'
    '<rect width="7" height="7" x="3" y="14" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/></svg>'
)
_ICONS["file-text"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
    '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>'
)
_ICONS["code-2"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/></svg>'
)

# ── Evaluation Metrics ──
_ICONS["shield-check"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'
)
_ICONS["puzzle"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.611c-.47.47-1.087.706-1.704.706s-1.233-.235-1.704-.706l-1.568-1.568a1.026 1.026 0 0 0-.877-.29c-.493.074-.84.504-1.02.968a2.5 2.5 0 1 1-3.237-3.237c.464-.18.894-.527.967-1.02a1.026 1.026 0 0 0-.289-.877l-1.568-1.568A2.412 2.412 0 0 1 4 12c0-.617.236-1.234.706-1.704L6.317 8.68a.98.98 0 0 1 .837-.276c.47.07.802.48.968.925a2.501 2.501 0 1 1 3.214-3.214c-.166-.446-.497-.855-.925-.968a.979.979 0 0 1 .276-.837l1.611-1.611A2.412 2.412 0 0 1 14.002 2c.617 0 1.234.236 1.704.706l1.568 1.568c.23.23.556.338.877.29.493-.074.84-.504 1.02-.968a2.5 2.5 0 1 1 3.237 3.237c-.464.18-.894.527-.968 1.02Z"/></svg>'
)
_ICONS["zap"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
)
_ICONS["wrench"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>'
)
_ICONS["circle-dollar-sign"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><line x1="12" y1="18" x2="12" y2="22"/></svg>'
)

# ── UI Elements ──
_ICONS["star"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
)
_ICONS["download"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
)
_ICONS["external-link"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
)
_ICONS["user"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
)
_ICONS["calendar"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
)
_ICONS["bar-chart-3"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>'
)
_ICONS["search"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'
)
_ICONS["settings"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>'
)
_ICONS["heart"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>'
)
_ICONS["github"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>'
)
_ICONS["sparkles"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"/></svg>'
)
_ICONS["arrow-left"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>'
)
_ICONS["info"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
)

_ICONS["link"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
)

_ICONS["globe"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
)

_ICONS["eye"] = (
    '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none"'
    ' stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>'
)


def icon(name: str, size: int = 20, color: str = "currentColor") -> str:
    """Return inline SVG for a Lucide icon. Falls back to empty string if unknown."""
    tmpl = _ICONS.get(name)
    if not tmpl:
        return ""
    return tmpl.format(s=str(size), c=color)


def icon_img(name: str, size: int = 20, color: str = "currentColor") -> str:
    """Shorter alias, same as icon()."""
    return icon(name, size, color)
