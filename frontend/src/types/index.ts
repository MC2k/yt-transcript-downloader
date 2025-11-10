export interface TranscriptSegment {
  id: number;
  text: string;
  start?: number;
  duration?: number;
}

export interface TranscriptResponse {
  success: boolean;
  text?: string;
  segments?: TranscriptSegment[];
  language?: string;
  error?: string;
}

export interface ExtractorResult {
  text: string;
  segments: TranscriptSegment[];
  language: string | null;
}
