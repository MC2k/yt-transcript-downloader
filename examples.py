"""
Example usage of yt_transcript_downloader.

This script demonstrates various ways to use the transcript extraction library.
"""

import logging
from yt_transcript_downloader import extract_transcript_direct

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def example_basic_usage():
    """Basic example: Extract transcript from a single URL."""
    print("\n=== Example 1: Basic Usage ===")
    
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    print(f"Extracting transcript from: {url}")
    
    result = extract_transcript_direct(url)
    
    if result:
        print(f"✓ Success!")
        print(f"  - Segments: {len(result['segments'])}")
        print(f"  - Words: {len(result['text'].split())}")
        print(f"  - Preview: {result['text'][:200]}...")
    else:
        print("✗ Failed to extract transcript")


def example_with_language():
    """Example: Specify preferred language."""
    print("\n=== Example 2: With Language Preference ===")
    
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    print(f"Extracting transcript with German language preference")
    
    result = extract_transcript_direct(url, language="de")
    
    if result:
        print(f"✓ Success!")
        print(f"  - Segments: {len(result['segments'])}")
        print(f"  - Language: {result['language']}")
    else:
        print("✗ Failed to extract transcript (video may not have German captions)")


def example_working_with_segments():
    """Example: Work with segments."""
    print("\n=== Example 3: Working with Segments ===")
    
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    result = extract_transcript_direct(url)
    
    if result:
        print(f"First 5 segments:")
        for segment in result['segments'][:5]:
            print(f"  [{segment['id']:3d}] {segment['text']}")
        
        if len(result['segments']) > 5:
            print(f"  ... and {len(result['segments']) - 5} more segments")
    else:
        print("✗ Failed to extract transcript")


def example_batch_processing():
    """Example: Process multiple URLs with error handling."""
    print("\n=== Example 4: Batch Processing ===")
    
    urls = [
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "https://youtu.be/jNQXAC9IVRw",  # Different URL format
    ]
    
    results = {}
    for url in urls:
        print(f"Processing: {url}")
        result = extract_transcript_direct(url)
        results[url] = result
    
    # Summary
    successful = sum(1 for r in results.values() if r)
    failed = len(results) - successful
    
    print(f"\nSummary: {successful} successful, {failed} failed")


def example_error_handling():
    """Example: Handle errors gracefully."""
    print("\n=== Example 5: Error Handling ===")
    
    test_urls = [
        ("Valid URL", "https://www.youtube.com/watch?v=jNQXAC9IVRw"),
        ("Invalid video ID", "https://www.youtube.com/watch?v=invalid"),
        ("Invalid URL", "https://example.com"),
    ]
    
    for name, url in test_urls:
        print(f"\nTesting: {name} - {url}")
        result = extract_transcript_direct(url)
        
        if result:
            print(f"  ✓ Extracted {len(result['segments'])} segments")
        else:
            print(f"  ✗ Could not extract transcript")


if __name__ == "__main__":
    print("YouTube Transcript Downloader - Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_with_language()
    example_working_with_segments()
    example_batch_processing()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
