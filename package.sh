#!/bin/bash
# Package Sol-Ark Cloud integration for distribution

# Set version
VERSION="1.0.0"
PACKAGE_NAME="solark_cloud"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Sol-Ark Cloud Integration Packager${NC}"
echo -e "${BLUE}Version: ${VERSION}${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create dist directory
echo -e "${GREEN}Creating distribution directory...${NC}"
mkdir -p dist
rm -rf dist/${PACKAGE_NAME}
mkdir -p dist/${PACKAGE_NAME}

# Copy integration files
echo -e "${GREEN}Copying integration files...${NC}"
cp -r custom_components/${PACKAGE_NAME} dist/

# Copy documentation
echo -e "${GREEN}Copying documentation...${NC}"
cp README.md dist/
cp INSTALLATION.md dist/
cp CONFIGURATION.md dist/
cp LICENSE dist/

# Create HACS-compatible structure
echo -e "${GREEN}Creating HACS structure...${NC}"
mkdir -p dist/custom_components
mv dist/${PACKAGE_NAME} dist/custom_components/

# Create zip for manual installation
echo -e "${GREEN}Creating zip archive...${NC}"
cd dist
zip -r ${PACKAGE_NAME}_v${VERSION}.zip custom_components/${PACKAGE_NAME}/* README.md INSTALLATION.md CONFIGURATION.md LICENSE
cd ..

# Create HACS zip (just the integration folder)
echo -e "${GREEN}Creating HACS zip archive...${NC}"
cd dist/custom_components
zip -r ../${PACKAGE_NAME}_hacs_v${VERSION}.zip ${PACKAGE_NAME}/*
cd ../..

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Packaging Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Created files:"
echo "  - dist/${PACKAGE_NAME}_v${VERSION}.zip (Full package)"
echo "  - dist/${PACKAGE_NAME}_hacs_v${VERSION}.zip (HACS package)"
echo ""
echo "To install manually:"
echo "  1. Extract ${PACKAGE_NAME}_v${VERSION}.zip"
echo "  2. Copy custom_components/${PACKAGE_NAME} to <config>/custom_components/"
echo "  3. Restart Home Assistant"
echo ""
echo "For HACS:"
echo "  1. Use the GitHub repository directly"
echo "  2. Or upload ${PACKAGE_NAME}_hacs_v${VERSION}.zip to a release"
echo ""
