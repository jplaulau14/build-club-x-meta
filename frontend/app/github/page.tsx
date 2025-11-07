"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ChatContainer } from "@/components/chat/chat-container";
import { ChatInput } from "@/components/chat/chat-input";
import { Message, streamGitHubMessage, GitHubStreamEvent } from "@/lib/api";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Github, Wrench, CheckCircle2, Loader2 } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

interface ToolAnnotation {
  id: string;
  tool: string;
  type: "tool_call" | "tool_result";
  args?: Record<string, unknown>;
  result?: unknown;
  result_preview?: string;
  timestamp: number;
  status: "calling" | "completed";
}

export default function GitHubChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [temperature, setTemperature] = useState(0.7);
  const [error, setError] = useState<string | null>(null);

  // Tool call annotations tracking
  const [annotations, setAnnotations] = useState<ToolAnnotation[]>([]);
  const [pendingToolCalls, setPendingToolCalls] = useState<Map<string, ToolAnnotation>>(new Map());

  const handleSend = async (message: string) => {
    setError(null);
    const userMessage: Message = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setStreamingContent("");
    setAnnotations([]);
    setPendingToolCalls(new Map());

    try {
      let fullResponse = "";
      const newAnnotations: ToolAnnotation[] = [];
      const pending = new Map<string, ToolAnnotation>();

      for await (const event of streamGitHubMessage(message, temperature)) {
        // Handle different event types
        if (event.type === "text" && event.content) {
          fullResponse += event.content;
          setStreamingContent(fullResponse);
        }
        else if (event.type === "annotation") {
          if (event.annotation_type === "tool_call") {
            // Tool is being called
            const uniqueId = `${event.tool}-call-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
            const annotation: ToolAnnotation = {
              id: uniqueId,
              tool: event.tool || "unknown",
              type: "tool_call",
              args: event.args,
              timestamp: Date.now(),
              status: "calling"
            };
            newAnnotations.push(annotation);
            pending.set(uniqueId, annotation);
            setAnnotations([...newAnnotations]);
            setPendingToolCalls(new Map(pending));
          }
          else if (event.annotation_type === "tool_result") {
            // Tool returned a result - find the most recent pending call for this tool
            const toolName = event.tool || "unknown";

            // Find the most recent "calling" annotation for this tool
            let pendingIndex = -1;
            for (let i = newAnnotations.length - 1; i >= 0; i--) {
              if (newAnnotations[i].tool === toolName && newAnnotations[i].status === "calling") {
                pendingIndex = i;
                break;
              }
            }

            if (pendingIndex !== -1) {
              // Update the pending call with result
              newAnnotations[pendingIndex] = {
                ...newAnnotations[pendingIndex],
                result: event.result,
                result_preview: event.result_preview,
                status: "completed"
              };

              // Remove from pending map
              pending.delete(newAnnotations[pendingIndex].id);
              setAnnotations([...newAnnotations]);
              setPendingToolCalls(new Map(pending));
            }
          }
        }
        else if (event.type === "done") {
          // Stream completed
          break;
        }
        else if (event.type === "error") {
          throw new Error(event.message || "Unknown error");
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

  // Example queries for each stage
  const exampleQueries = [
    {
      stage: "Stage 1",
      label: "Single Tool",
      queries: [
        "Find popular React repositories",
        "Search for Python machine learning libraries",
        "Find Rust web frameworks"
      ]
    },
    {
      stage: "Stage 2",
      label: "Multiple Tools",
      queries: [
        "Tell me about facebook/react",
        "Find TypeScript frameworks",
        "What is vercel/next.js?"
      ]
    },
    {
      stage: "Stage 3",
      label: "Tool Chaining",
      queries: [
        "Find popular Python web frameworks and show me open issues for the top one",
        "Search for JavaScript testing libraries and tell me about the most popular one",
        "Find Go web frameworks and show issues for the top result"
      ]
    }
  ];

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] p-6">
      <div className="w-full max-w-6xl h-[700px] flex gap-4">
        {/* Main Chat Panel */}
        <Card className="flex flex-col flex-1 shadow-sm">
          <CardHeader className="border-b py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Github className="w-5 h-5 text-muted-foreground" />
                <div>
                  <CardTitle className="text-lg font-semibold">GitHub Agent</CardTitle>
                  <CardDescription className="text-xs mt-1">
                    Tool Calling Demo - Powered by PydanticAI + Llama 3.2
                  </CardDescription>
                </div>
              </div>
              <div className="flex gap-2">
                <Badge variant="secondary" className="text-xs">Tool Calling</Badge>
                <Badge variant="outline" className="text-xs">Ollama</Badge>
              </div>
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
              placeholder="Ask me about GitHub repositories..."
            />
          </div>
        </Card>

        {/* Side Panel: Tool Calls + Examples */}
        <div className="w-80 flex flex-col gap-4">
          {/* Tool Call Annotations */}
          <Card className="flex-1 shadow-sm overflow-hidden flex flex-col">
            <CardHeader className="border-b py-3 flex-shrink-0">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Wrench className="w-4 h-4 text-muted-foreground" />
                  <CardTitle className="text-sm font-semibold">Tool Annotations</CardTitle>
                </div>
                <Badge variant="secondary" className="text-xs">
                  {annotations.length} {annotations.length === 1 ? 'call' : 'calls'}
                </Badge>
              </div>
            </CardHeader>
            <ScrollArea className="flex-1 overflow-y-auto">
              <div className="p-4">
                {annotations.length === 0 ? (
                  <div className="text-sm text-muted-foreground text-center py-8">
                    Tool call annotations will appear here during execution
                  </div>
                ) : (
                  <div className="space-y-3">
                    {annotations.map((annotation) => (
                      <div
                        key={annotation.id}
                        className={`p-3 rounded-lg border ${
                          annotation.status === "calling"
                            ? "bg-blue-50 border-blue-200 dark:bg-blue-950/20 dark:border-blue-800"
                            : "bg-green-50 border-green-200 dark:bg-green-950/20 dark:border-green-800"
                        }`}
                      >
                        <div className="flex items-center gap-2 mb-2">
                          {annotation.status === "calling" ? (
                            <Loader2 className="w-4 h-4 text-blue-600 animate-spin flex-shrink-0" />
                          ) : (
                            <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />
                          )}
                          <span className="text-sm font-mono font-semibold truncate">
                            {annotation.tool}
                          </span>
                          <Badge
                            variant={annotation.status === "calling" ? "default" : "outline"}
                            className="text-xs ml-auto flex-shrink-0"
                          >
                            {annotation.status === "calling" ? "executing" : "completed"}
                          </Badge>
                        </div>

                        {annotation.args && Object.keys(annotation.args).length > 0 && (
                          <div className="mt-2 p-2 bg-background/50 rounded border text-xs overflow-hidden">
                            <div className="font-semibold mb-1 text-muted-foreground">Arguments:</div>
                            <div className="overflow-x-auto max-w-full">
                              <pre className="font-mono text-xs whitespace-pre-wrap break-all">
                                {JSON.stringify(annotation.args, null, 2)}
                              </pre>
                            </div>
                          </div>
                        )}

                        {annotation.result_preview && (
                          <div className="mt-2 p-2 bg-background/50 rounded border text-xs overflow-hidden">
                            <div className="font-semibold mb-1 text-muted-foreground">Result:</div>
                            <div className="overflow-x-auto max-w-full">
                              <div className="font-mono text-xs whitespace-pre-wrap break-all">
                                {annotation.result_preview}
                              </div>
                            </div>
                          </div>
                        )}

                        {annotation.result && typeof annotation.result === 'object' && (
                          <div className="mt-2 p-2 bg-background/50 rounded border text-xs max-h-40 overflow-auto">
                            <div className="font-semibold mb-1 text-muted-foreground">Full Result:</div>
                            <div className="overflow-x-auto max-w-full">
                              <pre className="font-mono text-xs whitespace-pre-wrap break-all">
                                {JSON.stringify(annotation.result, null, 2)}
                              </pre>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </ScrollArea>
          </Card>

          {/* Example Queries */}
          <Card className="shadow-sm">
            <CardHeader className="border-b py-3">
              <CardTitle className="text-sm font-semibold">Example Queries</CardTitle>
            </CardHeader>
            <ScrollArea className="max-h-64">
              <div className="p-4 space-y-4">
                {exampleQueries.map((section, sectionIdx) => (
                  <div key={sectionIdx}>
                    {sectionIdx > 0 && <Separator className="my-3" />}
                    <div className="mb-2">
                      <Badge variant="outline" className="text-xs">
                        {section.stage}
                      </Badge>
                      <span className="text-xs text-muted-foreground ml-2">
                        {section.label}
                      </span>
                    </div>
                    <div className="space-y-2">
                      {section.queries.map((query, queryIdx) => (
                        <button
                          key={queryIdx}
                          onClick={() => !isLoading && handleSend(query)}
                          disabled={isLoading}
                          className="w-full text-left text-xs p-2 rounded border hover:bg-muted/50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {query}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </Card>
        </div>
      </div>
    </div>
  );
}
