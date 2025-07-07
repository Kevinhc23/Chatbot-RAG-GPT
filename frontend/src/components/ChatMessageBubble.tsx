"use client";
import { FC } from "react";
import { ChatMessage } from "@/app/types";
import { User, Bot } from "lucide-react";

export const ChatMessageBubble: FC<{ message: ChatMessage }> = ({
  message,
}) => {
  const isUser = message.role === "user";
  const isThinking = message.content === "Pensando...";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div className="flex flex-col items-start gap-2 max-w-[75%]">
        <div className="flex items-end gap-3 w-full">
          {/* Avatar del asistente (solo cuando no es usuario) */}
          {!isUser && (
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
          )}

          {/* Burbuja de mensaje */}
          <div
            className={`relative px-4 py-2 rounded-2xl max-w-full ${
              isUser
                ? "bg-blue-600 text-white rounded-br-sm"
                : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-bl-sm"
            }`}
          >
            {/* Contenido del mensaje */}
            {isThinking ? (
              <div className="flex items-center gap-3">
                <div className="flex space-x-1">
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"></div>
                </div>
                <span className="text-gray-500 text-sm">Pensando...</span>
              </div>
            ) : (
              <div className="whitespace-pre-wrap text-sm leading-relaxed">
                {message.content}
              </div>
            )}

            {/* Imágenes */}
            {!!message.images?.length && (
              <div className="mt-3 grid grid-cols-2 gap-2">
                {message.images.map((src, index) => (
                  <div key={index} className="relative">
                    <img
                      src={src}
                      alt={`Imagen ${index + 1}`}
                      className="rounded-lg object-cover aspect-video w-full hover:scale-105 transition-transform cursor-pointer"
                      onClick={() => window.open(src, "_blank")}
                    />
                  </div>
                ))}
              </div>
            )}

            {/* Videos */}
            {!!message.videos?.length && (
              <div className="mt-3 space-y-2">
                {message.videos.map((src, index) => (
                  <div key={index} className="relative">
                    <video
                      src={src}
                      controls
                      className="w-full rounded-lg max-w-xs"
                      preload="metadata"
                    />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Avatar del usuario (solo cuando es usuario) */}
          {isUser && (
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
          )}
        </div>

        {/* Botones de acción para mensajes del asistente */}
        {!isUser && !isThinking && (
          <div className="flex items-center gap-1 ml-11 opacity-70">
            <button
              onClick={() => navigator.clipboard.writeText(message.content)}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
              title="Copiar"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                />
              </svg>
            </button>
            <button
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
              title="Me gusta"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"
                />
              </svg>
            </button>
            <button
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
              title="No me gusta"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018c.163 0 .326.02.485.06L17 4m-7 10v2a2 2 0 002 2h.095c.5 0 .905-.405.905-.905 0-.714.211-1.412.608-2.006L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5"
                />
              </svg>
            </button>
            <button
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
              title="Regenerar"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
