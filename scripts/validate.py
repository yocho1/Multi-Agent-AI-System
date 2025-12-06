#!/usr/bin/env python
"""
Validation script to verify the AI Agent System structure and imports.
Run with: python scripts/validate.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def validate_imports() -> None:
    """Validate all key modules can be imported."""
    modules_to_check = [
        # Config
        ("src.config.settings", "Settings"),
        ("src.config.logging_config", "setup_logging"),
        # Base abstractions
        ("src.agents.base.agent", "BaseAgent"),
        ("src.agents.base.tool", "BaseTool"),
        ("src.agents.base.memory", "BaseMemory"),
        # Specialized agents
        ("src.agents.specialized", "WriterAgent"),
        ("src.agents.specialized", "FlightAgent"),
        ("src.agents.specialized", "WeatherAgent"),
        ("src.agents.specialized", "CodeAgent"),
        # Core agents
        ("src.agents.orchestrator", "OrchestratorAgent"),
        ("src.agents.planner", "PlannerAgent"),
        # Utils
        ("src.utils.clients", "ClientManager"),
        ("src.utils.auth", "create_access_token"),
        ("src.utils.health", "health_summary"),
        ("src.utils.metrics", "metrics_response"),
        ("src.utils.tracing", "initialize_tracing"),
        # API
        ("src.api", "router"),
        ("src.api.middleware", "APIKeyMiddleware"),
    ]

    print("🔍 Validating imports...\n")
    passed = 0
    failed = 0

    for module_name, symbol_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[symbol_name])
            getattr(module, symbol_name)
            print(f"✅ {module_name}.{symbol_name}")
            passed += 1
        except Exception as exc:
            print(f"❌ {module_name}.{symbol_name}: {exc}")
            failed += 1

    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


def validate_structure() -> None:
    """Validate directory structure."""
    print("\n🏗️  Validating directory structure...\n")

    required_dirs = [
        "ai_agent_system/src/agents/base",
        "ai_agent_system/src/agents/tools",
        "ai_agent_system/src/api/endpoints",
        "ai_agent_system/src/api/middleware",
        "ai_agent_system/src/config",
        "ai_agent_system/src/utils",
        "ai_agent_system/src/tests/unit",
        "ai_agent_system/src/tests/integration",
        "docker",
        "docs",
    ]

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} (missing)")

    required_files = [
        "pyproject.toml",
        "Makefile",
        "README.md",
        ".env.example",
        ".gitignore",
        ".pre-commit-config.yaml",
        "docker/Dockerfile",
        "docker/docker-compose.yml",
        "docs/api.md",
        "docs/architecture.md",
        ".github/workflows/ci.yml",
    ]

    print()
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")


def main() -> int:
    """Run all validations."""
    print("=" * 60)
    print("🤖 AI Agent System Validation")
    print("=" * 60)

    validate_structure()

    try:
        success = validate_imports()
        return 0 if success else 1
    except Exception as exc:
        print(f"\n❌ Validation failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
