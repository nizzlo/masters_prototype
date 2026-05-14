#!/bin/bash

# Adaptive Knowledge System — Evaluation Test Runner
# Runs baseline vs adaptive vectorization experiments across all datasets
# and writes results to EVALUATION_RESULTS.md
#
# Usage:
#   ./test.sh              # run all datasets (simple + complex)
#   ./test.sh --simple     # run simple datasets only (faster, ~30s)
#   ./test.sh --complex    # run complex datasets only
#   ./test.sh --help       # show this help

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# ── colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ── help ──────────────────────────────────────────────────────────────────────
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo ""
    echo -e "${BOLD}Usage:${NC}  ./test.sh [--simple | --complex | --help]"
    echo ""
    echo "  (no flag)   Run all 6 datasets — 3 simple + 3 complex"
    echo "  --simple    Run the 3 simple datasets only (hr_policy, product_inventory, technical_manual)"
    echo "  --complex   Run the 3 complex datasets only (annual_report, employee_performance, compliance_manual)"
    echo "  --help      Show this help message"
    echo ""
    echo -e "${BOLD}Output:${NC} EVALUATION_RESULTS.md in the project root"
    echo ""
    exit 0
fi

# ── banner ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}${BOLD}============================================================${NC}"
echo -e "${BLUE}${BOLD}   Adaptive Knowledge System — Evaluation Runner${NC}"
echo -e "${BLUE}${BOLD}============================================================${NC}"
echo ""

# ── check Python / venv ───────────────────────────────────────────────────────
PYTHON=""

if [[ -f "$PROJECT_DIR/.venv/bin/python" ]]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo -e "${RED}ERROR: Python not found.${NC}"
    echo "  Create the virtual environment first:"
    echo "    python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo -e "${CYAN}Python  :${NC} $($PYTHON --version 2>&1)"
echo -e "${CYAN}Runtime :${NC} $PYTHON"

# ── check Ollama ─────────────────────────────────────────────────────────────
echo ""
echo -e "${YELLOW}Checking Ollama ...${NC}"

if ! command -v ollama &>/dev/null; then
    echo -e "${RED}ERROR: ollama not found in PATH.${NC}"
    echo "  Install from https://ollama.com or run: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

if ! curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${YELLOW}  Ollama server not running — starting it now ...${NC}"
    ollama serve &>/dev/null &
    OLLAMA_PID=$!
    sleep 3
    if ! curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo -e "${RED}ERROR: Could not start Ollama server.${NC}"
        exit 1
    fi
    echo -e "${GREEN}  Ollama started (pid $OLLAMA_PID)${NC}"
else
    echo -e "${GREEN}  Ollama is running.${NC}"
fi

# Verify embedding model is available
EMBED_MODEL="mxbai-embed-large"
if ! ollama list 2>/dev/null | grep -q "$EMBED_MODEL"; then
    echo ""
    echo -e "${YELLOW}  Embedding model '$EMBED_MODEL' not found. Pulling ...${NC}"
    ollama pull "$EMBED_MODEL"
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}ERROR: Failed to pull embedding model.${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}  Embedding model: $EMBED_MODEL ✓${NC}"

# ── select datasets mode ───────────────────────────────────────────────────────
MODE="all"
if [[ "$1" == "--simple" ]]; then MODE="simple"; fi
if [[ "$1" == "--complex" ]]; then MODE="complex"; fi

echo ""
case "$MODE" in
    all)     echo -e "${CYAN}Mode    :${NC} All datasets (3 simple + 3 complex)" ;;
    simple)  echo -e "${CYAN}Mode    :${NC} Simple datasets only" ;;
    complex) echo -e "${CYAN}Mode    :${NC} Complex datasets only" ;;
esac

# ── inject MODE into the evaluation script via env var ───────────────────────
# The evaluation script reads EVAL_MODE to skip unwanted dataset groups.
export EVAL_MODE="$MODE"

# ── run evaluation ────────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}------------------------------------------------------------${NC}"
echo -e "${BOLD}Running evaluation ...${NC}"
echo -e "${BLUE}------------------------------------------------------------${NC}"
echo ""

START_TIME=$(date +%s)

"$PYTHON" experiments/run_evaluation.py
EXIT_CODE=$?

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo ""
echo -e "${BLUE}------------------------------------------------------------${NC}"

if [[ $EXIT_CODE -ne 0 ]]; then
    echo -e "${RED}${BOLD}Evaluation FAILED (exit code $EXIT_CODE)${NC}"
    echo ""
    echo "Troubleshooting tips:"
    echo "  • Ensure dependencies are installed: pip install -r requirements.txt"
    echo "  • Check Ollama is running: ollama serve"
    echo "  • Check the embedding model: ollama pull mxbai-embed-large"
    exit $EXIT_CODE
fi

echo -e "${GREEN}${BOLD}Evaluation complete in ${ELAPSED}s${NC}"
echo ""
echo -e "${CYAN}Report :${NC} $PROJECT_DIR/EVALUATION_RESULTS.md"
echo ""
echo -e "${BOLD}Quick-open:${NC}"
echo "  open EVALUATION_RESULTS.md          # macOS"
echo "  cat  EVALUATION_RESULTS.md | head -80"
echo ""
