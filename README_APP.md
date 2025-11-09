# 🎬 YouTube Transcript Downloader - Full Stack App

Extract YouTube transcripts instantly. Built with **Next.js 15** + **Flask**.

## ⚡ Quick Start

```bash
# 1. First time setup
./setup.fish

# 2. Start everything
./start-dev.fish

# 3. Open browser
http://localhost:3001
```

## 🎯 What It Does

- Paste a YouTube URL
- Click "Extract"
- Get the transcript instantly
- Copy or download as .txt

## 📁 What You Have

```
├── frontend/          # Next.js 15 web app (PORT 3001)
├── backend/           # Flask API (PORT 8000)
├── venv/             # Python virtual environment
├── setup.fish        # One-time setup
└── start-dev.fish    # Start dev servers
```

## 🚀 Running

**Terminal 1 - Backend:**

```bash
source venv/bin/activate.fish
python -m flask --app backend.app run --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

Then open: **http://localhost:3001**

## 📚 Docs

- **[GETTING_STARTED.md](./GETTING_STARTED.md)** - Quick start guide
- **[SETUP_AND_RUN.md](./SETUP_AND_RUN.md)** - Detailed setup
- **[README.md](./README.md)** - Original project info

## 🛠️ Tech Stack

- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind, shadcn/ui
- **Backend:** Flask, Python 3.8+
- **Features:** Dark mode, copy/download, responsive design

## ✨ Features

✅ Extract YouTube transcripts  
✅ Copy to clipboard  
✅ Download as .txt  
✅ Dark/Light mode  
✅ Mobile responsive  
✅ Real-time validation

## 🐛 Troubleshooting

**Port in use?**

```bash
lsof -i :8000
kill -9 <PID>
```

**ModuleNotFoundError?**

```bash
source venv/bin/activate.fish
```

**CORS error?**

- Make sure backend is running on port 8000
- Check `.env.local` has correct backend URL

## 🚀 Deploy

**Frontend (Vercel):**

```bash
npm run build
vercel deploy
```

**Backend (Railway/Heroku):**

- Deploy Python app with Flask
- Set environment variables
- Update frontend URL

That's it! 🎉

---

For more details, see **GETTING_STARTED.md** or **SETUP_AND_RUN.md**
