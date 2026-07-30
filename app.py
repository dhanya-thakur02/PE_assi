import streamlit as st
import time
from search_engine import SemanticSearchEngine

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="🔍",
    layout="wide"
)

# -------------------------------------------------------
# STYLES
# -------------------------------------------------------

st.markdown("""
<style>

.app-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 2px;
}
.app-header-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: #E1F5EE;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    flex-shrink: 0;
}
.app-header-title {
    font-size: 60px !important;
    color: #9FE1CB !important;
    font-weight: 700;
    margin: 0;
    line-height: 1.15;
}

.info-card {
    border-radius: 12px;
    padding: 16px 18px;
    height: 100%;
}
.info-card-blue {
    background: #E6F1FB;
}
.info-card-purple {
    background: #EEEDFE;
}
.info-card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 10px;
}
.info-card-blue .info-card-title { color: #042C53; }
.info-card-purple .info-card-title { color: #26215C; }
.info-row {
    display: flex;
    gap: 6px;
    font-size: 13px;
    line-height: 1.9;
}
.info-card-blue .info-row { color: #0C447C; }
.info-card-purple .info-row { color: #3C3489; }
.info-row span:first-child { opacity: 0.75; }

.result-card {
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    border: 1px solid transparent;
}
.result-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
}
.result-rank {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    font-weight: 600;
}
.result-time-label { font-size: 11px; text-align: right; margin: 0; }
.result-time-value { font-size: 13px; font-weight: 600; text-align: right; margin: 0; }
.result-score-label { font-size: 11px; margin: 0 0 2px 0; }
.result-score-value { font-size: 19px; font-weight: 700; margin: 0 0 10px 0; }
.result-field { font-size: 12px; margin: 0 0 3px 0; }
.result-field-label { opacity: 0.75; }
.result-divider { border-top: 0.5px solid; padding-top: 10px; margin-bottom: 10px; opacity: 0.9; }
.result-summary-title {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    font-weight: 600;
    margin: 0 0 5px 0;
}
.result-summary-text { font-size: 12px; line-height: 1.55; margin: 0; }
.watch-btn {
    display: block;
    text-align: center;
    width: 100%;
    padding: 7px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
    box-sizing: border-box;
}

.st-key-search-row [data-testid="stHorizontalBlock"] {
    align-items: flex-end;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# RANK COLOR THEMES (cycled per result)
# -------------------------------------------------------

RANK_THEMES = [
    {"border": "#BA7517", "bg": "#FAEEDA", "title": "#412402", "sub": "#633806"},
    {"border": "#888780", "bg": "#F1EFE8", "title": "#2C2C2A", "sub": "#444441"},
    {"border": "#D85A30", "bg": "#FAECE7", "title": "#4A1B0C", "sub": "#712B13"},
    {"border": "#378ADD", "bg": "#E6F1FB", "title": "#042C53", "sub": "#0C447C"},
    {"border": "#7F77DD", "bg": "#EEEDFE", "title": "#26215C", "sub": "#3C3489"},
]

# -------------------------------------------------------
# LOAD SEARCH ENGINE
# -------------------------------------------------------

@st.cache_resource
def load_engine():
    return SemanticSearchEngine()

engine = load_engine()

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown("""
<div class="app-header">
    <div class="app-header-icon">🔍</div>
    <p class="app-header-title">Semantic Search Engine using MiniLM</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------
# INFORMATION SECTION
# -------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="info-card info-card-blue">
        <div class="info-card-title"> Dataset Information</div>
        <div class="info-row"><span>Dataset:</span><span>Microsoft Learn Transcripts</span></div>
        <div class="info-row"><span>Total Summaries:</span><span>{len(engine.dataset)}</span></div>
        <div class="info-row"><span>Source:</span><span>embedding_index_3m.json</span></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card info-card-purple">
        <div class="info-card-title"> Model Information</div>
        <div class="info-row"><span>Embedding Model:</span><span>all-MiniLM-L6-v2</span></div>
        <div class="info-row"><span>Embedding Dimension:</span><span>384</span></div>
        <div class="info-row"><span>Similarity Measure:</span><span>Cosine Similarity</span></div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------
# SEARCH BAR
# -------------------------------------------------------

with st.container(key="search-row"):

    left, right = st.columns([5, 1])

    with left:
        query = st.text_input(
            "Enter your query",
            placeholder="Example: Responsible AI"
        )

    with right:
        search = st.button(
            "Search",
            use_container_width=True
        )

st.divider()

# -------------------------------------------------------
# PIPELINE
# -------------------------------------------------------

pipeline_placeholder = st.empty()
results_placeholder = st.empty()

# -------------------------------------------------------
# SEARCH BUTTON
# -------------------------------------------------------

if search:

    if query.strip() == "":

        st.warning("Please enter a query.")

    else:

        with pipeline_placeholder.container(border=True):

            st.subheader("Semantic Search Pipeline")

            progress = st.progress(0)

            st.write("Step 1 : Query received")
            progress.progress(20)
            time.sleep(0.5)

            st.write("Step 2 : Generating semantic embedding")
            progress.progress(40)
            time.sleep(0.5)

            st.write(f"Step 3 : Comparing with {len(engine.dataset)} summaries")
            progress.progress(60)
            time.sleep(0.5)

            st.write("Step 4 : Computing cosine similarity")
            progress.progress(80)
            time.sleep(0.5)

            results = engine.search(query)

            st.write("Step 5 : Ranking Top 5 results")
            progress.progress(100)
            time.sleep(0.5)

        # -------------------------------------------------------
        # RESULTS
        # -------------------------------------------------------

        st.divider()
        st.subheader("Top 5 Search Results")

        if len(results) == 0:
            st.error("No matching results found.")

        else:

            for index, result in enumerate(results, start=1):

                theme = RANK_THEMES[(index - 1) % len(RANK_THEMES)]
                similarity = result["score"] * 100
                video_url = (
                    f"https://www.youtube.com/watch?v={result['videoId']}"
                    f"&t={result['start']}s"
                )

                st.markdown(f"""
                <div class="result-card" style="background:{theme['bg']}; border-color:{theme['border']};">
                    <div class="result-top">
                        <div class="result-rank" style="color:{theme['title']};">🏆 Rank #{index}</div>
                        <div>
                            <p class="result-time-label" style="color:{theme['sub']};">Video Time</p>
                            <p class="result-time-value" style="color:{theme['title']};">{result['start']}</p>
                        </div>
                    </div>
                    <p class="result-score-label" style="color:{theme['sub']};">Similarity Score</p>
                    <p class="result-score-value" style="color:{theme['title']};">{similarity:.2f}%</p>
                    <p class="result-field" style="color:{theme['title']};"><span class="result-field-label" style="color:{theme['sub']};">Title:</span> {result['title']}</p>
                    <p class="result-field" style="color:{theme['title']};"><span class="result-field-label" style="color:{theme['sub']};">Speaker:</span> {result['speaker']}</p>
                    <div class="result-divider" style="border-color:{theme['border']};">
                        <p class="result-summary-title" style="color:{theme['title']};">📝 Summary</p>
                        <p class="result-summary-text" style="color:{theme['sub']};">{result['summary']}</p>
                    </div>
                    <a class="watch-btn" href="{video_url}" target="_blank" style="background:{theme['border']}; color:{theme['bg']};">▶ Watch on YouTube</a>
                </div>
                """, unsafe_allow_html=True)

        
