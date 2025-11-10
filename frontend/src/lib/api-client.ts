import { TranscriptResponse } from "@/types";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:5000";

export async function fetchTranscript(url: string): Promise<TranscriptResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/transcript`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const error = await response.json();
      return {
        success: false,
        error: error.error || "Failed to fetch transcript",
      };
    }

    const data = await response.json();
    return data;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
    return {
      success: false,
      error: `Network error: ${errorMessage}`,
    };
  }
}

export function isValidYouTubeURL(url: string): boolean {
  try {
    const urlObj = new URL(url);
    const hostname = urlObj.hostname;

    // Check if it's a YouTube URL
    const isYouTube =
      hostname.includes("youtube.com") ||
      hostname.includes("youtu.be") ||
      hostname.includes("youtube.be");

    if (!isYouTube) return false;

    // Extract video ID
    const videoIdMatch =
      url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/) ||
      url.match(/youtube\.com\/embed\/([^&\n?#]+)/);

    return videoIdMatch && videoIdMatch[1] ? videoIdMatch[1].length === 11 : false;
  } catch {
    return false;
  }
}
