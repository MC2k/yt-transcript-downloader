# How to Use in Another Project

This guide explains how to copy and use `yt_transcript_downloader` in your other projects.

## Step 1: Copy the Module

Choose one method:

### Option A: Copy Entire Folder (Recommended)

```bash
# From your project directory
cp -r /path/to/yt_whisper_cli/yt_transcript_downloader ./

# Now you have:
# your_project/
# ├── yt_transcript_downloader/
# │   ├── __init__.py
# │   ├── transcript_extractor.py
# │   ├── setup.py
# │   ├── requirements.txt
# │   └── ...documentation files...
# └── your_code.py
```

### Option B: Minimal Copy (Just the Code)

If you only need the code without documentation:

```bash
# Create the module directory
mkdir -p your_project/yt_transcript_downloader

# Copy only essential files
cp /path/to/yt_whisper_cli/yt_transcript_downloader/__init__.py your_project/yt_transcript_downloader/
cp /path/to/yt_whisper_cli/yt_transcript_downloader/transcript_extractor.py your_project/yt_transcript_downloader/

# Add to your requirements.txt
echo "requests>=2.25.0" >> your_project/requirements.txt
```

### Option C: Install as Package

```bash
# From your project directory, install the package
pip install /path/to/yt_whisper_cli/yt_transcript_downloader

# Now import globally:
# from yt_transcript_downloader import extract_transcript_direct
```

## Step 2: Install Dependencies

```bash
pip install -r yt_transcript_downloader/requirements.txt

# Or just:
pip install requests
```

## Step 3: Start Using

### In Python Script

```python
from yt_transcript_downloader import extract_transcript_direct

def main():
    url = "https://www.youtube.com/watch?v=abc123"

    result = extract_transcript_direct(url)

    if result:
        print(f"Transcript ({len(result['segments'])} segments):")
        print(result['text'][:500] + "...")
    else:
        print("Could not extract transcript")

if __name__ == "__main__":
    main()
```

### In a Function

```python
from yt_transcript_downloader import extract_transcript_direct
import logging

logging.basicConfig(level=logging.INFO)

def process_video(video_url: str) -> dict:
    """Process a YouTube video and extract transcript."""

    result = extract_transcript_direct(video_url)

    if result:
        return {
            "status": "success",
            "url": video_url,
            "transcript": result['text'],
            "segments": len(result['segments']),
        }
    else:
        return {
            "status": "error",
            "url": video_url,
            "message": "Could not extract transcript"
        }

# Usage
result = process_video("https://www.youtube.com/watch?v=VIDEO_ID")
print(result)
```

### In a Web Framework

#### Flask

```python
from flask import Flask, request, jsonify
from yt_transcript_downloader import extract_transcript_direct

app = Flask(__name__)

@app.route('/api/transcript', methods=['GET'])
def get_transcript():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    result = extract_transcript_direct(url)

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Could not extract transcript'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

#### FastAPI

```python
from fastapi import FastAPI, HTTPException
from yt_transcript_downloader import extract_transcript_direct

app = FastAPI()

@app.get("/api/transcript")
async def get_transcript(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="Missing url parameter")

    result = extract_transcript_direct(url)

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Could not extract transcript")
```

### In a Data Pipeline

```python
from yt_transcript_downloader import extract_transcript_direct
import time
import csv

def extract_transcripts_from_urls(urls: list, output_file: str):
    """Extract transcripts from multiple URLs and save to CSV."""

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Status', 'Segments', 'Preview'])

        for url in urls:
            print(f"Processing: {url}")

            result = extract_transcript_direct(url)

            if result:
                preview = result['text'][:100] + "..."
                writer.writerow([
                    url,
                    'success',
                    len(result['segments']),
                    preview
                ])
            else:
                writer.writerow([url, 'failed', '', ''])

            # Important: Add delay to avoid rate limiting
            time.sleep(2)

# Usage
urls = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
]

extract_transcripts_from_urls(urls, "transcripts.csv")
```

## Configuration Examples

### Logging Configuration

```python
import logging

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcripts.log'),
        logging.StreamHandler()
    ]
)

from yt_transcript_downloader import extract_transcript_direct

result = extract_transcript_direct(url)
```

### Custom Error Handling

```python
from yt_transcript_downloader import extract_transcript_direct
import logging

logger = logging.getLogger(__name__)

def safe_extract(url: str, max_retries: int = 3) -> dict:
    """Extract transcript with custom retry logic."""

    for attempt in range(max_retries):
        try:
            result = extract_transcript_direct(url)

            if result:
                logger.info(f"Successfully extracted: {url}")
                return result
            else:
                logger.warning(f"Attempt {attempt + 1}: Could not extract {url}")

        except Exception as e:
            logger.error(f"Error extracting {url}: {e}")

        if attempt < max_retries - 1:
            import time
            time.sleep(2 ** attempt)  # Exponential backoff

    return None
```

## Project Structure Examples

### Minimal Project

```
my_project/
├── main.py
├── requirements.txt
├── yt_transcript_downloader/
│   ├── __init__.py
│   └── transcript_extractor.py
└── README.md
```

`requirements.txt`:

```
requests>=2.25.0
```

`main.py`:

```python
from yt_transcript_downloader import extract_transcript_direct

if __name__ == "__main__":
    result = extract_transcript_direct("https://www.youtube.com/watch?v=abc")
    if result:
        print(result['text'])
```

### Web Application

```
web_app/
├── app.py
├── config.py
├── requirements.txt
├── yt_transcript_downloader/
│   ├── __init__.py
│   └── transcript_extractor.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── README.md
```

### Data Science Project

```
data_science/
├── main.py
├── analysis.py
├── data/
│   └── transcripts.csv
├── notebooks/
│   └── exploration.ipynb
├── requirements.txt
├── yt_transcript_downloader/
│   ├── __init__.py
│   └── transcript_extractor.py
└── README.md
```

## Common Patterns

### Pattern 1: Simple Extraction

```python
from yt_transcript_downloader import extract_transcript_direct

url = "https://www.youtube.com/watch?v=abc123"
result = extract_transcript_direct(url)

if result:
    print(result['text'])
```

### Pattern 2: With Language Preference

```python
# German preference, fallback to English
result = extract_transcript_direct(url, language="de")

# English only
result = extract_transcript_direct(url, language="en")
```

### Pattern 3: Batch Processing

```python
import time

urls = [...]
results = {}

for url in urls:
    result = extract_transcript_direct(url)
    results[url] = result
    time.sleep(2)  # Rate limiting
```

### Pattern 4: Caching

```python
cache = {}

def get_transcript(url):
    if url not in cache:
        cache[url] = extract_transcript_direct(url)
    return cache[url]
```

### Pattern 5: Error Recovery

```python
def get_transcript_safe(url):
    result = extract_transcript_direct(url)
    return result if result else {"text": "", "segments": []}
```

## Testing in Your Project

### Simple Test

```python
from yt_transcript_downloader import extract_transcript_direct

def test_extraction():
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    result = extract_transcript_direct(url)

    assert result is not None
    assert "text" in result
    assert "segments" in result
    assert len(result["segments"]) > 0

if __name__ == "__main__":
    test_extraction()
    print("✓ Test passed!")
```

### Pytest Setup

```python
# test_transcripts.py
import pytest
from yt_transcript_downloader import extract_transcript_direct

@pytest.mark.slow
def test_youtube_extraction():
    """Test extraction from real YouTube video."""
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    result = extract_transcript_direct(url)

    if result:  # May fail if rate limited
        assert isinstance(result, dict)
        assert "text" in result
        assert len(result["segments"]) > 0
```

Run with:

```bash
pytest -v
pytest -v -m slow  # Run slow tests too
```

## Troubleshooting

### Import Error

```python
# If you get: ModuleNotFoundError: No module named 'yt_transcript_downloader'

# Solution 1: Install dependencies
pip install requests

# Solution 2: Check file is in right location
import os
print(os.path.exists("yt_transcript_downloader/__init__.py"))

# Solution 3: Add to Python path
import sys
sys.path.insert(0, "/path/to/your/project")
```

### Returns None

```python
# Enable logging to see what's happening
import logging
logging.basicConfig(level=logging.DEBUG)

result = extract_transcript_direct(url)
# Now you'll see detailed error messages
```

### Rate Limiting

```python
import time

# Make sure to add delays!
for url in urls:
    result = extract_transcript_direct(url)
    time.sleep(2)  # At minimum
    # time.sleep(5)  # Better for reliability
```

## Updates

When the module is updated in yt_whisper_cli, simply copy the new version:

```bash
cp /path/to/yt_whisper_cli/yt_transcript_downloader/transcript_extractor.py ./yt_transcript_downloader/
```

Or if using pip, reinstall:

```bash
pip install --upgrade ./yt_transcript_downloader
```

## Next Steps

1. Copy the module to your project
2. Install requirements: `pip install requests`
3. Start using: `extract_transcript_direct(url)`
4. Enable logging for debugging
5. Add delays between batch requests
6. Check examples.py for more patterns

## Support

All documentation is included:

- `README.md` - Complete reference
- `QUICKSTART.md` - Quick start guide
- `INTEGRATION_GUIDE.md` - Integration patterns
- `examples.py` - Working examples
