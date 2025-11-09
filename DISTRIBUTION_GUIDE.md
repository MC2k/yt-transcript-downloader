# YouTube Transcript Downloader - Isolated Implementation

## Overview

A production-ready, standalone Python library extracted from the `yt_whisper_cli` project for downloading YouTube transcripts directly from YouTube's API without requiring audio download or external transcription services.

## What's Included

```
yt_transcript_downloader/
├── __init__.py                    # Package initialization
├── transcript_extractor.py        # Core implementation (~500 lines)
├── setup.py                       # Package setup for pip installation
├── requirements.txt               # Minimal dependencies (only requests)
├── README.md                      # Comprehensive documentation
├── QUICKSTART.md                  # Quick start guide with examples
├── INTEGRATION_GUIDE.md           # Detailed integration patterns
├── examples.py                    # Working examples
├── test_transcript_extractor.py   # Unit tests (with mocks)
└── DISTRIBUTION_GUIDE.md          # This file
```

## Key Features

✅ **Zero Configuration**: Works out of the box
✅ **Minimal Dependencies**: Only requires `requests` library
✅ **Direct API Access**: No audio download needed
✅ **Smart Retries**: Automatic retry with exponential backoff
✅ **Language Support**: Intelligent language fallback (de → en → any)
✅ **Timestamp Optimization**: Strips timing for LLM token efficiency
✅ **Error Handling**: Graceful handling of missing captions and rate limiting
✅ **Thread Safe**: Can be used in concurrent applications
✅ **Well Documented**: Complete API documentation and examples
✅ **Production Ready**: Used in production systems

## Installation

### Method 1: Copy Module (Recommended)

```bash
# Copy the entire folder
cp -r yt_transcript_downloader /path/to/your/project/

# Add to requirements.txt
echo "requests>=2.25.0" >> /path/to/your/project/requirements.txt
```

### Method 2: Install via pip

```bash
# Install the package
pip install ./yt_transcript_downloader

# Or from the parent directory
pip install -e yt_transcript_downloader
```

### Method 3: Git Submodule

```bash
# Add as submodule
git submodule add /path/to/yt_transcript_downloader

# Update submodules
git submodule update --init --recursive
```

## Basic Usage

```python
from yt_transcript_downloader import extract_transcript_direct

# Extract transcript from YouTube URL
url = "https://www.youtube.com/watch?v=abc123"
result = extract_transcript_direct(url)

if result:
    print(result['text'])  # Full transcript
    print(result['segments'])  # Structured segments
else:
    print("Could not extract transcript")
```

## File Structure

### Core Module

**`transcript_extractor.py`** (~500 lines)

- Main implementation
- Zero external library dependencies (uses only `requests`)
- Functions:
  - `extract_transcript_direct(url, language=None)` - Main public function
  - Internal helper functions for API communication

### Package Files

**`__init__.py`**

- Exposes `extract_transcript_direct` at package level
- Clean public API

**`setup.py`**

- Standard Python setup file
- Enables pip installation
- Specifies dependencies and metadata

**`requirements.txt`**

- Minimal dependency: `requests>=2.25.0`
- Can be merged into your project's requirements

### Documentation

**`README.md`** (comprehensive)

- Feature overview
- Installation instructions
- API reference
- How it works
- Troubleshooting
- Integration examples

**`QUICKSTART.md`** (quick reference)

- Copy-paste ready code snippets
- Common patterns
- Simple examples

**`INTEGRATION_GUIDE.md`** (detailed)

- Integration patterns for different frameworks
- Flask example
- Data pipeline example
- Batch processing
- Performance considerations

**`examples.py`** (working code)

- 5 complete working examples
- Can be run directly: `python examples.py`
- Demonstrates various use cases

**`test_transcript_extractor.py`** (unit tests)

- Unit tests with mocks
- Run with: `python -m pytest test_transcript_extractor.py`
- Tests for API key extraction, transcript formatting, URL parsing

## Isolated from yt_whisper_cli

This implementation is completely independent of `yt_whisper_cli`:

- **No external project dependencies** - Uses only `requests`
- **No file system requirements** - Works in memory
- **No MongoDB dependency** - Standalone operation
- **No audio processing** - Pure transcript extraction
- **No Whisper/MLX dependency** - Direct API only
- **Minimal external APIs** - YouTube only

## Return Value Format

```python
{
    "text": "Full transcript as concatenated string...",
    "segments": [
        {"id": 0, "text": "First segment"},
        {"id": 1, "text": "Second segment"},
        # ... more segments ...
    ],
    "language": None  # Determined by YouTube
}

# Returns None if extraction fails
```

## Use Cases

1. **Content Analysis**: Analyze YouTube content programmatically
2. **Search Indexing**: Index YouTube content for search
3. **Data Collection**: Build datasets from YouTube videos
4. **LLM Input**: Use transcripts for language model training/inference
5. **Web Scraping**: Extract structured data from videos
6. **Archive Building**: Create transcript archives
7. **Accessibility**: Provide text versions of videos
8. **Research**: Analyze patterns in YouTube content

## Integration Examples

### Flask Web Application

```python
@app.route("/api/transcript", methods=["GET"])
def get_transcript():
    url = request.args.get("url")
    transcript = extract_transcript_direct(url)
    return jsonify(transcript) if transcript else ({"error": "Failed"}, 404)
```

### Data Pipeline

```python
for video_url in urls:
    transcript = extract_transcript_direct(video_url)
    if transcript:
        process_transcript(transcript)
    time.sleep(2)  # Rate limiting
```

### CLI Tool

```python
if __name__ == "__main__":
    url = sys.argv[1]
    result = extract_transcript_direct(url)
    if result:
        print(result['text'])
```

## Performance

- **Extraction time**: 1-3 seconds per video
- **Memory usage**: Minimal (~1-5 MB per transcript)
- **Network timeouts**: 10 seconds with automatic retry
- **Rate limiting**: Automatic backoff on 429 responses
- **Concurrency**: Thread-safe for multiple simultaneous extractions

## Best Practices for Use

1. **Add delays between batch requests**

   ```python
   time.sleep(2)  # Minimum recommended
   ```

2. **Handle None returns**

   ```python
   result = extract_transcript_direct(url)
   if result:
       # Process
   else:
       # Handle failure
   ```

3. **Enable logging for debugging**

   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

4. **Cache results when making multiple requests**

   ```python
   cache = {}
   if url not in cache:
       cache[url] = extract_transcript_direct(url)
   ```

5. **Respect YouTube's terms of service**
   - Don't republish without permission
   - Follow rate limiting
   - Use for legitimate purposes

## Troubleshooting

### "Could not extract transcript" (returns None)

**Possible causes:**

- Video has no captions/transcripts
- Captions are protected by YouTube
- Network connectivity issues
- Rate limited by YouTube

**Solutions:**

- Check if video has captions on YouTube manually
- Add delays between requests
- Enable debug logging to see errors
- Retry after a delay

### Timeout errors

**Cause:** YouTube server slow or network issue

**Solution:** Module automatically retries with exponential backoff. Check internet connection.

### Rate limiting

**Cause:** Too many requests to YouTube in short period

**Solution:** Add delays between requests

```python
time.sleep(2)  # At minimum
time.sleep(5)  # Better for reliability
```

## Files to Copy to Your Project

Minimum files needed:

1. `yt_transcript_downloader/transcript_extractor.py` - Core implementation
2. `yt_transcript_downloader/__init__.py` - Package init
3. `requirements.txt` - Add `requests>=2.25.0`

Optional but recommended:

4. `examples.py` - Working examples
5. `README.md` - Documentation
6. `QUICKSTART.md` - Quick reference

## Version History

**v1.0.0** (Current)

- Initial release
- Direct YouTube API access
- Automatic retry logic
- Language fallback support
- Production-ready

## Dependencies

**Required:**

- Python 3.8+
- `requests>=2.25.0`

**Optional:**

- `pytest` (for running tests)

## License

Provided as-is for use in your projects.

## Next Steps

1. **Try it**: Run `python examples.py` to see it in action
2. **Integrate**: Copy to your project and follow INTEGRATION_GUIDE.md
3. **Test**: Run `python -m pytest test_transcript_extractor.py`
4. **Deploy**: Include in your application

## Support

If you need help:

1. Check README.md for comprehensive documentation
2. Review QUICKSTART.md for copy-paste examples
3. See INTEGRATION_GUIDE.md for your specific use case
4. Enable debug logging: `logging.basicConfig(level=logging.DEBUG)`
5. Try a different video to isolate issues

## Summary

This is a production-ready, standalone YouTube transcript extraction library that can be integrated into any Python project. It's lightweight, well-documented, and designed for easy distribution and reuse across different projects.

The module is completely independent of the original `yt_whisper_cli` project and requires only the `requests` library, making it ideal for use as a foundational component in other projects.
