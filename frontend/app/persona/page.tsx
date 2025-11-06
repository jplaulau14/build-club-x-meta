"use client";

import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ChatContainer } from "@/components/chat/chat-container";
import { ChatInput } from "@/components/chat/chat-input";
import { Message, streamPersonaMessage, getPersonas } from "@/lib/api";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Users } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";

export default function PersonaChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [temperature, setTemperature] = useState(0.7);
  const [selectedPersona, setSelectedPersona] = useState<string>("");
  const [personas, setPersonas] = useState<Record<string, string>>({});
  const [currentPersonaName, setCurrentPersonaName] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPersonas().then((data) => {
      setPersonas(data);
      if (Object.keys(data).length > 0) {
        setSelectedPersona(Object.keys(data)[0]);
      }
    });
  }, []);

  const handleSend = async (message: string) => {
    setError(null);
    const userMessage: Message = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setStreamingContent("");

    try {
      let fullResponse = "";
      let metadataReceived = false;

      for await (const chunk of streamPersonaMessage(
        message,
        selectedPersona,
        undefined,
        temperature
      )) {
        if (chunk.type === "metadata") {
          if (typeof chunk.data === "object" && "persona" in chunk.data) {
            setCurrentPersonaName(chunk.data.persona);
            metadataReceived = true;
          }
        } else if (chunk.type === "content") {
          if (typeof chunk.data === "string") {
            fullResponse += chunk.data;
            setStreamingContent(fullResponse);
          }
        }
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

  const personaName = currentPersonaName || "Select a persona";
  const personaKey = selectedPersona || "default";

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] p-6">
      <div className="w-full max-w-3xl h-[600px] flex flex-col">
        <Card className="flex flex-col h-full shadow-sm">
          <CardHeader className="border-b py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Users className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-lg font-semibold">Persona Chat</CardTitle>
              </div>
              <Badge variant="secondary" className="text-xs">{personaName}</Badge>
            </div>
          </CardHeader>

          <div className="flex-1 flex flex-col min-h-0">
            <ChatContainer
              messages={messages}
              isLoading={isLoading && !streamingContent}
              streamingContent={streamingContent}
            />

            <div className="p-4 border-t bg-muted/30 space-y-4">
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium min-w-24">Persona:</span>
                <Select
                  value={selectedPersona}
                  onValueChange={setSelectedPersona}
                  disabled={isLoading}
                >
                  <SelectTrigger className="flex-1">
                    <SelectValue placeholder="Select a persona" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(personas).map(([key, description]) => (
                      <SelectItem key={key} value={key}>
                        <div className="flex flex-col items-start">
                          <span className="font-medium capitalize">
                            {key.replace("_", " ")}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {description}
                          </span>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Separator />

              <div className="flex items-center gap-4">
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
                <div className="text-sm text-destructive">Error: {error}</div>
              )}
            </div>

            <ChatInput
              onSend={handleSend}
              disabled={isLoading}
              placeholder="Chat with your selected persona..."
            />
          </div>
        </Card>
      </div>
    </div>
  );
}
