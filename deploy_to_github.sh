#!/bin/bash
# GitHub Deployment Script for Sol-Ark Cloud Integration
# This script will help you push the integration to your GitHub account

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Sol-Ark Cloud Integration - GitHub Deployer${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Get user information
echo -e "${YELLOW}Please provide your GitHub information:${NC}"
echo ""
read -p "GitHub username: " GITHUB_USER
read -p "Repository name (default: solark_cloud): " REPO_NAME
REPO_NAME=${REPO_NAME:-solark_cloud}

echo ""
echo -e "${GREEN}Configuration:${NC}"
echo "  GitHub User: $GITHUB_USER"
echo "  Repository: $REPO_NAME"
echo "  URL: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
read -p "Is this correct? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${RED}Deployment cancelled.${NC}"
    exit 1
fi

# Initialize git if not already done
if [ ! -d .git ]; then
    echo ""
    echo -e "${GREEN}Initializing git repository...${NC}"
    git init
    git branch -M main
else
    echo ""
    echo -e "${GREEN}Git repository already initialized.${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo -e "${GREEN}Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.tox/
.coverage
.pytest_cache/

# Project specific
*.zip
.secrets
EOF
fi

# Add all files
echo ""
echo -e "${GREEN}Adding files to git...${NC}"
git add .

# Commit
echo -e "${GREEN}Creating initial commit...${NC}"
git commit -m "Initial commit: Sol-Ark Cloud Integration v1.0.0

- Full UI configuration flow
- Options flow for easy updates
- Multi-mode authentication (Auto/Strict/Legacy)
- 8 comprehensive sensors for solar monitoring
- Complete documentation suite
- Production-ready code with error handling
- HACS compatible

Features:
- PV Power sensor
- Load Power sensor
- Grid Import/Export sensors
- Battery Power and SoC sensors
- Energy Today sensor
- Diagnostic sensors

See README.md for complete documentation."

# Add remote
echo ""
echo -e "${GREEN}Adding GitHub remote...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}IMPORTANT: Next Steps${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}1. Create the repository on GitHub:${NC}"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: ${REPO_NAME}"
echo "   - Description: Home Assistant integration for Sol-Ark Cloud solar monitoring"
echo "   - Public or Private: Your choice (Public recommended for HACS)"
echo "   - Do NOT initialize with README (we already have one)"
echo "   - Click 'Create repository'"
echo ""
echo -e "${YELLOW}2. Push to GitHub:${NC}"
echo "   Once you've created the repository, run:"
echo ""
echo -e "   ${GREEN}git push -u origin main${NC}"
echo ""
echo -e "${YELLOW}3. Create a release (optional but recommended):${NC}"
echo "   - Go to: https://github.com/$GITHUB_USER/$REPO_NAME/releases/new"
echo "   - Tag version: v1.0.0"
echo "   - Release title: Sol-Ark Cloud Integration v1.0.0"
echo "   - Description: Copy from DEPLOYMENT_SUMMARY.md"
echo "   - Attach: Run ./package.sh first, then upload generated zips"
echo "   - Click 'Publish release'"
echo ""
echo -e "${YELLOW}4. For HACS installation:${NC}"
echo "   Users can add this repository as a custom repository:"
echo "   - HACS → Integrations → Three dots → Custom repositories"
echo "   - URL: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "   - Category: Integration"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Git repository is ready!${NC}"
echo "Repository: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo -e "${YELLOW}Remember to:${NC}"
echo "  1. Create the repository on GitHub"
echo "  2. Run: git push -u origin main"
echo ""
