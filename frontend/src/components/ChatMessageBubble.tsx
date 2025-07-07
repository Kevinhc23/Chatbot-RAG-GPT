"use client";
import { FC } from "react";
import { ChatMessage } from "@/app/types";

export const ChatMessageBubble: FC<{ message: ChatMessage }> = ({
  message,
}) => {
  const isUser = message.role === "user";
  const isThinking = message.content === "Pensando...";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-neutral-100 dark:bg-neutral-800"
        } rounded-2xl p-3 shadow max-w-[80%] whitespace-pre-wrap`}
      >
        {isThinking ? (
          <div className="flex items-center gap-2">
            <div className="animate-pulse flex space-x-1">
              <div className="h-2 w-2 bg-neutral-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="h-2 w-2 bg-neutral-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="h-2 w-2 bg-neutral-400 rounded-full animate-bounce"></div>
            </div>
            <span className="text-neutral-500 text-sm">Pensando...</span>
          </div>
        ) : (
          message.content
        )}
        {!!message.images?.length && (
          <div className="grid grid-cols-2 gap-2 mt-2">
            {message.images.map((src) => (
              <img
                key={src}
                src={src}
                alt="assistant-provided"
                className="rounded-lg object-cover aspect-video"
              />
            ))}
          </div>
        )}
        {!!message.videos?.length && (
          <div className="flex flex-col gap-2 mt-2">
            {message.videos.map((src) => (
              <video
                key={src}
                src={src}
                controls
                className="w-full rounded-lg"
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
