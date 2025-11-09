# YouTube Transcript Downloader - Full Stack Application

A modern web application for extracting YouTube transcripts instantly. Built with Next.js 15 frontend and Python Flask backend.

## 🎯 Features

- ✅ **Simple UI** - Clean, minimal interface for pasting YouTube links
- ✅ **Fast Extraction** - Direct YouTube API access (no audio download)
- ✅ **Dark/Light Mode** - Theme switcher with persistence
- ✅ **Responsive Design** - Works perfectly on mobile and desktop
- ✅ **Copy & Download** - Copy transcript to clipboard or download as .txt
- ✅ **Error Handling** - Helpful error messages for common issues
- ✅ **Modern Stack** - Next.js 15, TypeScript, Tailwind CSS, shadcn/ui

## 🛠️ Tech Stack

### Frontend

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality React components
- **next-themes** - Dark/Light mode support

### Backend

- **Python 3.8+** - Core language
- **Flask** - Lightweight HTTP API framework
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **requests** - HTTP library for YouTube access

## 📋 Prerequisites

- **Node.js 18+** - For Next.js frontend
- **Python 3.8+** - For Flask backend
- **npm** or **yarn** - JavaScript package manager
- **pip** - Python package manager

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Run setup script (macOS/Linux with fish shell)
./setup.fish

# Or manually:

# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Start the Backend (Terminal 1)

```bash
cd backend
python -m flask --app app run --port 8000
```

The API will be available at `http://localhost:8000`

**Expected output:**

```
 * Running on http://127.0.0.1:8000
```

### 3. Start the Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

The application will open at `http://localhost:3001` (or `http://localhost:3000` if port 3000 is available)

### 4. Use the Application

1. Navigate to `http://localhost:3001`
2. Paste a YouTube URL (e.g., `https://www.youtube.com/watch?v=...`)
3. Click "Extract"
4. View, copy, or download the transcript

## 📁 Project Structure

```
yt_transcript_downloader/
├── frontend/                    # Next.js 15 application
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx      # Root layout with theme provider
│   │   │   ├── page.tsx        # Main home page
│   │   │   └── api/
│   │   │       └── transcript/
│   │   │           └── route.ts # (Optional) Server-side API proxy
│   │   ├── components/
│   │   │   ├── Header.tsx      # App header with theme toggle
│   │   │   ├── URLInput.tsx    # URL input form
│   │   │   ├── TranscriptDisplay.tsx # Results display
│   │   │   └── providers.tsx   # Theme provider wrapper
│   │   ├── lib/
│   │   │   └── api-client.ts   # Fetch utilities
│   │   ├── types/
│   │   │   └── index.ts        # TypeScript interfaces
│   │   └── globals.css         # Tailwind styles
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── .env.local              # Environment variables
│
├── backend/                     # Flask API
│   ├── app.py                  # Flask application
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Backend environment variables (optional)
│
├── transcript_extractor.py     # Core extraction logic (unchanged)
├── requirements.txt            # Original Python requirements
├── setup.fish                  # Setup script
└── README.md                   # This file
```

## 🌐 API Documentation

### Health Check

```bash
GET http://localhost:5000/health

Response:
{
  "status": "healthy",
  "service": "YouTube Transcript Downloader API"
}
```

### Health Check

```bash
GET http://localhost:8000/health

Response:
{
  "status": "healthy",
  "service": "YouTube Transcript Downloader API"
}
```

### Extract Transcript

```bash
POST http://localhost:8000/api/transcript

Request:
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "language": "en"  // Optional
}

Response (Success):
{
  "success": true,
  "text": "Never gonna give you up...",
  "segments": [
    {"id": 0, "text": "Never gonna give you up"},
    {"id": 1, "text": "Never gonna let you down"},
    ...
  ],
  "language": null
}

Response (Error):
{
  "success": false,
  "error": "Failed to extract transcript. The video may not have captions available."
}
```

## 🔧 Configuration

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# For production:
# NEXT_PUBLIC_BACKEND_URL=https://api.yourdomain.com
```

### Backend Environment Variables (Optional)

Create `backend/.env`:

```env
# Flask configuration
FLASK_ENV=development
PORT=8000

# For production:
# FLASK_ENV=production
# PORT=8000
```

## 🎨 Customization

### Change Backend Port

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

Then start backend on port 8000:

```bash
python -m flask --app app run --port 8000
```

### Change Frontend Port

Start frontend on custom port:

```bash
cd frontend
npm run dev -- -p 3001
```

## 📦 Building for Production

### Frontend

```bash
cd frontend
npm run build
npm run start
```

Deploy to Vercel:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Backend

Create production environment:

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with production server (Gunicorn recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Deploy options:

- **Heroku**: `heroku create my-transcript-api && git push heroku main`
- **Railway.app**: Connect GitHub repo and deploy
- **AWS/GCP/Azure**: Use container deployment

## 🐛 Troubleshooting

### "Cannot find module 'flask'"

```bash
pip install flask flask-cors
```

### "CORS error" in browser console

Make sure the backend is running and `.env.local` has the correct `NEXT_PUBLIC_BACKEND_URL`.

### "Failed to extract transcript"

- Verify the YouTube URL is valid
- Check if the video has captions available
- Some videos may have region-restricted captions
- Try a different video

### Port already in use

```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

## 📝 License

Same license as the main `yt_transcript_downloader` project.

## 🤝 Contributing

Contributions welcome! Please ensure:

- Code follows project style guidelines
- Tests pass
- Documentation is updated

## ❓ FAQ

**Q: Does this require API keys?**
A: No! The extractor uses YouTube's public API endpoints embedded in web pages.

**Q: How long does extraction take?**
A: Usually 2-5 seconds depending on video length and network speed.

**Q: Which YouTube URLs are supported?**
A: `youtube.com/watch?v=...`, `youtu.be/...`, and embed URLs.

**Q: Can I extract transcripts in other languages?**
A: Yes! Pass `"language": "de"` in the request to prefer German, etc.

**Q: Will this work if the video has no captions?**
A: No, the video must have captions available for extraction to work.

---

Made with ❤️ by extracting YouTube transcripts intelligently
