"use client";
import { ChatMessage } from "@/app/types";
import { useAuth } from "@/contexts/AuthContext";
import { useCallback, useEffect, useRef, useState } from "react";

interface ChatSession {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message_preview?: string;
}

interface ChatResponse {
  answer: string;
  images?: string[];
  videos?: string[];
  session_id: number;
}

interface SessionResponse {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  messages: ChatMessage[];
}

export function useChatWithHistory() {
  const { token, handleAuthError } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const controller = useRef<AbortController | null>(null);

  // Crear headers con autenticación
  const getAuthHeaders = useCallback(() => {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    return headers;
  }, [token]);

  // Cargar sesiones al inicializar
  const loadSessions = useCallback(async () => {
    if (!token) return; // No cargar si no hay token

    setLoadingSessions(true);
    try {
      const res = await fetch(
        `${
          process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
        }/history/sessions`,
        {
          headers: getAuthHeaders(),
        }
      );
      if (res.ok) {
        const sessionsData = await res.json();
        setSessions(sessionsData);
      } else {
        handleAuthError(res);
      }
    } catch (error) {
      console.error("Error cargando sesiones:", error);
    } finally {
      setLoadingSessions(false);
    }
  }, [token, getAuthHeaders]);

  // Cargar mensajes de una sesión específica
  const loadSession = useCallback(
    async (sessionId: number) => {
      if (!token) return;

      try {
        const res = await fetch(
          `${
            process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
          }/history/sessions/${sessionId}`,
          {
            headers: getAuthHeaders(),
          }
        );
        if (res.ok) {
          const sessionData: SessionResponse = await res.json();
          setMessages(sessionData.messages);
          setCurrentSessionId(sessionId);
        } else {
          handleAuthError(res);
        }
      } catch (error) {
        console.error("Error cargando sesión:", error);
      }
    },
    [token, getAuthHeaders]
  );

  // Crear nueva sesión
  const createNewSession = useCallback(() => {
    setMessages([]);
    setCurrentSessionId(null);
  }, []);

  // Eliminar sesión
  const deleteSession = useCallback(
    async (sessionId: number) => {
      if (!token) return;

      try {
        const res = await fetch(
          `${
            process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
          }/history/sessions/${sessionId}`,
          {
            method: "DELETE",
            headers: getAuthHeaders(),
          }
        );
        if (res.ok) {
          setSessions((prev) => prev.filter((s) => s.id !== sessionId));
          if (currentSessionId === sessionId) {
            createNewSession();
          }
        } else {
          handleAuthError(res);
        }
      } catch (error) {
        console.error("Error eliminando sesión:", error);
      }
    },
    [token, currentSessionId, createNewSession, getAuthHeaders]
  );

  // Actualizar título de sesión
  const updateSessionTitle = useCallback(
    async (sessionId: number, newTitle: string) => {
      if (!token) return;

      try {
        const res = await fetch(
          `${
            process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
          }/history/sessions/${sessionId}/title`,
          {
            method: "PUT",
            headers: getAuthHeaders(),
            body: JSON.stringify({ title: newTitle }),
          }
        );
        if (res.ok) {
          setSessions((prev) =>
            prev.map((s) =>
              s.id === sessionId ? { ...s, title: newTitle } : s
            )
          );
        } else {
          handleAuthError(res);
        }
      } catch (error) {
        console.error("Error actualizando título:", error);
      }
    },
    [token, getAuthHeaders]
  );

  // Enviar mensaje
  const sendMessage = useCallback(
    async (question: string) => {
      if (isLoading || !token) return;

      setIsLoading(true);
      const userMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
      };
      setMessages((m) => [...m, userMsg]);

      // Agregar mensaje de "pensando"
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
        const res = await fetch(
          `${
            process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
          }/chat-history`,
          {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({
              question,
              session_id: currentSessionId,
            }),
            signal: controller.current.signal,
          }
        );

        if (!res.ok) {
          handleAuthError(res);
          throw new Error(`Error del servidor: ${res.status}`);
        }

        const payload: ChatResponse = await res.json();

        // Actualizar session_id si es una nueva sesión
        if (!currentSessionId) {
          setCurrentSessionId(payload.session_id);
          // Recargar la lista de sesiones
          loadSessions();
        }

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
    [isLoading, currentSessionId, loadSessions, token, getAuthHeaders]
  );

  // Cargar sesiones al montar el componente y cuando cambie el token
  useEffect(() => {
    if (token) {
      loadSessions();
    }
  }, [loadSessions, token]);

  return {
    messages,
    isLoading,
    currentSessionId,
    sessions,
    loadingSessions,
    sendMessage,
    loadSession,
    createNewSession,
    deleteSession,
    updateSessionTitle,
    loadSessions,
  };
}
