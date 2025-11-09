"""
Quick start guide for yt_transcript_downloader.

This file contains simple, copy-paste ready examples.
"""

# ==============================================================================

# INSTALLATION

# ==============================================================================

# Option 1: Direct copy (recommended for single projects)

# cp -r yt_transcript_downloader /path/to/your/project/

# Option 2: Install as package

# pip install requests

# Then copy the folder to your project

# ==============================================================================

# BASIC USAGE

# ==============================================================================

from yt_transcript_downloader import extract_transcript_direct

# Extract transcript from YouTube URL

url = "https://www.youtube.com/watch?v=abc123"
result = extract_transcript_direct(url)

if result:
print(result['text']) # Full transcript text
else:
print("Could not extract transcript")

# ==============================================================================

# WITH LANGUAGE PREFERENCE

# ==============================================================================

result = extract_transcript_direct(url, language="de")

if result: # Work with segments
for segment in result['segments']:
print(f"{segment['id']}: {segment['text']}")

# ==============================================================================

# ERROR HANDLING

# ==============================================================================

import logging

# Enable debug logging to see detailed information

logging.basicConfig(level=logging.INFO)

result = extract_transcript_direct(url)
if result:
print(f"Transcript: {len(result['segments'])} segments")
else:
print("Extraction failed - check logs for details")

# ==============================================================================

# BATCH PROCESSING

# ==============================================================================

import time

urls = [
"https://www.youtube.com/watch?v=video1",
"https://www.youtube.com/watch?v=video2",
"https://www.youtube.com/watch?v=video3",
]

transcripts = {}
for url in urls:
result = extract_transcript_direct(url)
transcripts[url] = result

    # Add delay to avoid rate limiting
    time.sleep(2)

# Process results

for url, transcript in transcripts.items():
if transcript:
print(f"{url}: {len(transcript['segments'])} segments")
else:
print(f"{url}: FAILED")

# ==============================================================================

# INTEGRATION IN FLASK APP

# ==============================================================================

# from flask import Flask, request, jsonify

# from yt_transcript_downloader import extract_transcript_direct

#

# app = Flask(**name**)

#

# @app.route("/api/transcript", methods=["GET"])

# def get_transcript():

# url = request.args.get("url")

# if not url:

# return jsonify({"error": "Missing url parameter"}), 400

#

# transcript = extract_transcript_direct(url)

#

# if transcript:

# return jsonify(transcript)

# else:

# return jsonify({"error": "Could not extract transcript"}), 404

# ==============================================================================

# RETURN VALUE FORMAT

# ==============================================================================

# extract_transcript_direct() returns a dict like this:

# {

# "text": "full transcript concatenated...",

# "segments": [

# {"id": 0, "text": "first segment"},

# {"id": 1, "text": "second segment"},

# {"id": 2, "text": "third segment"},

# ...

# ],

# "language": None # Language determined by YouTube

# }

#

# Returns None if extraction fails

# ==============================================================================

# SUPPORTED URL FORMATS

# ==============================================================================

# All these URLs work:

urls = [
"https://www.youtube.com/watch?v=abc123",
"https://youtu.be/abc123",
"https://www.youtube.com/embed/abc123",
"https://www.youtube.com/watch?v=abc123&t=30s",
]

for url in urls:
result = extract_transcript_direct(url) # ...

# ==============================================================================

# RATE LIMITING

# ==============================================================================

# YouTube rate limits heavily! Add delays between requests:

import time

urls = ["url1", "url2", "url3"]

for url in urls:
result = extract_transcript_direct(url) # ... process result ...

    # IMPORTANT: Add delay to avoid rate limiting
    time.sleep(2)  # Wait 2 seconds between requests

# ==============================================================================

# TROUBLESHOOTING

# ==============================================================================

# Enable detailed logging:

import logging
logging.basicConfig(level=logging.DEBUG)

result = extract_transcript_direct(url)

# Now you'll see detailed information about what's happening

# Common issues:

# 1. Returns None: Video doesn't have captions or transcript is protected

# 2. Timeout: Network issue or YouTube server slow - automatically retries

# 3. Rate limiting: Make too many requests too fast - add delays between requests
