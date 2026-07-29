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
# LOAD SEARCH ENGINE
# -------------------------------------------------------

@st.cache_resource
def load_engine():
    return SemanticSearchEngine()

engine = load_engine()

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.title("🔍 Semantic Search Engine using MiniLM")
st.caption("Clinical Semantic Search using Sentence Transformers")

st.divider()

# -------------------------------------------------------
# INFORMATION SECTION
# -------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("📂 Dataset Information")

        st.write("**Dataset :** Microsoft Learn Transcripts")
        st.write(f"**Total Summaries :** {len(engine.dataset)}")
        st.write("**Source :** embedding_index_3m.json")

with col2:

    with st.container(border=True):

        st.subheader("🤖 Model Information")

        st.write("**Embedding Model :** all-MiniLM-L6-v2")
        st.write("**Embedding Dimension :** 384")
        st.write("**Similarity Measure :** Cosine Similarity")

st.divider()

# -------------------------------------------------------
# SEARCH BAR
# -------------------------------------------------------

left, right = st.columns([5,1])

with left:

    query = st.text_input(
        "Enter your query",
        placeholder="Example: Responsible AI"
    )

with right:

    st.write("")
    st.write("")

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
            time.sleep(0.5)        # -------------------------------------------------------
        # RESULTS
        # -------------------------------------------------------

        st.divider()
        st.subheader("Top 5 Search Results")

        if len(results) == 0:
            st.error("No matching results found.")

        else:

            for index, result in enumerate(results, start=1):

                with st.container(border=True):

                    col1, col2 = st.columns([4, 1])

                    with col1:

                        st.markdown(f"## 🏆 Rank #{index}")

                        similarity = result["score"] * 100

                        st.metric(
                            label="Similarity Score",
                            value=f"{similarity:.2f}%"
                        )

                        st.write(f"**Title:** {result['title']}")

                        st.write(f"**Speaker:** {result['speaker']}")

                    with col2:

                        st.metric(
                            label="Video Time",
                            value=result["start"]
                        )

                    st.markdown("---")

                    st.markdown("### 📝 Summary")

                    st.write(result["summary"])

                    st.markdown("---")

                    video_url = (
                        f"https://www.youtube.com/watch?v={result['videoId']}"
                        f"&t={result['start']}s"
                    )

                    st.link_button(
                        "▶ Watch on YouTube",
                        video_url,
                        use_container_width=True
                    )

        st.success("Search completed successfully!")