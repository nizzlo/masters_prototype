#!/bin/bash

# Stop all Adaptive Knowledge System services

echo "Stopping services..."

# Stop Streamlit
pkill -f "streamlit run" 2>/dev/null && echo "✓ Stopped Streamlit" || echo "Streamlit not running"

# Stop FastAPI
pkill -f "uvicorn api.server" 2>/dev/null && echo "✓ Stopped FastAPI" || echo "FastAPI not running"

echo "Done."
