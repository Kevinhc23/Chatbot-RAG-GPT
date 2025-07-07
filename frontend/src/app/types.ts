export interface ChatResponse {
  answer: string;
  images: string[];
  videos: string[];
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  images?: string[];
  videos?: string[];
}
