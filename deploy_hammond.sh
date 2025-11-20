#!/bin/bash
# GitHub Deployment Script for Sol-Ark Cloud Integration
# Pre-configured for HammondAutomationHub/HomeAssistant_SolArk

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Sol-Ark Cloud Integration - GitHub Deployer${NC}"
echo -e "${BLUE}   Repository: HammondAutomationHub/HomeAssistant_SolArk${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

GITHUB_USER="HammondAutomationHub"
REPO_NAME="HomeAssistant_SolArk"
REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo -e "${GREEN}Configuration:${NC}"
echo "  GitHub User: $GITHUB_USER"
echo "  Repository: $REPO_NAME"
echo "  URL: $REPO_URL"
echo ""

# Initialize git if not already done
if [ ! -d .git ]; then
    echo -e "${GREEN}Initializing git repository...${NC}"
    git init
    git branch -M main
else
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

Complete Home Assistant custom integration for Sol-Ark Cloud monitoring.

Features:
- Full UI configuration flow with no YAML required
- Options flow for easy settings updates
- Multi-mode authentication (Auto/Strict/Legacy)
- 8 comprehensive sensors (PV, Load, Grid, Battery, Energy)
- Production-ready code with comprehensive error handling
- Complete documentation suite
- HACS compatible

Sensors:
- PV Power (W)
- Load Power (W)  
- Grid Import/Export Power (W)
- Battery Power (W) with charge/discharge detection
- Battery State of Charge (%)
- Energy Today (kWh)
- Last Error (diagnostics)

Documentation:
- Quick Start Guide (5 minutes)
- Detailed Installation Guide
- Complete Configuration Reference
- Usage Examples with Automations
- Energy Dashboard Integration
- Comprehensive Troubleshooting

See README.md for complete documentation."

# Add remote
echo ""
echo -e "${GREEN}Adding GitHub remote...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}IMPORTANT: Next Steps${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}1. Create the repository on GitHub (if not already created):${NC}"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: ${REPO_NAME}"
echo "   - Description: Home Assistant integration for Sol-Ark Cloud solar monitoring"
echo "   - Public (recommended for HACS)"
echo "   - Do NOT initialize with README"
echo "   - Click 'Create repository'"
echo ""
echo -e "${YELLOW}2. Push to GitHub:${NC}"
echo "   Run this command:"
echo ""
echo -e "   ${GREEN}git push -u origin main${NC}"
echo ""
echo -e "${YELLOW}3. Get a Personal Access Token (if you don't have one):${NC}"
echo "   - Go to: https://github.com/settings/tokens"
echo "   - Click 'Generate new token (classic)'"
echo "   - Name: 'Home Assistant Integration'"
echo "   - Scopes: Check 'repo'"
echo "   - Click 'Generate token'"
echo "   - COPY THE TOKEN (you won't see it again!)"
echo "   - Use as password when pushing"
echo ""
echo -e "${YELLOW}4. Create a release (optional but recommended):${NC}"
echo "   - Go to: https://github.com/$GITHUB_USER/$REPO_NAME/releases/new"
echo "   - Tag version: v1.0.0"
echo "   - Release title: Sol-Ark Cloud Integration v1.0.0"
echo "   - Run ./package.sh to create distribution zips"
echo "   - Attach the generated zip files"
echo "   - Click 'Publish release'"
echo ""
echo -e "${YELLOW}5. For HACS installation:${NC}"
echo "   Users can add your repository as a custom repository:"
echo "   - HACS → Integrations → Three dots → Custom repositories"
echo "   - URL: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "   - Category: Integration"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Git repository is ready!${NC}"
echo "Repository: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo -e "${YELLOW}Next command to run:${NC}"
echo -e "${GREEN}git push -u origin main${NC}"
echo ""
