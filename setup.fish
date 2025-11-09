#!/usr/bin/env fish

# YouTube Transcript Downloader - Setup Script
# This script sets up both the frontend and backend

set script_dir (dirname (status filename))
set project_root (dirname $script_dir)

echo "🚀 YouTube Transcript Downloader Setup"
echo "======================================"
echo ""

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd $project_root/backend
pip install -r requirements.txt
if test $status -ne 0
    echo "❌ Failed to install backend dependencies"
    exit 1
end
echo "✅ Backend dependencies installed"
echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd $project_root/frontend
npm install
if test $status -ne 0
    echo "❌ Failed to install frontend dependencies"
    exit 1
end
echo "✅ Frontend dependencies installed"
echo ""

echo "✨ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend - Flask API):"
echo "  cd $project_root"
echo "  python -m flask --app backend.app run"
echo ""
echo "Terminal 2 (Frontend - Next.js):"
echo "  cd $project_root/frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser"
