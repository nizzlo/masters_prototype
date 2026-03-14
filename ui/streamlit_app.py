"""
Streamlit UI for the Adaptive Knowledge System.

This is the main entry point for the Streamlit application.
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator_agent import OrchestratorAgent
from config import settings, AVAILABLE_MODELS
import tempfile

# Page config
st.set_page_config(
    page_title="Adaptive Knowledge System",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Material Symbols font
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />
<style>
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    vertical-align: middle;
    -webkit-font-smoothing: antialiased;
    margin-right: 8px;
}
.icon-lg {
    font-size: 28px;
}
.icon-sm {
    font-size: 18px;
    margin-right: 4px;
}
</style>
""", unsafe_allow_html=True)

def icon(name: str, size: str = "") -> str:
    """Return HTML for a Material Symbol icon."""
    css_class = f"material-symbols-outlined {size}".strip()
    return f'<span class="{css_class}">{name}</span>'

# Model selection in sidebar
st.sidebar.markdown(f'### {icon("hub")} Adaptive Knowledge System', unsafe_allow_html=True)

# Model selector
st.sidebar.markdown(f'{icon("tune")} **Model Settings**', unsafe_allow_html=True)
current_model = st.session_state.get("selected_model", settings.reasoning_model)
model_options = list(AVAILABLE_MODELS.keys())
model_labels = [f"{AVAILABLE_MODELS[m]['name']} ({AVAILABLE_MODELS[m]['speed']})" for m in model_options]

selected_idx = model_options.index(current_model) if current_model in model_options else 0
selected_model = st.sidebar.selectbox(
    "Reasoning Model",
    model_options,
    index=selected_idx,
    format_func=lambda x: f"{AVAILABLE_MODELS[x]['name']} ({AVAILABLE_MODELS[x]['speed']})",
    help="Choose between speed and quality"
)

# Show model info
model_info = AVAILABLE_MODELS[selected_model]
st.sidebar.caption(f"{model_info['description']}")

# Note about what model affects
with st.sidebar.expander("What does this affect?"):
    st.markdown("""
    **Affects:**
    - Vectorization strategy selection
    - Answer generation
    
    **Does NOT affect:**
    - Embeddings (always mxbai-embed-large)
    - Document parsing
    - Vector search/retrieval
    """)

# Reinitialize orchestrator if model changed
if "selected_model" not in st.session_state or st.session_state.selected_model != selected_model:
    st.session_state.selected_model = selected_model
    # Update settings
    settings.reasoning_model = selected_model
    st.session_state.orchestrator = OrchestratorAgent()
    if "selected_model" in st.session_state:
        st.toast(f"Switched to {model_info['name']}")

st.sidebar.divider()

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Upload Data", "Knowledge Base", "AI Agent"],
)

# Main content
if page == "Upload Data":
    st.markdown(f'# {icon("upload_file", "icon-lg")} Upload Data', unsafe_allow_html=True)
    st.markdown("Upload enterprise data to build your knowledge base.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls", "pdf", "docx", "doc", "txt", "md"],
        help="Supported formats: CSV, Excel, PDF, Word, Text",
    )
    
    if uploaded_file is not None:
        st.info(f"Selected file: **{uploaded_file.name}**")
        
        if st.button("Process File", type="primary", icon=":material/play_arrow:"):
            with st.spinner("Processing file..."):
                # Save to temp file
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # Process
                try:
                    result = st.session_state.orchestrator.process_file(
                        tmp_path, 
                        source_name=uploaded_file.name
                    )
                    
                    # Clean up
                    os.unlink(tmp_path)
                    
                    if result["status"] == "success":
                        st.success("File processed successfully", icon=":material/check_circle:")
                        
                        # Show processing steps
                        st.subheader("Processing Steps")
                        for step_name, step_info in result.get("steps", {}).items():
                            status_icon = "✓" if step_info.get("status") == "success" else "✗"
                            with st.expander(f"{status_icon} {step_name.replace('_', ' ').title()}"):
                                for key, value in step_info.items():
                                    if key != "status":
                                        st.write(f"**{key}:** {value}")
                    else:
                        st.error(f"Processing failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    os.unlink(tmp_path)
                    st.error(f"Error: {str(e)}")

elif page == "Knowledge Base":
    st.markdown(f'# {icon("database", "icon-lg")} Knowledge Base', unsafe_allow_html=True)
    st.markdown("View information about your indexed documents.")
    
    # Get stats
    try:
        stats = st.session_state.orchestrator.get_stats()
        
        # Display metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents Indexed", stats["source_count"])
        with col2:
            st.metric("Vector Entries", stats["total_vectors"])
        
        # Display sources
        st.subheader("Indexed Sources")
        if stats["sources"]:
            for source in stats["sources"]:
                st.markdown(f'{icon("description", "icon-sm")} {source}', unsafe_allow_html=True)
        else:
            st.info("No documents indexed yet. Upload some files to get started!")
        
        # Clear button
        st.divider()
        if st.button("Clear Knowledge Base", type="secondary", icon=":material/delete:"):
            st.session_state.orchestrator.clear_knowledge_base()
            # Reinitialize orchestrator to get fresh collection reference
            st.session_state.orchestrator = OrchestratorAgent()
            st.success("Knowledge base cleared", icon=":material/check_circle:")
            st.rerun()
            
    except Exception as e:
        st.error(f"Error loading stats: {str(e)}")

elif page == "AI Agent":
    st.markdown(f'# {icon("smart_toy", "icon-lg")} AI Agent', unsafe_allow_html=True)
    st.markdown("Ask questions about your indexed documents.")
    
    # Get available sources for filtering
    try:
        stats = st.session_state.orchestrator.get_stats()
        available_sources = stats.get("sources", [])
    except:
        available_sources = []
    
    # Retrieval mode
    col1, col2 = st.columns([1, 2])
    with col1:
        retrieval_mode = st.radio(
            "Retrieval Mode",
            ["Global", "Scoped"],
            help="Global searches all documents. Scoped lets you select specific sources.",
        )
    
    # Source filter (for scoped mode)
    selected_sources = None
    if retrieval_mode == "Scoped" and available_sources:
        with col2:
            selected_sources = st.multiselect(
                "Select Sources",
                available_sources,
                default=available_sources[:1] if available_sources else [],
            )
    
    # Query input
    query = st.text_area(
        "Your Question",
        placeholder="e.g., What were the key findings in the financial report?",
        height=100,
    )
    
    if st.button("Ask", type="primary", disabled=not query, icon=":material/search:"):
        with st.spinner("Searching knowledge base and generating answer..."):
            try:
                result = st.session_state.orchestrator.query(
                    query=query,
                    sources=selected_sources if retrieval_mode == "Scoped" else None,
                    k=settings.default_top_k,
                )
                
                # Calculate retrieval metrics
                if result.retrieved_chunks:
                    scores = [chunk.score for chunk in result.retrieved_chunks]
                    avg_score = sum(scores) / len(scores)
                    max_score = max(scores)
                    min_score = min(scores)
                    score_range = max_score - min_score
                    
                    # Display retrieval metrics
                    st.subheader("Retrieval Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Chunks Retrieved", len(result.retrieved_chunks))
                    with col2:
                        st.metric("Avg Similarity", f"{avg_score:.3f}")
                    with col3:
                        st.metric("Top Score", f"{max_score:.3f}")
                    with col4:
                        # Confidence based on top score and score spread
                        confidence = max_score * (1 - score_range * 0.5) if score_range < 1 else max_score * 0.5
                        st.metric("Confidence", f"{confidence:.1%}")
                    
                    # Score distribution
                    with st.expander("Score Distribution"):
                        import pandas as pd
                        score_data = pd.DataFrame({
                            "Chunk": [f"Chunk {i+1}" for i in range(len(scores))],
                            "Similarity Score": scores,
                            "Source": [chunk.source for chunk in result.retrieved_chunks]
                        })
                        st.bar_chart(score_data.set_index("Chunk")["Similarity Score"])
                        st.dataframe(score_data, use_container_width=True)
                    
                    # Evaluation metrics explanation
                    with st.expander("Evaluation Metrics Explained"):
                        st.markdown("""
**How Retrieval Quality is Measured**

The system uses standard Information Retrieval metrics:

| Metric | Formula | Description |
|--------|---------|-------------|
| **Recall@K** | `relevant_in_top_k / total_relevant` | What % of relevant chunks were retrieved in top K |
| **Precision@K** | `relevant_in_top_k / K` | What % of top K chunks are relevant |
| **MRR** | `1 / rank_of_first_relevant` | How quickly a relevant chunk appears |

**Current Score-Based Proxy Metrics:**
""")
                        # Calculate proxy metrics based on similarity threshold
                        threshold = 0.5  # Consider chunks with score > 0.5 as "relevant"
                        high_quality = sum(1 for s in scores if s > threshold)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            proxy_precision = high_quality / len(scores) if scores else 0
                            st.metric("Precision (proxy)", f"{proxy_precision:.1%}", 
                                     help=f"Chunks with score > {threshold}")
                        with col2:
                            # Normalized Discounted Cumulative Gain proxy
                            dcg = sum(s / (i + 2) for i, s in enumerate(scores))  # log2(i+2)
                            ideal_dcg = sum(sorted(scores, reverse=True)[i] / (i + 2) for i in range(len(scores)))
                            ndcg = dcg / ideal_dcg if ideal_dcg > 0 else 0
                            st.metric("nDCG", f"{ndcg:.3f}",
                                     help="Normalized Discounted Cumulative Gain")
                        with col3:
                            # Score consistency
                            consistency = 1 - (score_range / max_score) if max_score > 0 else 0
                            st.metric("Score Consistency", f"{consistency:.1%}",
                                     help="How similar the scores are (less spread = more consistent)")
                        
                        st.markdown(f"""
---
**Note:** True evaluation requires **ground truth labels** - human-annotated relevant chunks for each query.  
The proxy metrics above use similarity scores (threshold={threshold}) as a relevance estimate.

**Score threshold:** {threshold} · **High-quality chunks:** {high_quality}/{len(scores)}
""")
                
                # Display retrieved chunks
                st.subheader("Retrieved Context")
                for i, chunk in enumerate(result.retrieved_chunks):
                    with st.expander(f"#{i+1} · {chunk.source} · {chunk.score:.3f}"):
                        st.write(chunk.content)
                
                # Display answer
                st.markdown(f'### {icon("lightbulb", "icon-lg")} Answer', unsafe_allow_html=True)
                st.markdown(result.answer)
                
                # Display sources
                if result.sources:
                    st.caption(f"**Sources used:** {', '.join(result.sources)}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.sidebar.divider()
st.sidebar.caption("Adaptive Knowledge System v1.0")
st.sidebar.caption("Powered by Ollama + ChromaDB")
st.sidebar.caption(f"Collection: `{settings.chroma_collection_name}`")
