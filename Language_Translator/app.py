# ============================================================
# app.py
# Main Streamlit application for the Language Translation Tool.
# Run with: streamlit run app.py
# ============================================================

import base64

import streamlit as st

from languages import (
    SOURCE_LANGUAGE_OPTIONS,
    TARGET_LANGUAGE_OPTIONS,
    get_language_code,
)
from translator import (
    translate_text,
    text_to_speech,
    compute_statistics,
    is_rtl_language,
)

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌐 LinguaFlow — AI Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root Variables ── */
:root {
    --bg:           #0d0f14;
    --surface:      #161922;
    --surface-2:    #1e2230;
    --border:       #2a2f3d;
    --accent:       #4fffb0;
    --accent-dim:   #1a5c40;
    --accent-glow:  rgba(79, 255, 176, 0.18);
    --text-primary: #e8ecf5;
    --text-muted:   #6b7280;
    --danger:       #ff5f5f;
    --warning:      #fbbf24;
    --radius:       14px;
    --radius-sm:    8px;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text-primary) !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px !important; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 2.8rem 1rem 1.6rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    background: var(--accent-glow);
    border: 1px solid var(--accent-dim);
    padding: 0.3rem 1rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    line-height: 1.1 !important;
    margin: 0 0 0.6rem !important;
}
.hero h1 span { color: var(--accent); }
.hero p {
    font-size: 1.05rem;
    color: var(--text-muted);
    margin: 0 auto;
    max-width: 560px;
    line-height: 1.6;
}

/* ── Card ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem 1.6rem;
    position: relative;
}
.card-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.7rem;
}

/* ── Stat Pills ── */
.stat-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 0.75rem;
}
.stat-pill {
    font-size: 0.76rem;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-muted);
}
.stat-pill b { color: var(--text-primary); }

/* ── Detected Language Badge ── */
.detected-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    background: rgba(251, 191, 36, 0.12);
    border: 1px solid rgba(251, 191, 36, 0.35);
    color: var(--warning);
    margin-top: 0.6rem;
    font-weight: 500;
}

/* ── Success / Error Banners ── */
.banner {
    border-radius: var(--radius-sm);
    padding: 0.85rem 1.1rem;
    font-size: 0.9rem;
    margin: 0.9rem 0;
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    line-height: 1.5;
}
.banner-success {
    background: rgba(79, 255, 176, 0.08);
    border: 1px solid var(--accent-dim);
    color: var(--accent);
}
.banner-error {
    background: rgba(255, 95, 95, 0.10);
    border: 1px solid rgba(255, 95, 95, 0.35);
    color: var(--danger);
}

/* ── Translated Output Box ── */
.translation-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.3rem 1.5rem;
    min-height: 130px;
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--text-primary);
    white-space: pre-wrap;
    word-break: break-word;
    margin-top: 0.4rem;
}
.translation-box.rtl { direction: rtl; text-align: right; }

/* ── Streamlit widget overrides ── */
.stTextArea textarea {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    resize: vertical !important;
    caret-color: var(--accent);
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-glow) !important;
}

.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

/* Primary button */
.stButton > button[kind="primary"],
.stButton > button {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.6rem !important;
    transition: opacity 0.18s, transform 0.14s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* Secondary / ghost button */
button[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
}
button[data-testid="baseButton-secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* Audio player */
audio { width: 100%; margin-top: 0.5rem; filter: invert(1) hue-rotate(140deg) brightness(0.85); }

/* Divider */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* Column gaps */
[data-testid="column"] { padding: 0 0.5rem !important; }

/* Selectbox label */
.stSelectbox label { color: var(--text-muted) !important; font-size: 0.82rem !important; }
.stTextArea label  { color: var(--text-muted) !important; font-size: 0.82rem !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ── Session-state initialisation ────────────────────────────────────────────
def _init_state() -> None:
    """Initialise all session-state keys if not already present."""
    defaults = {
        "source_text": "",
        "translated_text": "",
        "tts_audio": None,
        "last_error": "",
        "stats": None,
        "target_lang_code": "fr",  # default target: French
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


_init_state()


# ── Helper: inline HTML rendering ───────────────────────────────────────────
def _banner(msg: str, kind: str = "success") -> None:
    icon = "✅" if kind == "success" else "❌"
    st.markdown(
        f'<div class="banner banner-{kind}">{icon}&nbsp;{msg}</div>',
        unsafe_allow_html=True,
    )


def _stat_row(label_pairs: list[tuple[str, str]]) -> None:
    pills = "".join(
        f'<span class="stat-pill">{lbl}: <b>{val}</b></span>'
        for lbl, val in label_pairs
    )
    st.markdown(f'<div class="stat-row">{pills}</div>', unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✦ AI Translation Engine</div>
        <h1>🌐 Lingua<span>Flow</span></h1>
        <p>Translate, listen, and communicate across 57 languages with ease..</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Language selector row ────────────────────────────────────────────────────
col_src_lang, col_swap, col_tgt_lang = st.columns([5, 1, 5])

with col_src_lang:
    source_language = st.selectbox(
        "🔍 Source Language",
        options=SOURCE_LANGUAGE_OPTIONS,
        index=SOURCE_LANGUAGE_OPTIONS.index("English"),  # default: English
        key="source_lang_select",
    )

with col_swap:
    st.markdown("<br>", unsafe_allow_html=True)
    swap_clicked = st.button("⇄", help="Swap source ↔ target languages", use_container_width=True)

with col_tgt_lang:
    # Determine current index for target language
    try:
        tgt_idx = TARGET_LANGUAGE_OPTIONS.index("French")
        # If a previous selection was persisted, restore it
        persisted = st.session_state.get("target_lang_code", "fr")
        for i, lang in enumerate(TARGET_LANGUAGE_OPTIONS):
            from languages import get_language_code as _glc
            if _glc(lang) == persisted:
                tgt_idx = i
                break
    except ValueError:
        tgt_idx = TARGET_LANGUAGE_OPTIONS.index("French")

    target_language = st.selectbox(
        "🎯 Target Language",
        options=TARGET_LANGUAGE_OPTIONS,
        index=tgt_idx,
        key="target_lang_select",
    )

# Persist target language code
st.session_state["target_lang_code"] = get_language_code(target_language)

# ── Swap logic ───────────────────────────────────────────────────────────────
if swap_clicked:
    if st.session_state.get("translated_text"):
        # Swap the text
        st.session_state["source_text"] = st.session_state["translated_text"]
        st.session_state["translated_text"] = ""
        st.session_state["tts_audio"] = None
        st.session_state["last_error"] = ""
        st.session_state["stats"] = None
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── Main two-panel layout ────────────────────────────────────────────────────
col_input, col_output = st.columns(2, gap="large")

# ── LEFT: Input panel ────────────────────────────────────────────────────────
with col_input:
    st.markdown('<div class="card-label">📝 Input Text</div>', unsafe_allow_html=True)

    source_text = st.text_area(
        label="Enter text to translate",
        value=st.session_state["source_text"],
        height=220,
        placeholder="Type or paste your text here…",
        label_visibility="collapsed",
        key="source_text_area",
    )
    # Keep session state in sync
    st.session_state["source_text"] = source_text

    # Input statistics
    if source_text.strip():
        word_count  = len(source_text.split())
        char_count  = len(source_text)
        _stat_row([("Words", word_count), ("Characters", char_count)])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Action buttons ────────────────────────────────────────────────────
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        translate_clicked = st.button("🚀 Translate", use_container_width=True)
    with btn_col2:
        clear_clicked = st.button("🗑️ Clear All", use_container_width=True)

# ── RIGHT: Output panel ───────────────────────────────────────────────────────
with col_output:
    st.markdown('<div class="card-label">🌍 Translated Output</div>', unsafe_allow_html=True)

    # ── Error banner ──────────────────────────────────────────────────────
    if st.session_state["last_error"]:
        _banner(st.session_state["last_error"], "error")

    # ── Translation result box ────────────────────────────────────────────
    rtl_class = (
        "rtl"
        if is_rtl_language(st.session_state.get("target_lang_code", "en"))
        else ""
    )
    display_text = st.session_state["translated_text"] or "Translation will appear here…"
    st.markdown(
        f'<div class="translation-box {rtl_class}">{display_text}</div>',
        unsafe_allow_html=True,
    )

    # ── Output statistics ─────────────────────────────────────────────────
    if st.session_state["stats"]:
        s = st.session_state["stats"]
        _stat_row([
            ("Words", s["translated_words"]),
            ("Characters", s["translated_chars"]),
        ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Copy & TTS buttons ────────────────────────────────────────────────
    if st.session_state["translated_text"]:
        copy_col, tts_col = st.columns(2)

        with copy_col:
            # JavaScript clipboard copy trick via hidden textarea
            translated_escaped = (
                st.session_state["translated_text"]
                .replace("\\", "\\\\")
                .replace("`", "\\`")
                .replace("$", "\\$")
            )
            copy_js = f"""
                <script>
                function copyToClipboard() {{
                    navigator.clipboard.writeText(`{translated_escaped}`)
                        .then(() => alert('✅ Copied to clipboard!'))
                        .catch(() => alert('❌ Copy failed — please copy manually.'));
                }}
                </script>
                <button onclick="copyToClipboard()" style="
                    width:100%; padding:0.55rem 0; border-radius:8px;
                    background:transparent; border:1px solid #2a2f3d;
                    color:#6b7280; font-family:'Syne',sans-serif;
                    font-weight:700; font-size:0.9rem; cursor:pointer;
                    transition:all 0.18s;"
                    onmouseover="this.style.borderColor='#4fffb0';this.style.color='#4fffb0';"
                    onmouseout="this.style.borderColor='#2a2f3d';this.style.color='#6b7280';">
                    📋 Copy Text
                </button>
            """
            st.components.v1.html(copy_js, height=48)

        with tts_col:
            tts_clicked = st.button("🔊 Listen (TTS)", use_container_width=True)
    else:
        tts_clicked = False

# ── TTS audio player (spans full width below output panel) ───────────────────
if st.session_state.get("tts_audio"):
    st.markdown("---")
    st.markdown('<div class="card-label">🎧 Audio Playback</div>', unsafe_allow_html=True)
    st.audio(st.session_state["tts_audio"], format="audio/mp3")

# ── Translate action ─────────────────────────────────────────────────────────
if translate_clicked:
    if not source_text.strip():
        st.session_state["last_error"] = "Input field is empty. Please enter some text."
        st.session_state["translated_text"] = ""
        st.session_state["tts_audio"] = None
        st.session_state["stats"] = None
    else:
        src_code = get_language_code(source_language)
        tgt_code = get_language_code(target_language)

        with st.spinner("Translating… ✨"):
            result = translate_text(source_text, src_code, tgt_code)

        if result["success"]:
            st.session_state["translated_text"] = result["translated_text"]
            st.session_state["last_error"]       = ""
            st.session_state["stats"]            = compute_statistics(
                source_text, result["translated_text"]
            )
            st.session_state["tts_audio"]        = None  # reset old audio
            _banner("Translation successful!", "success")
        else:
            st.session_state["last_error"]       = result["error"]
            st.session_state["translated_text"]  = ""
            st.session_state["stats"]            = None
            st.session_state["tts_audio"]        = None

    st.rerun()

# ── TTS action ───────────────────────────────────────────────────────────────
if "tts_clicked" in dir() and tts_clicked and st.session_state["translated_text"]:
    tgt_code = get_language_code(target_language)
    with st.spinner("Generating audio…"):
        audio_bytes = text_to_speech(st.session_state["translated_text"], tgt_code)
    if audio_bytes:
        st.session_state["tts_audio"] = audio_bytes
    else:
        st.warning("⚠️ TTS is not supported for this language or encountered an error.")
    st.rerun()

# ── Clear action ─────────────────────────────────────────────────────────────
if clear_clicked:
    for key in ["source_text", "translated_text", "tts_audio", "last_error", "stats"]:
        st.session_state[key] = None if key == "tts_audio" else ""
    st.session_state["stats"] = None
    st.rerun()

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center; color:#6b7280; font-size:0.8rem; padding-bottom:1rem;">
        🌐 LinguaFlow • Connecting Languages, Connecting People
    </div>
    """,
    unsafe_allow_html=True,
)