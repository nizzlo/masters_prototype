#!/bin/bash

# Stop all Adaptive Knowledge System services

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Stopping services..."

# Stop Streamlit
if [ -f logs/streamlit.pid ]; then
    PID=$(cat logs/streamlit.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Stopped Streamlit (PID: $PID)"
    fi
    rm -f logs/streamlit.pid
fi
pkill -f "streamlit run" 2>/dev/null && echo -e "${GREEN}✓${NC} Stopped remaining Streamlit processes" || true

# Stop FastAPI
if [ -f logs/api.pid ]; then
    PID=$(cat logs/api.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Stopped FastAPI (PID: $PID)"
    fi
    rm -f logs/api.pid
fi
pkill -f "uvicorn api.server" 2>/dev/null && echo -e "${GREEN}✓${NC} Stopped remaining FastAPI processes" || true

# Verify ports are free
sleep 1
if lsof -i :8000 >/dev/null 2>&1; then
    echo -e "${RED}Warning: Port 8000 still in use${NC}"
else
    echo -e "${GREEN}✓${NC} Port 8000 is free"
fi

if lsof -i :8501 >/dev/null 2>&1; then
    echo -e "${RED}Warning: Port 8501 still in use${NC}"
else
    echo -e "${GREEN}✓${NC} Port 8501 is free"
fi

echo ""
echo "Done."
