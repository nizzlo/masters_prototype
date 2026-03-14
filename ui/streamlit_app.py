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
import tempfile

# Page config
st.set_page_config(
    page_title="Adaptive Knowledge System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize orchestrator in session state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = OrchestratorAgent()

# Sidebar navigation
st.sidebar.title("🧠 Adaptive Knowledge System")
page = st.sidebar.radio(
    "Navigation",
    ["📤 Upload Data", "📚 Knowledge Base", "💬 Ask the AI Agent"],
)

# Main content
if page == "📤 Upload Data":
    st.title("📤 Upload Data")
    st.markdown("Upload enterprise data to build your knowledge base.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls", "pdf", "docx", "doc", "txt", "md"],
        help="Supported formats: CSV, Excel, PDF, Word, Text",
    )
    
    if uploaded_file is not None:
        st.info(f"Selected file: **{uploaded_file.name}**")
        
        if st.button("🚀 Process File", type="primary"):
            with st.spinner("Processing file..."):
                # Save to temp file
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # Process
                try:
                    result = st.session_state.orchestrator.process_file(tmp_path)
                    
                    # Clean up
                    os.unlink(tmp_path)
                    
                    if result["status"] == "success":
                        st.success("✅ File processed successfully!")
                        
                        # Show processing steps
                        st.subheader("Processing Steps")
                        for step_name, step_info in result.get("steps", {}).items():
                            status_icon = "✅" if step_info.get("status") == "success" else "❌"
                            with st.expander(f"{status_icon} {step_name.replace('_', ' ').title()}"):
                                for key, value in step_info.items():
                                    if key != "status":
                                        st.write(f"**{key}:** {value}")
                    else:
                        st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    os.unlink(tmp_path)
                    st.error(f"❌ Error: {str(e)}")

elif page == "📚 Knowledge Base":
    st.title("📚 Knowledge Base")
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
                st.write(f"📄 {source}")
        else:
            st.info("No documents indexed yet. Upload some files to get started!")
        
        # Clear button
        st.divider()
        if st.button("🗑️ Clear Knowledge Base", type="secondary"):
            st.session_state.orchestrator.clear_knowledge_base()
            st.success("Knowledge base cleared!")
            st.rerun()
            
    except Exception as e:
        st.error(f"Error loading stats: {str(e)}")

elif page == "💬 Ask the AI Agent":
    st.title("💬 Ask the AI Agent")
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
            ["🌐 Global", "🎯 Scoped"],
            help="Global searches all documents. Scoped lets you select specific sources.",
        )
    
    # Source filter (for scoped mode)
    selected_sources = None
    if retrieval_mode == "🎯 Scoped" and available_sources:
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
    
    if st.button("🔍 Ask", type="primary", disabled=not query):
        with st.spinner("Searching knowledge base and generating answer..."):
            try:
                result = st.session_state.orchestrator.query(
                    query=query,
                    sources=selected_sources if retrieval_mode == "🎯 Scoped" else None,
                    k=5,
                )
                
                # Display retrieved chunks
                st.subheader("📋 Retrieved Context")
                for i, chunk in enumerate(result.retrieved_chunks):
                    with st.expander(f"Chunk {i+1} - {chunk.source} (Score: {chunk.score:.3f})"):
                        st.write(chunk.content)
                
                # Display answer
                st.subheader("💡 Answer")
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
