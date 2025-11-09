# YouTube Transcript Downloader

A standalone, dependency-free Python library for downloading YouTube transcripts (captions) directly from YouTube without requiring audio download or external transcription services.

## Features

- **Direct YouTube API Access**: Extracts transcripts directly from YouTube's internal API
- **Zero External Dependencies**: Uses only Python standard library and `requests`
- **Intelligent Language Fallback**: Attempts de → de-DE → en → en-US → en-GB → any available
- **Automatic Retry Logic**: Built-in retry mechanism with exponential backoff
- **Timestamp Stripping**: Optimizes transcripts for LLM token usage
- **Robust Error Handling**: Gracefully handles rate limiting, timeouts, and missing transcripts
- **Easy to Integrate**: Simple, intuitive API for use in other projects

## Installation

### Option 1: Copy the Module

```bash
# Copy the yt_transcript_downloader folder to your project
cp -r yt_transcript_downloader /path/to/your/project/
```

### Option 2: Install as Package

```bash
# From the parent directory of yt_transcript_downloader
pip install -e yt_transcript_downloader
```

## Requirements

- Python 3.8+
- `requests` library

```bash
pip install requests
```

## Quick Start

### Basic Usage

```python
from yt_transcript_downloader import extract_transcript_direct

# Extract transcript from YouTube URL
url = "https://www.youtube.com/watch?v=abc123"
result = extract_transcript_direct(url)

if result:
    print(f"Transcript: {result['text']}")
    print(f"Number of segments: {len(result['segments'])}")
else:
    print("Could not extract transcript")
```

### With Language Preference

```python
# Specify preferred language
result = extract_transcript_direct(url, language="de")

if result:
    print(f"Transcript: {result['text']}")
```

### Working with Segments

```python
result = extract_transcript_direct(url)

if result:
    # Iterate through segments
    for segment in result['segments']:
        segment_id = segment['id']
        text = segment['text']
        print(f"[{segment_id}] {text}")
```

## API Reference

### `extract_transcript_direct(url, language=None)`

Extracts transcript directly from YouTube using captions.

**Parameters:**

- `url` (str): Full YouTube URL (e.g., `https://www.youtube.com/watch?v=abc123`)
- `language` (str, optional): Preferred language code (e.g., `"de"`, `"en"`)

**Returns:**

- `dict` with transcript data or `None` if extraction failed:
  ```python
  {
      "text": "full transcript text",
      "segments": [
          {"id": 0, "text": "first segment"},
          {"id": 1, "text": "second segment"},
          ...
      ],
      "language": None  # Language determined by YouTube
  }
  ```

**Raises:**

- Logs warnings for various error conditions but does not raise exceptions
- Returns `None` if extraction fails

## How It Works

1. **Extract Video ID**: Parses the YouTube URL to extract the video ID
2. **Fetch Page HTML**: Retrieves the YouTube page to extract transcript parameters and API key
3. **Call YouTube API**: Uses the extracted API key to call YouTube's internal `get_transcript` endpoint
4. **Parse Response**: Converts YouTube's caption format to readable segments
5. **Format Output**: Strips timestamps to optimize for LLM token usage

## Supported URL Formats

The library supports all standard YouTube URL formats:

- `https://www.youtube.com/watch?v=abc123`
- `https://youtu.be/abc123`
- `https://www.youtube.com/embed/abc123`
- `https://www.youtube.com/watch?v=abc123&t=123s` (with timestamps)

## Logging

The library uses Python's standard `logging` module. Configure logging to see detailed information:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Or configure specific logger
logger = logging.getLogger('yt_transcript_downloader')
logger.setLevel(logging.DEBUG)
```

Log levels:

- `DEBUG`: Detailed extraction steps
- `INFO`: Successful extractions and summary info
- `WARNING`: Failures and fallbacks
- `ERROR`: Critical errors (none expected in normal operation)

## Limitations

- Only works with videos that have captions/transcripts available
- Some videos may have transcripts but YouTube protects them from API retrieval (rare)
- Language availability depends on the video's available captions
- Respects YouTube's rate limiting (automatic retry with backoff)

## Integration Examples

### In a Data Processing Pipeline

```python
from yt_transcript_downloader import extract_transcript_direct

def process_youtube_video(video_url):
    transcript = extract_transcript_direct(video_url)

    if transcript:
        # Process transcript for your use case
        full_text = transcript['text']
        # ... do something with the text ...
        return {"status": "success", "text": full_text}
    else:
        return {"status": "error", "reason": "Transcript extraction failed"}

# Usage
result = process_youtube_video("https://www.youtube.com/watch?v=abc123")
```

### In a Web Application

```python
from flask import Flask, request, jsonify
from yt_transcript_downloader import extract_transcript_direct

app = Flask(__name__)

@app.route("/api/transcript", methods=["GET"])
def get_transcript():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    transcript = extract_transcript_direct(url)

    if transcript:
        return jsonify(transcript)
    else:
        return jsonify({"error": "Could not extract transcript"}), 404
```

### Batch Processing

```python
from yt_transcript_downloader import extract_transcript_direct

urls = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
    "https://www.youtube.com/watch?v=video3",
]

transcripts = {}
for url in urls:
    result = extract_transcript_direct(url)
    transcripts[url] = result if result else None

# Process results
successful = {url: t for url, t in transcripts.items() if t}
failed = [url for url, t in transcripts.items() if not t]

print(f"Extracted {len(successful)} transcripts, {len(failed)} failed")
```

## Performance

- Transcript extraction typically takes 1-3 seconds per video
- Network request timeouts are set to 10 seconds
- Automatic retries with exponential backoff for failed requests
- No audio download required (much faster than audio-based transcription)

## Error Handling

The library handles errors gracefully:

- **Rate Limiting (429)**: Automatically retries with backoff
- **Timeout**: Logs warning and returns `None`
- **Missing Transcripts**: Returns `None`
- **Network Errors**: Retries up to 3 times
- **YouTube Protection**: Returns `None` (some videos protect their transcripts)

## Thread Safety

The module is thread-safe for multiple concurrent transcript extractions. Each call creates its own session with retry logic.

## Contributing

When integrating into your project:

1. Keep the module standalone with minimal dependencies
2. Respect YouTube's terms of service
3. Implement rate limiting if making many requests
4. Cache results when appropriate

## License

This module is provided as-is for use in your projects.

## Troubleshooting

### "Could not extract API key from HTML"

This can happen if:

- YouTube changed their HTML structure (unlikely, but possible)
- Network connectivity issues
- The page didn't load properly

**Solution**: Retry the request. Add delays between multiple requests.

### "No transcript params found in HTML"

The video doesn't have captions/transcripts available.

**Solution**: Check if the video has manual or auto-generated captions on YouTube.

### Timeout errors

Network or YouTube server slowness.

**Solution**: The library automatically retries. Check your internet connection.

### Rate limiting

Making too many requests in a short period.

**Solution**: Add delays between requests or implement batch processing with delays:

```python
import time
from yt_transcript_downloader import extract_transcript_direct

urls = [...]
for url in urls:
    result = extract_transcript_direct(url)
    time.sleep(2)  # Wait 2 seconds between requests
```

## Development

For development or modifications:

```bash
# Clone or copy the module
cd yt_transcript_downloader

# Run tests (if added)
python -m pytest tests/

# Check code quality
python -m pylint yt_transcript_downloader/
```

## See Also

- Original implementation: `yt_to_text/direct_transcript_extractor.py` in yt_whisper_cli
- YouTube API Documentation: https://developers.google.com/youtube/v3
