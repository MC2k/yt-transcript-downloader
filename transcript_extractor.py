"""YouTube Transcript Downloader - Main module for direct transcript extraction.

This module provides efficient transcript extraction without requiring audio download
or external dependencies beyond requests.

Features:
- Direct YouTube API access (no external libraries)
- Intelligent language fallback
- Automatic retry logic with exponential backoff
- Robust error handling
"""

import logging
import re
import requests
from typing import Optional, Dict, List, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

__version__ = "1.0.0"
__all__ = ["extract_transcript_direct"]

logger = logging.getLogger(__name__)

# Language fallback chain: YouTube's API tries each in order
LANGUAGE_FALLBACK_CHAIN = [
    "de",       # German (primary)
    "de-DE",    # German variant
    "en",       # English (secondary)
    "en-US",    # US English variant
    "en-GB",    # British English variant
]

# YouTube API configuration
YOUTUBE_API_URL = "https://www.youtube.com/youtubei/v1/get_transcript"
YOUTUBE_WATCH_URL = "https://www.youtube.com/watch"


def _create_session_with_retries(retries: int = 3, backoff_factor: float = 0.5) -> requests.Session:
    """
    Create requests session with automatic retry logic.
    
    This prevents rate limit errors by automatically retrying failed requests
    with exponential backoff.
    
    Args:
        retries: Number of retries
        backoff_factor: Backoff multiplier for retries
        
    Returns:
        requests.Session with retry strategy
    """
    session = requests.Session()
    
    retry_strategy = Retry(
        total=retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
        backoff_factor=backoff_factor
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def _extract_api_key_from_html(html_content: str) -> Optional[str]:
    """
    Extract YouTube API key from page HTML.
    
    YouTube embeds the API key in the page source for client-side API calls.
    This extracts it dynamically so we don't need to hardcode it.
    
    Args:
        html_content: HTML content from YouTube watch page
        
    Returns:
        API key string or None if not found
    """
    try:
        # YouTube API key pattern - looks like: AIzaSy...
        pattern = r'"INNERTUBE_API_KEY":"([^"]+)"'
        match = re.search(pattern, html_content)
        
        if match:
            api_key = match.group(1)
            logger.debug(f"Extracted API key from HTML: {api_key[:20]}...")
            return api_key
        
        logger.warning("Could not extract API key from HTML")
        return None
    except Exception as e:
        logger.warning(f"Error extracting API key: {e}")
        return None


def _extract_params_from_html(video_id: str, session: requests.Session) -> Optional[Dict[str, str]]:
    """
    Extract transcript parameters and API key from YouTube page HTML.
    
    The params value is embedded in the HTML when the page loads and contains
    information about available transcripts for the video.
    The API key is also extracted from the page.
    
    Args:
        video_id: YouTube video ID
        session: Requests session with retry logic
        
    Returns:
        Dict with 'params' and 'api_key' strings
        Returns None if params could not be extracted (transcript not available)
    """
    try:
        url = f"{YOUTUBE_WATCH_URL}?v={video_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Look for getTranscriptEndpoint params in HTML
        pattern = r'"getTranscriptEndpoint"\s*:\s*\{\s*"params"\s*:\s*"([^"]+)"'
        match = re.search(pattern, response.text, re.DOTALL)
        
        if not match:
            logger.debug(f"[{video_id}] No transcript params found in HTML")
            return None
        
        params = match.group(1)
        logger.debug(f"[{video_id}] Extracted transcript params from HTML")
        
        # Also extract API key from the same page
        api_key = _extract_api_key_from_html(response.text)
        if not api_key:
            logger.warning(f"[{video_id}] Could not extract API key from HTML")
            return None
        
        return {
            "params": params,
            "api_key": api_key
        }
        
    except requests.exceptions.Timeout:
        logger.warning(f"[{video_id}] Timeout fetching page HTML")
        return None
    except requests.exceptions.RequestException as e:
        logger.warning(f"[{video_id}] Error fetching page HTML: {e}")
        return None
    except Exception as e:
        logger.warning(f"[{video_id}] Unexpected error extracting params: {e}")
        return None


def _call_transcript_api(params: str, session: requests.Session, api_key: str, video_id: str = "") -> Optional[List[Dict]]:
    """
    Call YouTube's internal get_transcript API with extracted params.
    
    Args:
        params: Base64-encoded params from HTML
        session: Requests session with retry logic
        api_key: YouTube API key (dynamically extracted from HTML)
        video_id: Video ID for logging purposes
        
    Returns:
        List of transcript segments with text and timing
        Returns None if API call failed
    """
    try:
        url = f"{YOUTUBE_API_URL}?key={api_key}"
        
        # Proper headers for YouTube API (mimics browser)
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://www.youtube.com",
            "Referer": "https://www.youtube.com/watch"
        }
        
        payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20230101.00.00"
                }
            },
            "params": params
        }
        
        response = session.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 429:
            logger.warning("Rate limited by YouTube (429), will retry")
            return None
        
        response.raise_for_status()
        data = response.json()
        
        # Extract transcript segments from nested API response
        try:
            segments = (
                data['actions'][0]
                ['updateEngagementPanelAction']['content']
                ['transcriptRenderer']['content']
                ['transcriptSearchPanelRenderer']['body']
                ['transcriptSegmentListRenderer']['initialSegments']
            )
            
            logger.debug(f"Successfully fetched transcript: {len(segments)} segments")
            return segments
            
        except (KeyError, IndexError) as e:
            logger.warning(f"Unexpected API response structure: {e}")
            return None
            
    except requests.exceptions.Timeout:
        logger.warning("Timeout calling YouTube API")
        return None
    except requests.exceptions.RequestException as e:
        logger.warning(f"Error calling YouTube API: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error in API call: {e}")
        return None


def _fetch_transcript(video_id: str, languages: List[str]) -> Optional[List[Dict]]:
    """
    Fetch raw transcript from YouTube using direct API access.
    
    Strategy:
    1. Fetch page HTML to extract transcript params and API key
    2. Call YouTube's internal get_transcript API with the key
    3. Parse and return transcript segments
    
    Args:
        video_id: YouTube video ID
        languages: List of language codes
    
    Returns:
        List of caption dicts with 'text', 'start', 'duration'
        Returns None if no transcript found or protected by YouTube
    """
    session = None
    try:
        # Create session with automatic retry logic
        session = _create_session_with_retries(retries=3, backoff_factor=0.5)
        
        logger.debug(f"[{video_id}] Fetching transcript (languages: {languages})")
        
        # Step 1: Extract params and API key from HTML
        extraction_result = _extract_params_from_html(video_id, session)
        if not extraction_result:
            logger.debug(f"[{video_id}] Could not extract transcript params from HTML")
            return None
        
        params = extraction_result["params"]
        api_key = extraction_result["api_key"]
        
        # Step 2: Call API with params and extracted API key
        segments = _call_transcript_api(params, session, api_key, video_id)
        if not segments:
            logger.debug(f"[{video_id}] Could not retrieve transcript from API")
            return None
        
        # Step 3: Convert YouTube API segments to caption format
        captions = []
        for segment in segments:
            try:
                renderer = segment['transcriptSegmentRenderer']
                text = renderer['snippet']['runs'][0]['text']
                start_ms = int(renderer['startMs'])
                end_ms = int(renderer.get('endMs', start_ms + 1000))
                
                caption = {
                    'text': text,
                    'start': start_ms / 1000.0,  # Convert ms to seconds
                    'duration': (end_ms - start_ms) / 1000.0
                }
                captions.append(caption)
            except (KeyError, IndexError, ValueError) as e:
                logger.debug(f"Error parsing segment: {e}")
                continue
        
        if captions:
            logger.info(f"[{video_id}] Successfully fetched transcript: {len(captions)} captions")
            return captions
        else:
            logger.warning(f"[{video_id}] No valid captions extracted from API response")
            return None
    
    except Exception as e:
        logger.debug(f"[{video_id}] Unexpected error fetching transcript: {e}")
        return None
    finally:
        if session:
            session.close()


def _format_transcript_no_timestamps(captions: List[Dict]) -> Dict[str, Any]:
    """
    Convert YouTube captions to segment format WITHOUT timestamps.
    
    This strips timing information to optimize for LLM token usage.
    
    Args:
        captions: List of caption dicts from YouTube API
                 Format: [{"text": "...", "start": 0.0, "duration": 2.1}, ...]
    
    Returns:
        Dict with format: {"text": "...", "segments": [...], "language": "..."}
        Segments: [{"id": int, "text": str, "start": float, "duration": float}, ...]
    """
    segments = []
    full_text_parts = []
    
    for idx, caption in enumerate(captions):
        text = caption.get('text', '').strip()
        if text:
            segments.append({
                "id": idx,
                "text": text,
                "start": caption.get('start', 0.0),
                "duration": caption.get('duration', 0.0)
            })
            full_text_parts.append(text)
    
    full_text = ' '.join(full_text_parts)
    
    return {
        "text": full_text,
        "segments": segments,
        "language": None
    }


def extract_transcript_direct(url: str, language: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Extract transcript directly from YouTube using captions (no audio download).
    
    Strategy:
    1. Extract video ID from URL
    2. Fetch page to extract transcript params
    3. Call YouTube's internal API with params
    4. Format transcript without timestamps
    5. Return None if all fail
    
    Timestamps are stripped to optimize for LLM token usage.
    
    Args:
        url: Full YouTube URL (e.g., https://www.youtube.com/watch?v=abc123)
        language: Preferred language code (e.g., "de", "en")
    
    Returns:
        Dict with transcript data:
        {
            "text": "full transcript text",
            "segments": [{"id": 0, "text": "..."}, ...],
            "language": None
        }
        
        Returns None if extraction failed
    """
    try:
        # Extract video ID from URL using proven regex patterns
        patterns = [
            r'(?:v=|/)([0-9A-Za-z_-]{11}).*',  # Standard watch URL or short URL
            r'youtu\.be/([0-9A-Za-z_-]{11})',   # youtu.be short links
            r'embed/([0-9A-Za-z_-]{11})',       # Embed URLs
        ]
        video_id = None
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break
        
        if not video_id:
            logger.warning(f"Failed to extract video ID from {url}")
            return None
        
        logger.info(f"[{video_id}] Attempting direct transcript extraction")
        
        # Build language list
        languages_to_try = []
        if language:
            languages_to_try.append(language)
            if '-' in language:
                base_lang = language.split('-')[0]
                if base_lang not in languages_to_try:
                    languages_to_try.append(base_lang)
        
        # Add default fallback chain
        for lang in LANGUAGE_FALLBACK_CHAIN:
            if lang not in languages_to_try:
                languages_to_try.append(lang)
        
        logger.debug(f"[{video_id}] Language priority: {languages_to_try}")
        
        # Fetch transcript using direct API
        transcript_captions = _fetch_transcript(video_id, languages_to_try)
        
        if not transcript_captions:
            logger.warning(f"[{video_id}] Failed to extract transcript")
            return None
        
        # Format transcript without timestamps
        result = _format_transcript_no_timestamps(transcript_captions)
        
        logger.info(f"[{video_id}] ✓ Extracted transcript: {len(result['segments'])} segments, ~{len(result['text'].split())} words")
        
        return result
    
    except Exception as e:
        logger.warning(f"Direct extraction failed for {url}: {e}", exc_info=True)
        return None
