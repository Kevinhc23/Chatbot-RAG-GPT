"use client";
import { useChat } from "@/lib/useChat";
import { ChatMessageBubble } from "@/components/ChatMessageBubble";
import { useEffect, useRef, useState } from "react";
import { Sparkles } from "lucide-react";

export default function ChatPage() {
  const { messages, sendMessage, isLoading } = useChat();
  const [input, setInput] = useState("");
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    await sendMessage(input.trim());
    setInput("");
  };

  return (
    <div className="flex flex-col h-screen">
      <header className="border-b p-4 flex items-center gap-2 bg-white dark:bg-neutral-900">
        <Sparkles className="w-5 h-5 text-blue-600" />
        <h1 className="font-semibold text-lg">Asistente AI</h1>
      </header>

      <main
        ref={listRef}
        className="flex-1 overflow-y-auto p-4 bg-neutral-50 dark:bg-neutral-900"
      >
        {messages.map((m) => (
          <ChatMessageBubble key={m.id} message={m} />
        ))}
      </main>

      <form
        onSubmit={handleSubmit}
        className="p-4 border-t bg-white dark:bg-neutral-800"
      >
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu mensaje..."
            disabled={isLoading}
            className="flex-1 rounded-xl border p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-neutral-700 dark:border-neutral-600 dark:text-white disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="rounded-xl bg-blue-600 text-white px-4 py-2 disabled:opacity-50 flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                Enviando...
              </>
            ) : (
              "Enviar"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
