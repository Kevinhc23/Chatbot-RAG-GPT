"use client";
import { useState, useRef, useCallback } from "react";
import { ChatMessage, ChatResponse } from "@/app/types";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const controller = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (question: string) => {
      if (isLoading) return; // Evitar múltiples requests

      setIsLoading(true);
      const userMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
      };
      setMessages((m) => [...m, userMsg]);

      // Agregar mensaje de "pensando" para mejorar UX
      const thinkingMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Pensando...",
        images: [],
        videos: [],
      };
      setMessages((m) => [...m, thinkingMsg]);

      controller.current?.abort();
      controller.current = new AbortController();

      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question }),
          signal: controller.current.signal,
        });

        if (!res.ok) {
          throw new Error(`Error del servidor: ${res.status}`);
        }

        const payload: ChatResponse = await res.json();

        // Reemplazar mensaje de "pensando" con la respuesta real
        setMessages((m) =>
          m.map((msg) =>
            msg.id === thinkingMsg.id
              ? {
                  ...msg,
                  content: payload.answer,
                  images: payload.images || [],
                  videos: payload.videos || [],
                }
              : msg
          )
        );
      } catch (error) {
        console.error("Error enviando mensaje:", error);
        // Reemplazar mensaje de "pensando" con error
        setMessages((m) =>
          m.map((msg) =>
            msg.id === thinkingMsg.id
              ? {
                  ...msg,
                  content:
                    "Lo siento, ocurrió un error al procesar tu pregunta.",
                }
              : msg
          )
        );
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading]
  );

  return { messages, sendMessage, isLoading };
}
