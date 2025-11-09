"""Package initialization for yt_transcript_downloader.

Provides convenient access to the transcript extraction functionality.
"""

from .transcript_extractor import extract_transcript_direct

__version__ = "1.0.0"
__all__ = ["extract_transcript_direct"]
