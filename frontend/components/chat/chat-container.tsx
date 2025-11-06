import { useEffect, useRef } from "react";
import { ChatMessage } from "./chat-message";
import { Message } from "@/lib/api";
import { Loader2 } from "lucide-react";

interface ChatContainerProps {
  messages: Message[];
  isLoading?: boolean;
  streamingContent?: string;
}

export function ChatContainer({
  messages,
  isLoading = false,
  streamingContent = "",
}: ChatContainerProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, streamingContent]);

  return (
    <div className="flex-1 overflow-y-auto p-4" ref={scrollRef}>
      {messages.length === 0 && !isLoading && (
        <div className="flex items-center justify-center h-full text-muted-foreground">
          <p>Start a conversation by typing a message below</p>
        </div>
      )}

      {messages.map((msg, idx) => (
        <ChatMessage key={idx} role={msg.role} content={msg.content} />
      ))}

      {streamingContent && (
        <ChatMessage role="assistant" content={streamingContent} />
      )}

      {isLoading && !streamingContent && (
        <div className="flex gap-3 mb-4">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
            <Loader2 className="w-5 h-5 text-primary animate-spin" />
          </div>
          <div className="bg-muted rounded-lg px-4 py-2.5">
            <p className="text-sm text-muted-foreground">Thinking...</p>
          </div>
        </div>
      )}
    </div>
  );
}
