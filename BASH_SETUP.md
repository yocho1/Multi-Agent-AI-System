#!/bin/bash

# Quick start guide for bash users

# Make sure run.sh is executable

chmod +x ./run.sh

echo "✓ Setup complete!"
echo ""
echo "Quick start commands:"
echo ""
echo " # Install dependencies"
echo " make install"
echo ""
echo " # Run tests"
echo " make test # all tests"
echo " make test-unit # unit tests only"
echo " make test-int # integration tests"
echo ""
echo " # Start server"
echo " make dev # development (hot reload)"
echo " make run # production (4 workers)"
echo ""
echo " # Code quality"
echo " make lint # flake8"
echo " make typecheck # mypy strict"
echo " make format # black formatter"
echo ""
echo " # Or use the bash script:"
echo " ./run.sh help # show all commands"
echo " ./run.sh server # start dev server"
echo " ./run.sh test # run tests"
echo ""
