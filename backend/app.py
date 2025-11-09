"""Flask API wrapper for YouTube Transcript Downloader.

This module provides a simple HTTP API for the transcript extractor.
"""

import logging
import sys
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path to import transcript_extractor
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from transcript_extractor import extract_transcript_direct

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes - more permissive for development
cors_config = {
    "origins": ["*"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"],
}
CORS(app, resources={r"/api/*": cors_config}, supports_credentials=True)

# Configure app
app.config['JSON_SORT_KEYS'] = False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "YouTube Transcript Downloader API"
    }), 200


@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    """
    Extract transcript from YouTube video.
    
    Request body:
    {
        "url": "https://www.youtube.com/watch?v=...",
        "language": "en"  # Optional
    }
    
    Response:
    {
        "success": true,
        "text": "Full transcript...",
        "segments": [{"id": 0, "text": "..."}, ...],
        "language": null
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        url = data.get('url', '').strip()
        language = data.get('language')
        
        if not url:
            return jsonify({
                "success": False,
                "error": "URL is required"
            }), 400
        
        logger.info(f"Extracting transcript from: {url}")
        
        # Extract transcript
        result = extract_transcript_direct(url, language=language)
        
        if result is None:
            return jsonify({
                "success": False,
                "error": "Failed to extract transcript. The video may not have captions available."
            }), 422
        
        logger.info(f"Successfully extracted {len(result['segments'])} segments")
        
        return jsonify({
            "success": True,
            "text": result['text'],
            "segments": result['segments'],
            "language": result.get('language')
        }), 200
    
    except Exception as e:
        logger.error(f"Error extracting transcript: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    import os
    
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    logger.info(f"Starting YouTube Transcript Downloader API on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
