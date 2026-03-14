#!/bin/bash

# Adaptive Knowledge System - Startup Script
# This script starts all required services

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Create logs directory if it doesn't exist
mkdir -p logs

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Adaptive Knowledge System Startup    ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :"$1" >/dev/null 2>&1
}

# Function to wait for port to be ready
wait_for_port() {
    local port=$1
    local timeout=$2
    local count=0
    while [ $count -lt $timeout ]; do
        if port_in_use $port; then
            return 0
        fi
        sleep 1
        count=$((count + 1))
    done
    return 1
}

# Check for Python
if ! command_exists python3; then
    echo -e "${RED}Error: Python3 is not installed.${NC}"
    exit 1
fi

# Check for Ollama
if ! command_exists ollama; then
    echo -e "${RED}Error: Ollama is not installed.${NC}"
    echo "Install from: https://ollama.com"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓${NC} Activating virtual environment..."
    source .venv/bin/activate
fi

# Check/Install dependencies
echo -e "${GREEN}✓${NC} Checking dependencies..."
pip3 install -q -r requirements.txt 2>/dev/null || {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip3 install -r requirements.txt
}

# Start Ollama if not running
echo ""
echo -e "${BLUE}[1/4] Checking Ollama...${NC}"
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${YELLOW}Starting Ollama...${NC}"
    ollama serve > /dev/null 2>&1 &
    sleep 2
fi
echo -e "${GREEN}✓${NC} Ollama is running"

# Check for required models
echo ""
echo -e "${BLUE}[2/4] Checking models...${NC}"
if ! ollama list 2>/dev/null | grep -q "llama3.2:1b"; then
    echo -e "${YELLOW}Pulling llama3.2:1b model (this may take a while)...${NC}"
    ollama pull llama3.2:1b
fi
echo -e "${GREEN}✓${NC} llama3.2:1b model ready"

if ! ollama list 2>/dev/null | grep -q "nomic-embed-text"; then
    echo -e "${YELLOW}Pulling nomic-embed-text model...${NC}"
    ollama pull nomic-embed-text
fi
echo -e "${GREEN}✓${NC} nomic-embed-text model ready"

# Start FastAPI server
echo ""
echo -e "${BLUE}[3/4] Starting API server...${NC}"
if port_in_use 8000; then
    echo -e "${YELLOW}Port 8000 already in use, killing existing process...${NC}"
    pkill -f "uvicorn api.server" 2>/dev/null || true
    sleep 2
fi
nohup python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000 > logs/api.log 2>&1 &
API_PID=$!
echo $API_PID > logs/api.pid
if wait_for_port 8000 10; then
    echo -e "${GREEN}✓${NC} API server running at http://localhost:8000 (PID: $API_PID)"
else
    echo -e "${RED}✗${NC} Failed to start API server. Check logs/api.log for details"
    cat logs/api.log 2>/dev/null | tail -20
fi

# Start Streamlit UI
echo ""
echo -e "${BLUE}[4/4] Starting Streamlit UI...${NC}"
if port_in_use 8501; then
    echo -e "${YELLOW}Port 8501 already in use, killing existing process...${NC}"
    pkill -f "streamlit run" 2>/dev/null || true
    sleep 2
fi
nohup python3 -m streamlit run ui/streamlit_app.py --server.headless true > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!
echo $STREAMLIT_PID > logs/streamlit.pid
if wait_for_port 8501 10; then
    echo -e "${GREEN}✓${NC} Streamlit UI running at http://localhost:8501 (PID: $STREAMLIT_PID)"
else
    echo -e "${RED}✗${NC} Failed to start Streamlit. Check logs/streamlit.log for details"
    cat logs/streamlit.log 2>/dev/null | tail -20
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  Services Started!                    ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "  ${GREEN}Streamlit UI:${NC}  http://localhost:8501"
echo -e "  ${GREEN}FastAPI:${NC}       http://localhost:8000"
echo -e "  ${GREEN}API Docs:${NC}      http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Run ./stop.sh to stop all services${NC}"
echo ""
