"use client";

import { useState } from "react";
import { Header } from "@/components/Header";
import { URLInput } from "@/components/URLInput";
import { TranscriptDisplay } from "@/components/TranscriptDisplay";
import { fetchTranscript } from "@/lib/api-client";
import { TranscriptResponse } from "@/types";

export default function Home() {
  const [transcript, setTranscript] = useState<TranscriptResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleExtract = async (url: string) => {
    setIsLoading(true);
    setTranscript(null);

    try {
      const result = await fetchTranscript(url);
      setTranscript(result);
    } catch (error) {
      console.error("Error:", error);
      setTranscript({
        success: false,
        error: "An unexpected error occurred. Please try again.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />

      <main className="flex-1">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
          {/* Input Section */}
          <div className="mb-8 sm:mb-12">
            <div className="mb-4">
              <p className="text-muted-foreground text-sm sm:text-base">
                Paste a YouTube link below and we&apos;ll extract the transcript for you.
              </p>
            </div>
            <URLInput onSubmit={handleExtract} isLoading={isLoading} />
          </div>

          {/* Results Section */}
          {transcript && (
            <div className="animate-in fade-in duration-300">
              <TranscriptDisplay data={transcript} />
            </div>
          )}

          {/* Empty State */}
          {!transcript && !isLoading && (
            <div className="text-center py-12 text-muted-foreground">
              <p>No transcript extracted yet.</p>
              <p className="text-sm mt-2">Enter a YouTube URL above to get started.</p>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-background">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-xs text-muted-foreground">
          <p>Made with ❤️ • Extracts transcripts from YouTube captions</p>
        </div>
      </footer>
    </div>
  );
}
