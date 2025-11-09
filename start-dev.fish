#!/usr/bin/env fish

# YouTube Transcript Downloader - Quick Start
# This script starts both backend and frontend

set project_root (dirname (status filename))

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  YouTube Transcript Downloader - Development Setup    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if venv exists
if not test -d "$project_root/venv"
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please run the setup first:"
    echo "  ./setup.fish"
    exit 1
end

# Start Backend
echo "🚀 Starting Backend (Flask API on port 8000)..."
cd $project_root
source venv/bin/activate.fish
python -m flask --app backend.app run --port 8000 &
set backend_pid $!
echo "   Backend PID: $backend_pid"
sleep 2

# Start Frontend
echo "🚀 Starting Frontend (Next.js on port 3001)..."
cd $project_root/frontend
npm run dev &
set frontend_pid $!
echo "   Frontend PID: $frontend_pid"
sleep 3

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                   ✨ Ready to Use!                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Frontend:  http://localhost:3001"
echo "Backend:   http://localhost:8000"
echo "Health:    http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Wait for processes
wait
