# Integration Guide

This guide explains how to integrate `yt_transcript_downloader` into your projects.

## Installation Options

### Option 1: Copy Module (Recommended)

Simply copy the `yt_transcript_downloader` folder to your project:

```bash
cp -r yt_transcript_downloader /path/to/your/project/
```

Then import it:

```python
from yt_transcript_downloader import extract_transcript_direct
```

**Pros:**

- No setup required
- Single, standalone module
- Easy to modify if needed
- Can be committed directly to your repo

**Cons:**

- Need to manually manage updates if the module changes

### Option 2: Install as Package

From the directory containing `yt_transcript_downloader`:

```bash
# Install in development mode (editable)
pip install -e yt_transcript_downloader

# Or install directly
pip install ./yt_transcript_downloader
```

Then import normally:

```python
from yt_transcript_downloader import extract_transcript_direct
```

**Pros:**

- Standard Python package installation
- Easy to share across projects
- Can be published to PyPI

**Cons:**

- Requires pip installation
- Need to manage package versions

## Quick Integration

### 1. Basic Setup

```python
from yt_transcript_downloader import extract_transcript_direct

# Extract transcript
result = extract_transcript_direct("https://www.youtube.com/watch?v=VIDEO_ID")

if result:
    print(result['text'])
```

### 2. With Error Handling

```python
import logging
from yt_transcript_downloader import extract_transcript_direct

logging.basicConfig(level=logging.INFO)

url = "https://www.youtube.com/watch?v=VIDEO_ID"
result = extract_transcript_direct(url)

if result:
    # Successfully extracted
    transcript_text = result['text']
    segments = result['segments']
    print(f"Extracted {len(segments)} segments")
else:
    # Failed to extract
    print("Could not extract transcript from this video")
```

### 3. Language-Specific Extraction

```python
# German preference
result = extract_transcript_direct(url, language="de")

# English preference
result = extract_transcript_direct(url, language="en")
```

### 4. Batch Processing

```python
import time
from yt_transcript_downloader import extract_transcript_direct

video_urls = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
    "https://www.youtube.com/watch?v=video3",
]

results = {}
for url in video_urls:
    result = extract_transcript_direct(url)
    results[url] = result

    # Important: Add delay to avoid YouTube rate limiting
    time.sleep(2)

# Process results
for url, transcript in results.items():
    if transcript:
        print(f"{url}: {len(transcript['segments'])} segments")
```

## Common Integration Patterns

### Web Application (Flask)

```python
from flask import Flask, request, jsonify
from yt_transcript_downloader import extract_transcript_direct

app = Flask(__name__)

@app.route('/api/transcript', methods=['GET'])
def get_transcript():
    """Endpoint to extract transcripts."""
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    transcript = extract_transcript_direct(url)

    if transcript:
        return jsonify(transcript)
    else:
        return jsonify({'error': 'Could not extract transcript'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

Usage:

```bash
curl "http://localhost:5000/api/transcript?url=https://www.youtube.com/watch?v=VIDEO_ID"
```

### Data Processing Pipeline

```python
from yt_transcript_downloader import extract_transcript_direct
import logging

logger = logging.getLogger(__name__)

def process_youtube_url(url: str) -> dict:
    """Process a YouTube URL and extract transcript."""

    logger.info(f"Processing: {url}")

    # Extract transcript
    transcript = extract_transcript_direct(url)

    if not transcript:
        logger.warning(f"Failed to extract transcript from {url}")
        return {"status": "error", "url": url}

    # Process transcript
    text = transcript['text']
    segments = transcript['segments']

    # Your processing logic here
    word_count = len(text.split())

    return {
        "status": "success",
        "url": url,
        "word_count": word_count,
        "segment_count": len(segments),
        "text": text,
    }

# Usage
urls = ["https://www.youtube.com/watch?v=VIDEO1", ...]
results = [process_youtube_url(url) for url in urls]
```

### Content Analysis

```python
from yt_transcript_downloader import extract_transcript_direct
from collections import Counter
import re

def analyze_transcript(url: str) -> dict:
    """Analyze a YouTube transcript."""

    result = extract_transcript_direct(url)
    if not result:
        return None

    text = result['text']

    # Word frequency
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)

    # Sentiment analysis (example with a hypothetical library)
    # from sentiment_lib import analyze
    # sentiment = analyze(text)

    return {
        'total_words': len(words),
        'unique_words': len(set(words)),
        'top_words': word_freq.most_common(10),
        'segments': len(result['segments']),
    }

# Usage
analysis = analyze_transcript("https://www.youtube.com/watch?v=VIDEO_ID")
print(analysis)
```

### Database Storage

```python
import sqlite3
from yt_transcript_downloader import extract_transcript_direct
from datetime import datetime

def save_transcript_to_db(url: str, db_path: str = "transcripts.db"):
    """Extract and save transcript to SQLite database."""

    # Extract transcript
    result = extract_transcript_direct(url)
    if not result:
        return False

    # Save to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            text TEXT,
            segments_count INTEGER,
            extracted_at TIMESTAMP
        )
    ''')

    cursor.execute('''
        INSERT OR REPLACE INTO transcripts (url, text, segments_count, extracted_at)
        VALUES (?, ?, ?, ?)
    ''', (url, result['text'], len(result['segments']), datetime.now()))

    conn.commit()
    conn.close()

    return True

# Usage
urls = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
]

for url in urls:
    if save_transcript_to_db(url):
        print(f"Saved: {url}")
```

## Return Value Structure

The `extract_transcript_direct()` function returns a dictionary or `None`:

```python
{
    "text": "Full transcript as single concatenated string...",
    "segments": [
        {"id": 0, "text": "First segment of text"},
        {"id": 1, "text": "Second segment of text"},
        {"id": 2, "text": "Third segment of text"},
        # ... more segments ...
    ],
    "language": None  # Language code (currently None, determined by YouTube)
}
```

Or `None` if extraction failed.

## Performance Considerations

### Response Time

- Single extraction: 1-3 seconds per video
- Network request timeout: 10 seconds
- Includes automatic retries for failed requests

### Rate Limiting

YouTube rate limits API access heavily:

```python
import time

urls = [...]
for url in urls:
    result = extract_transcript_direct(url)

    # IMPORTANT: Wait between requests
    time.sleep(2)  # Recommended minimum
    # time.sleep(5)  # Better for batch processing
```

### Memory Usage

- Minimal memory footprint
- Transcript is stored entirely in memory
- For large batch processing, consider storing results incrementally

### Optimization Tips

1. **Batch Processing**: Group requests with delays

   ```python
   for url in urls:
       extract_transcript_direct(url)
       time.sleep(2)
   ```

2. **Caching**: Store results to avoid re-extracting

   ```python
   cache = {}
   for url in urls:
       if url not in cache:
           cache[url] = extract_transcript_direct(url)
   ```

3. **Async Processing** (if using async framework):

   ```python
   import asyncio

   async def async_extract(url):
       # Run in executor to avoid blocking
       return extract_transcript_direct(url)

   # Usage with aiohttp or similar
   ```

## Troubleshooting Integration Issues

### Import Errors

```python
# If you get: ModuleNotFoundError: No module named 'yt_transcript_downloader'

# Option 1: Install requirements
pip install requests

# Option 2: Check path
import sys
sys.path.insert(0, '/path/to/yt_transcript_downloader')

# Option 3: Install as package
pip install -e ./yt_transcript_downloader
```

### Network Issues

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see detailed network debugging
result = extract_transcript_direct(url)
```

### Rate Limiting

```python
# YouTube returns 429 (Too Many Requests) if rate limited
# The module automatically retries with backoff
# If still failing, increase delays:

import time

for url in urls:
    result = extract_transcript_direct(url)
    time.sleep(5)  # Increase delay
```

### Missing Captions

```python
result = extract_transcript_direct(url)
if result is None:
    # Video either:
    # 1. Has no captions/transcripts
    # 2. Has captions but they're protected from API access (rare)
    # 3. Network error occurred
```

## Logging Setup

```python
import logging

# Basic setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Detailed debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcript_debug.log'),
        logging.StreamHandler()
    ]
)

# Get logger for the module
logger = logging.getLogger('yt_transcript_downloader')
logger.setLevel(logging.DEBUG)
```

## Next Steps

1. **Try the Examples**: Run `python examples.py` to see it in action
2. **Check QUICKSTART.md**: Copy-paste ready code snippets
3. **Read README.md**: Comprehensive documentation
4. **Run Tests**: `python -m pytest test_transcript_extractor.py`

## Support & Issues

If you encounter issues:

1. Check the logs (enable DEBUG level)
2. Verify the YouTube URL has captions
3. Check network connectivity
4. Try a different video to isolate the issue
5. Wait a bit before retrying (YouTube rate limiting)

For detailed error messages, enable logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Best Practices

1. **Always use delays between batch requests**

   ```python
   time.sleep(2)  # At minimum
   ```

2. **Handle None returns gracefully**

   ```python
   result = extract_transcript_direct(url)
   if result:
       # Process
   else:
       # Handle failure
   ```

3. **Cache results when possible**

   ```python
   cache = {}
   if url not in cache:
       cache[url] = extract_transcript_direct(url)
   ```

4. **Respect YouTube's terms of service**

   - Don't republish content without permission
   - Follow rate limiting guidelines
   - Use transcripts for legitimate purposes

5. **Log failures for debugging**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```
