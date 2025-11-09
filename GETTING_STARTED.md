# 🚀 YouTube Transcript Downloader - Getting Started

## ⚡ Quick Start (60 seconds)

### 1. First Time Setup

```bash
# Install dependencies (one time only)
./setup.fish
```

### 2. Start the Application

**Option A: Automatic (Recommended)**

```bash
./start-dev.fish
```

**Option B: Manual (Two terminals)**

Terminal 1 - Backend:

```bash
cd backend
source ../venv/bin/activate.fish
python -m flask --app app run --port 8000
```

Terminal 2 - Frontend:

```bash
cd frontend
npm run dev
```

### 3. Open in Browser

Navigate to: **http://localhost:3001**

---

## 📋 What's Running

| Service      | URL                          | Purpose                   |
| ------------ | ---------------------------- | ------------------------- |
| Frontend     | http://localhost:3001        | Next.js web interface     |
| Backend API  | http://localhost:8000        | Flask API server          |
| Health Check | http://localhost:8000/health | Verify backend is working |

---

## ✅ Verify Everything Works

### Test 1: Backend Health

```bash
curl http://localhost:8000/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "service": "YouTube Transcript Downloader API"
}
```

### Test 2: Frontend Loads

Open http://localhost:3001 in your browser

You should see:

- Header with "YouTube Transcript Downloader"
- Light/Dark mode toggle
- Input field for YouTube URL
- Empty state message

### Test 3: Extract a Transcript

1. Paste this YouTube URL: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
2. Click "Extract"
3. Wait 3-10 seconds
4. See the transcript appear below

---

## 🐛 Troubleshooting

### Issue: "Connection refused" on frontend

**Solution:** Make sure backend is running

```bash
# Check if backend is running
ps aux | grep flask

# If not, start it
source venv/bin/activate.fish
python -m flask --app backend.app run --port 8000
```

### Issue: "Port 3001 already in use"

**Solution:** Kill the process using that port

```bash
lsof -i :3001
kill -9 <PID>

# Then restart frontend
npm run dev
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Activate virtual environment first

```bash
source venv/bin/activate.fish
python -m flask --app backend.app run --port 8000
```

### Issue: YouTube video has no captions

The extractor only works if the video has captions. Try another video that definitely has captions (most popular videos do).

---

## 📁 Project Layout

```
.
├── frontend/              # Next.js 15 React app
│   ├── src/
│   │   ├── app/
│   │   ├── components/    # URLInput, TranscriptDisplay, Header
│   │   ├── lib/          # API client utilities
│   │   └── types/        # TypeScript interfaces
│   └── package.json
│
├── backend/              # Flask Python API
│   ├── app.py           # Main Flask application
│   └── requirements.txt
│
├── venv/                 # Python virtual environment
├── transcript_extractor.py  # Core extraction logic
├── setup.fish            # Initial setup script
└── start-dev.fish        # Start both services
```

---

## 🛠️ Development Tips

### Hot Reload

Both frontend and backend support hot reload:

- **Frontend**: Changes to `.tsx` files automatically refresh
- **Backend**: Changes to `.py` files automatically restart (when debug=True)

### View Backend Logs

Check the terminal running the Flask server for request logs and errors.

### Debug Frontend Issues

Open browser DevTools (F12) and check:

- Console tab for JavaScript errors
- Network tab to see API requests to `http://localhost:8000/api/transcript`

### Database/Storage

Currently, the app stores nothing. Each extraction is fresh. Transcripts are not saved.

---

## 📚 API Documentation

### Health Check

```bash
GET /health

curl http://localhost:8000/health
```

### Extract Transcript

```bash
POST /api/transcript
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=...",
  "language": "en"  // Optional, defaults to de → en fallback
}
```

**Success Response:**

```json
{
  "success": true,
  "text": "Full transcript text here...",
  "segments": [
    { "id": 0, "text": "First segment" },
    { "id": 1, "text": "Second segment" }
  ],
  "language": null
}
```

**Error Response:**

```json
{
  "success": false,
  "error": "Failed to extract transcript. The video may not have captions available."
}
```

---

## 🌍 Deployment

### Frontend (Vercel)

```bash
# Automatic deployment
# Just push to GitHub and connect to Vercel
# Update NEXT_PUBLIC_BACKEND_URL to your production API
```

### Backend (Railway, Heroku, AWS)

```bash
# Build and deploy to your hosting
# Update CORS and allowed origins for production
```

---

## ❓ FAQ

**Q: Why port 8000 instead of 5000?**
A: macOS uses port 5000 for AirTunes. Port 8000 avoids conflicts.

**Q: Can I run the frontend and backend on different machines?**
A: Yes! Update `NEXT_PUBLIC_BACKEND_URL` in `frontend/.env.local` to point to your backend URL.

**Q: How do I use this in production?**
A: See `SETUP_AND_RUN.md` section "Building for Production"

**Q: Is there a database?**
A: No, the app doesn't persist data. Transcripts are extracted fresh each time.

---

## 📞 Support

Check these files for more info:

- `SETUP_AND_RUN.md` - Detailed setup and API docs
- `README.md` - Feature overview
- `transcript_extractor.py` - Core extraction logic

---

**Happy extracting! 🎥✨**
