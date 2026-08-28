import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Natural light theme ───────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #292722;
}

.stApp {
    background: #f6f3ed;
    color: #292722;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 1.25rem 2rem 3.5rem;
    max-width: 1180px;
}

/* ── Hero ───────────────────────────────────────────────────────────── */
.hero {
    text-align: left;
    padding: 2.4rem 0 1.8rem;
    position: relative;
}

.hero-eyebrow {
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7c756b;
    margin-bottom: 0.7rem;
}

.hero h1 {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: clamp(2.6rem, 5vw, 4.4rem);
    font-weight: 800;
    line-height: 0.98;
    letter-spacing: -0.045em;
    color: #25231f;
    margin: 0 0 0.75rem;
}

.hero h1 span {
    color: #697b63;
}

.hero-sub {
    font-size: 0.98rem;
    font-weight: 400;
    color: #777168;
    max-width: 590px;
    margin: 0;
    line-height: 1.65;
}

.divider {
    height: 1px;
    background: #dfdbd2;
    margin: 0 0 2rem;
}

/* ── Main cards ─────────────────────────────────────────────────────── */
.input-card {
    background: #fffdf9;
    border: 1px solid #dfdbd2;
    border-radius: 14px;
    padding: 1.55rem 1.7rem 1.4rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 5px 18px rgba(53, 47, 38, 0.045);
}

.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid #cfc9bf !important;
    border-radius: 9px !important;
    color: #292722 !important;
    -webkit-text-fill-color: #292722 !important;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    font-size: 0.96rem !important;
    padding: 0.72rem 0.9rem !important;
    box-shadow: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: #a29b91 !important;
    opacity: 1 !important;
}

.stTextInput > div > div > input:focus {
    border-color: #697b63 !important;
    box-shadow: 0 0 0 3px rgba(105, 123, 99, 0.12) !important;
}

.stTextInput > label {
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace !important;
    font-size: 0.67rem !important;
    letter-spacing: 0.13em !important;
    text-transform: uppercase !important;
    color: #777168 !important;
    font-weight: 600 !important;
}

/* ── Primary button ─────────────────────────────────────────────────── */
.stButton > button {
    background: #30332e !important;
    color: #fffdf9 !important;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    font-weight: 650 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    border: 1px solid #30332e !important;
    border-radius: 9px !important;
    padding: 0.68rem 1.4rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.15s !important;
    box-shadow: none !important;
    width: 100%;
}

.stButton > button:hover {
    background: #4c5547 !important;
    border-color: #4c5547 !important;
    transform: translateY(-1px) !important;
    box-shadow: none !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Examples ───────────────────────────────────────────────────────── */
.example-row {
    display: flex;
    gap: 0.45rem;
    flex-wrap: wrap;
    align-items: center;
    margin: 0.5rem 0 1rem;
}

.example-label {
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
    font-size: 0.66rem;
    color: #928b82;
    letter-spacing: 0.08em;
    margin-right: 0.1rem;
}

.example-chip {
    background: #eeeae2;
    border: 1px solid #ddd8cf;
    border-radius: 999px;
    padding: 0.3rem 0.7rem;
    font-size: 0.72rem;
    color: #665f56;
}

/* ── Pipeline ───────────────────────────────────────────────────────── */
.section-heading {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 1.2rem;
    font-weight: 750;
    color: #292722;
    margin: 0.2rem 0 0.85rem;
}

.step-card {
    background: #fffdf9;
    border: 1px solid #dfdbd2;
    border-radius: 12px;
    padding: 1.15rem 1.35rem;
    margin-bottom: 0.75rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 3px 12px rgba(53, 47, 38, 0.035);
}

.step-card.active {
    border-color: #aebaa8;
    background: #f7f9f5;
}

.step-card.done {
    border-color: #cbd5c7;
    background: #f7f9f5;
}

.step-card::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: #e4dfd6;
}

.step-card.active::before { background: #697b63; }
.step-card.done::before { background: #879a7d; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.25rem;
}

.step-num {
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
    font-size: 0.63rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    color: #9b9388;
}

.step-title {
    font-size: 0.91rem;
    font-weight: 700;
    color: #292722;
}

.step-status {
    margin-left: auto;
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
    font-size: 0.62rem;
    letter-spacing: 0.06em;
}

.status-waiting { color: #aaa39a; }
.status-running { color: #697b63; }
.status-done { color: #697b63; }

.step-card div[style*="font-size:0.82rem"] {
    color: #827a70 !important;
}

/* ── Results ───────────────────────────────────────────────────────── */
.result-panel,
.report-panel,
.feedback-panel {
    background: #fffdf9;
    border: 1px solid #dfdbd2;
    border-radius: 13px;
    padding: 1.5rem 1.7rem;
    margin-top: 0.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 14px rgba(53, 47, 38, 0.035);
}

.report-panel {
    border-top: 3px solid #697b63;
}

.feedback-panel {
    border-top: 3px solid #a08d70;
}

.result-panel-title,
.panel-label {
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #777168;
    margin-bottom: 0.9rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid #e5e1d9;
}

.panel-label.orange { color: #697b63; }
.panel-label.green { color: #8a765e; }

.result-content {
    font-size: 0.9rem;
    line-height: 1.75;
    color: #4f4a43;
    white-space: pre-wrap;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stSpinner > div { color: #697b63 !important; }

details summary {
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace !important;
    font-size: 0.7rem !important;
    color: #777168 !important;
    letter-spacing: 0.07em !important;
    cursor: pointer;
}

.stDownloadButton > button {
    background: #fffdf9 !important;
    color: #4f4a43 !important;
    border: 1px solid #cfc9bf !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
}

.stDownloadButton > button:hover {
    border-color: #697b63 !important;
    color: #697b63 !important;
}

.notice {
    font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
    font-size: 0.65rem;
    color: #aaa39a;
    text-align: center;
    margin-top: 2.5rem;
    letter-spacing: 0.05em;
}

/* ── Mobile ────────────────────────────────────────────────────────── */
@media (max-width: 850px) {
    .block-container { padding: 1rem 1rem 2.5rem; }
    .hero { padding: 1.5rem 0 1.25rem; }
    .hero h1 { font-size: 3rem; }
    .hero-sub { font-size: 0.9rem; }
    .input-card { padding: 1.25rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#667085;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div class="example-row">
        <span class="example-label">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f"""
        <span class="example-chip">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        research_combined = research_combined[:10000]

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        report_for_critic = results["writer"][:6000]
        results["critic"] = critic_chain.invoke({
            "report": report_for_critic
        })

        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)