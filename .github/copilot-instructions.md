---
# Copilot Instructions for yt_transcript_downloader
---

## Project Overview

## Coding Guidelines

- Use clear, descriptive variable and function names.
- Prefer type hints in Python for better readability and maintainability.
- For React/Next.js, use functional components and hooks.
- Keep logic modular: separate data processing, API calls, and UI components.
- Write concise, informative comments for complex logic.

## Frontend Overview

The frontend is built using **Next.js 15** with React, providing a modern, responsive user-friendly interface for displaying AI-generated blog posts. Key features:

- **Responsive Design**: Mobile-first approach with hamburger menu on mobile, full navigation on desktop
- **JWT Authentication**: Session-based login with httpOnly cookies
- **Dark/Light Mode**: Theme persistence with next-themes
- **Component Library**: shadcn/ui components built on Radix UI
- **Tailwind CSS**: Modern, utility-first styling

## Best Practices

- For new features, add tests and update documentation
- New documentation should be created in the docs/ directory
- Use environment variables for sensitive data (API keys, etc.)
- Keep dependencies up-to-date in `requirements.txt` and `package.json`
- Migration scripts should be saved in the 'mirgration_scripts/' directory

## Copilot Usage

- When generating code, prefer existing project conventions
- For new scripts, follow the structure and naming of existing files
- For frontend changes, ensure compatibility with Tailwind CSS and Next.js routing
- For backend changes, ensure compatibility with current transcript and blog formats
- create a summary document only if requested!
- one final summary document at the end of all phases only if requested!
- use fish-compatible syntax for the terminal commands
- skip the excessive summaries and focus on actionable work!
- Don't test with inline Python using heredocs (e.g., `python - << 'PY'...`)
- heredocs is not allowed anywhere in this repository! it will break things!
- in this repository use ./python to run python scripts
- in this repository, always create separate test scripts for complex tests in the folder `tests_scripts/`
