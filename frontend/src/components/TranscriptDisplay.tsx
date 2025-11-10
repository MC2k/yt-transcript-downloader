"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { TranscriptResponse } from "@/types";
import { Copy, Download, Check } from "lucide-react";
import { useState } from "react";

interface TranscriptDisplayProps {
  data: TranscriptResponse;
}

export function TranscriptDisplay({ data }: TranscriptDisplayProps) {
  const [copied, setCopied] = useState(false);

  if (!data.success) {
    return (
      <Card className="border-destructive/50 bg-destructive/5">
        <CardHeader>
          <CardTitle className="text-destructive">Error</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">{data.error || "Failed to extract transcript"}</p>
          <p className="text-xs text-muted-foreground mt-2">
            • Check that the URL is a valid YouTube video link
          </p>
          <p className="text-xs text-muted-foreground">
            • The video may not have captions available
          </p>
          <p className="text-xs text-muted-foreground">
            • Try refreshing and try again in a few moments
          </p>
        </CardContent>
      </Card>
    );
  }

  const handleCopy = async () => {
    try {
      // Try clipboard API first if available
      if (navigator?.clipboard?.writeText) {
        await navigator.clipboard.writeText(data.text || "");
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
        return;
      }
    } catch (err) {
      console.error("Clipboard API failed:", err);
    }
    
    // Fallback: use old method
    try {
      const textarea = document.createElement("textarea");
      textarea.value = data.text || "";
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (fallbackErr) {
      console.error("Fallback copy failed:", fallbackErr);
      alert("Failed to copy transcript. Please try again.");
    }
  };

  const handleDownload = () => {
    try {
      const element = document.createElement("a");
      const file = new Blob([data.text || ""], { type: "text/plain" });
      element.href = URL.createObjectURL(file);
      element.download = `transcript-${new Date().toISOString().split('T')[0]}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      URL.revokeObjectURL(element.href);
    } catch (err) {
      console.error("Failed to download:", err);
      alert("Failed to download transcript. Please try copying to clipboard instead.");
    }
  };

  const segmentCount = data.segments?.length || 0;
  const wordCount = (data.text || "").split(/\s+/).length;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle>Transcript Extracted</CardTitle>
              <CardDescription>
                {segmentCount} segments • ~{wordCount} words
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                className="gap-2"
              >
                {copied ? (
                  <>
                    <Check className="h-4 w-4" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4" />
                    Copy
                  </>
                )}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownload}
                className="gap-2"
              >
                <Download className="h-4 w-4" />
                Download
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Full Transcript</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-muted p-4 rounded-lg max-h-96 overflow-y-auto">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {data.text}
            </p>
          </div>
        </CardContent>
      </Card>

      {data.segments && data.segments.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Segments</CardTitle>
            <CardDescription>Transcript divided into {segmentCount} parts</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-80 overflow-y-auto">
              {data.segments.map((segment) => {
                const formatTime = (seconds: number) => {
                  const mins = Math.floor(seconds / 60);
                  const secs = Math.floor(seconds % 60);
                  return `${mins}:${secs.toString().padStart(2, '0')}`;
                };
                
                return (
                  <div key={segment.id} className="p-3 bg-muted rounded-md">
                    <div className="flex items-baseline justify-between mb-2">
                      <div className="text-xs font-semibold text-muted-foreground">
                        Segment {segment.id + 1}
                      </div>
                      {segment.start !== undefined && (
                        <div className="text-xs text-muted-foreground">
                          {formatTime(segment.start)}
                        </div>
                      )}
                    </div>
                    <p className="text-sm">{segment.text}</p>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
