"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ChatContainer } from "@/components/chat/chat-container";
import { ChatInput } from "@/components/chat/chat-input";
import { Message, streamMessage } from "@/lib/api";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Zap } from "lucide-react";

export default function StreamingChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [temperature, setTemperature] = useState(0.7);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async (message: string) => {
    setError(null);
    const userMessage: Message = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setStreamingContent("");

    try {
      let fullResponse = "";

      for await (const chunk of streamMessage(message, temperature)) {
        fullResponse += chunk;
        setStreamingContent(fullResponse);
      }

      const assistantMessage: Message = {
        role: "assistant",
        content: fullResponse,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setStreamingContent("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container py-6">
      <div className="flex flex-col h-[calc(100vh-8rem)] max-w-3xl mx-auto">
        <Card className="flex flex-col flex-1 shadow-sm">
          <CardHeader className="border-b py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Zap className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-lg font-semibold">Streaming Chat</CardTitle>
              </div>
              <Badge variant="secondary" className="text-xs">Streaming</Badge>
            </div>
          </CardHeader>

          <div className="flex-1 flex flex-col min-h-0">
            <ChatContainer
              messages={messages}
              isLoading={isLoading && !streamingContent}
              streamingContent={streamingContent}
            />

            <div className="p-4 border-t bg-muted/30">
              <div className="flex items-center gap-4 mb-3">
                <span className="text-sm font-medium min-w-24">
                  Temperature: {temperature.toFixed(1)}
                </span>
                <Slider
                  value={[temperature]}
                  onValueChange={([value]) => setTemperature(value)}
                  min={0}
                  max={2}
                  step={0.1}
                  className="flex-1"
                  disabled={isLoading}
                />
              </div>
              {error && (
                <div className="text-sm text-destructive mb-2">
                  Error: {error}
                </div>
              )}
            </div>

            <ChatInput
              onSend={handleSend}
              disabled={isLoading}
              placeholder="Type your message and watch it stream in real-time..."
            />
          </div>
        </Card>
      </div>
    </div>
  );
}
