#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Store current directory
ROOT_DIR=$(pwd)

# Build Frontend
cd web
npm install
npm run build

# Return to root and copy artifacts (if needed, though api/main.py reads directly from web/dist)
# ensure web/dist exists in root context if api expects it
cd "$ROOT_DIR"
