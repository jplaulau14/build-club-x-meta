"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ChatContainer } from "@/components/chat/chat-container";
import { ChatInput } from "@/components/chat/chat-input";
import { Message, sendMessage } from "@/lib/api";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { MessageSquare } from "lucide-react";

export default function SimpleChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [temperature, setTemperature] = useState(0.7);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async (message: string) => {
    setError(null);
    const userMessage: Message = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(message, temperature);
      const assistantMessage: Message = {
        role: "assistant",
        content: response.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
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
                <MessageSquare className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-lg font-semibold">Simple Chat</CardTitle>
              </div>
              <Badge variant="secondary" className="text-xs">Non-Streaming</Badge>
            </div>
          </CardHeader>

          <div className="flex-1 flex flex-col min-h-0">
            <ChatContainer
              messages={messages}
              isLoading={isLoading}
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
              placeholder="Type your message and press Enter..."
            />
          </div>
        </Card>
      </div>
    </div>
  );
}
