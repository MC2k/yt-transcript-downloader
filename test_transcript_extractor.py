"""
Unit tests for yt_transcript_downloader.

Run with: python -m pytest test_transcript_extractor.py
"""

import pytest
from unittest.mock import patch, MagicMock
from yt_transcript_downloader import extract_transcript_direct
from yt_transcript_downloader.transcript_extractor import (
    _extract_api_key_from_html,
    _format_transcript_no_timestamps,
)


class TestExtractApiKey:
    """Tests for API key extraction from HTML."""
    
    def test_extract_valid_api_key(self):
        """Test extracting a valid API key from HTML."""
        html = '''
        <html>
            <script>
            var config = {"INNERTUBE_API_KEY":"AIzaSyTest1234567890"}
            </script>
        </html>
        '''
        key = _extract_api_key_from_html(html)
        assert key == "AIzaSyTest1234567890"
    
    def test_extract_api_key_missing(self):
        """Test when API key is not in HTML."""
        html = "<html><body>No API key here</body></html>"
        key = _extract_api_key_from_html(html)
        assert key is None
    
    def test_extract_api_key_empty_html(self):
        """Test with empty HTML."""
        html = ""
        key = _extract_api_key_from_html(html)
        assert key is None


class TestFormatTranscript:
    """Tests for transcript formatting."""
    
    def test_format_transcript_basic(self):
        """Test basic transcript formatting."""
        captions = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0},
        ]
        
        result = _format_transcript_no_timestamps(captions)
        
        assert result["text"] == "Hello World"
        assert len(result["segments"]) == 2
        assert result["segments"][0]["text"] == "Hello"
        assert result["segments"][1]["text"] == "World"
        assert result["language"] is None
    
    def test_format_transcript_empty(self):
        """Test with empty captions."""
        captions = []
        result = _format_transcript_no_timestamps(captions)
        
        assert result["text"] == ""
        assert result["segments"] == []
    
    def test_format_transcript_with_whitespace(self):
        """Test that whitespace is handled correctly."""
        captions = [
            {"text": "  Hello  ", "start": 0.0, "duration": 1.0},
            {"text": "  World  ", "start": 1.0, "duration": 1.0},
        ]
        
        result = _format_transcript_no_timestamps(captions)
        
        # Text should be trimmed but joined with space
        assert result["text"] == "Hello World"
    
    def test_format_transcript_skip_empty_text(self):
        """Test that empty text captions are skipped."""
        captions = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "", "start": 1.0, "duration": 1.0},
            {"text": "World", "start": 2.0, "duration": 1.0},
        ]
        
        result = _format_transcript_no_timestamps(captions)
        
        assert result["text"] == "Hello World"
        assert len(result["segments"]) == 2  # Only non-empty segments


class TestVideoIdExtraction:
    """Tests for video ID extraction from URLs."""
    
    @patch('yt_transcript_downloader.transcript_extractor._fetch_transcript')
    @patch('yt_transcript_downloader.transcript_extractor._format_transcript_no_timestamps')
    def test_extract_from_standard_url(self, mock_format, mock_fetch):
        """Test extracting from standard watch URL."""
        mock_fetch.return_value = [{"text": "test", "start": 0, "duration": 1}]
        mock_format.return_value = {"text": "test", "segments": [], "language": None}
        
        url = "https://www.youtube.com/watch?v=abc123"
        result = extract_transcript_direct(url)
        
        # Verify the function was called (indicating video ID was extracted)
        assert mock_fetch.called
    
    @patch('yt_transcript_downloader.transcript_extractor._fetch_transcript')
    @patch('yt_transcript_downloader.transcript_extractor._format_transcript_no_timestamps')
    def test_extract_from_short_url(self, mock_format, mock_fetch):
        """Test extracting from youtu.be short URL."""
        mock_fetch.return_value = [{"text": "test", "start": 0, "duration": 1}]
        mock_format.return_value = {"text": "test", "segments": [], "language": None}
        
        url = "https://youtu.be/abc123"
        result = extract_transcript_direct(url)
        
        assert mock_fetch.called
    
    def test_invalid_video_id(self):
        """Test with invalid video ID."""
        url = "https://example.com/not-a-youtube-url"
        result = extract_transcript_direct(url)
        
        assert result is None
    
    def test_empty_url(self):
        """Test with empty URL."""
        result = extract_transcript_direct("")
        assert result is None


class TestIntegration:
    """Integration tests (may require network access)."""
    
    @pytest.mark.slow
    def test_real_video_extraction(self):
        """Test extraction from real YouTube video (requires network).
        
        Note: This test requires network access and may be rate-limited.
        Use a well-known video with guaranteed captions.
        """
        # Using "Me at the zoo" - first YouTube video, always has captions
        url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        
        result = extract_transcript_direct(url)
        
        # We can't guarantee success due to YouTube's protection,
        # but if it succeeds, verify the structure
        if result:
            assert "text" in result
            assert "segments" in result
            assert "language" in result
            assert isinstance(result["segments"], list)
            assert len(result["segments"]) > 0
            assert "id" in result["segments"][0]
            assert "text" in result["segments"][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
