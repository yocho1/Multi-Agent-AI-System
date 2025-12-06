#!/bin/bash

# AI Agent System - Development Runner

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"

echo -e "${BLUE}=== AI Agent System ===${NC}\n"

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [command]

Commands:
  install         Install dependencies with poetry
  test            Run all unit tests
  test-unit       Run unit tests only
  test-int        Run integration tests only
  lint            Run flake8 linter
  type-check      Run mypy type checking
  format          Format code with black
  server          Start development server (port 8000)
  server-prod     Start production server
  shell           Start Python shell with environment loaded
  clean           Clean cache and temporary files
  help            Show this help message

Examples:
  $0 install
  $0 test
  $0 server
EOF
}

# Check if venv exists
check_venv() {
    if [ ! -f "$PYTHON" ]; then
        echo -e "${RED}Error: Virtual environment not found at $VENV_DIR${NC}"
        echo "Please create venv with: python -m venv .venv"
        exit 1
    fi
}

# Install dependencies
install() {
    echo -e "${GREEN}Installing dependencies...${NC}"
    check_venv
    cd "$PROJECT_DIR"
    "$PYTHON" -m poetry install --no-root
    echo -e "${GREEN}✓ Dependencies installed${NC}\n"
}

# Run tests
test_all() {
    echo -e "${GREEN}Running all tests...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    "$PYTHON" -m pytest src/tests/ -v --tb=short
}

test_unit() {
    echo -e "${GREEN}Running unit tests...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    "$PYTHON" -m pytest src/tests/unit/ -v --tb=short
}

test_int() {
    echo -e "${GREEN}Running integration tests...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    "$PYTHON" -m pytest src/tests/integration/ -v --tb=short
}

# Lint code
lint() {
    echo -e "${GREEN}Linting code...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    "$PYTHON" -m flake8 src/ --max-line-length=100
    echo -e "${GREEN}✓ Linting passed${NC}\n"
}

# Type checking
type_check() {
    echo -e "${GREEN}Type checking...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    "$PYTHON" -m mypy src/ --strict
    echo -e "${GREEN}✓ Type check passed${NC}\n"
}

# Format code
format_code() {
    echo -e "${GREEN}Formatting code...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    "$PYTHON" -m black src/ --line-length=100
    echo -e "${GREEN}✓ Code formatted${NC}\n"
}

# Start development server
server() {
    echo -e "${GREEN}Starting development server...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    echo -e "${BLUE}Server running at: http://127.0.0.1:8000${NC}"
    echo -e "${BLUE}API docs at: http://127.0.0.1:8000/docs${NC}\n"
    "$PYTHON" -m uvicorn src.main:app --reload --port 8000 --host 127.0.0.1
}

# Start production server
server_prod() {
    echo -e "${GREEN}Starting production server...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    echo -e "${BLUE}Server running at: http://127.0.0.1:8000${NC}\n"
    "$PYTHON" -m uvicorn src.main:app --port 8000 --host 0.0.0.0 --workers 4
}

# Start Python shell
shell() {
    echo -e "${GREEN}Starting Python shell...${NC}"
    check_venv
    cd "$PROJECT_DIR/ai_agent_system"
    "$PYTHON" -i << 'EOF'
from src.agents import *
from src.agents.tools import *
from src.config.settings import settings
print("Available: OrchestratorAgent, PlannerAgent, WriterAgent, FlightAgent, WeatherAgent, CodeAgent")
print("Tools: WebSearchTool, DatabaseQueryTool, CodeExecutorTool, SentimentAnalysisTool")
print("Settings:", settings)
EOF
}

# Clean cache
clean() {
    echo -e "${GREEN}Cleaning cache...${NC}"
    find "$PROJECT_DIR" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_DIR" -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_DIR" -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_DIR" -type f -name "*.pyc" -delete
    echo -e "${GREEN}✓ Cache cleaned${NC}\n"
}

# Main logic
case "${1:-help}" in
    install)
        install
        ;;
    test)
        test_all
        ;;
    test-unit)
        test_unit
        ;;
    test-int)
        test_int
        ;;
    lint)
        lint
        ;;
    type-check)
        type_check
        ;;
    format)
        format_code
        ;;
    server)
        server
        ;;
    server-prod)
        server_prod
        ;;
    shell)
        shell
        ;;
    clean)
        clean
        ;;
    help|*)
        usage
        ;;
esac
