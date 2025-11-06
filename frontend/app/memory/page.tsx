"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ChatContainer } from "@/components/chat/chat-container";
import { ChatInput } from "@/components/chat/chat-input";
import {
  Message,
  streamMemoryChat,
  getChats,
  createChat,
  deleteChat,
  getChatMessages,
  ChatSession,
} from "@/lib/api";
import { useAuth } from "@/lib/use-auth";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Brain, Plus, Trash2, LogOut, MessageSquare } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

export default function MemoryChatPage() {
  const router = useRouter();
  const { session, isLoading: authLoading, logout } = useAuth();
  const [chats, setChats] = useState<ChatSession[]>([]);
  const [selectedChatId, setSelectedChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [temperature, setTemperature] = useState(0.7);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !session) {
      router.push("/login");
    }
  }, [session, authLoading, router]);

  useEffect(() => {
    if (session) {
      loadChats();
    }
  }, [session]);

  useEffect(() => {
    if (selectedChatId && session) {
      loadMessages(selectedChatId);
    }
  }, [selectedChatId, session]);

  const loadChats = async () => {
    if (!session) return;
    try {
      const data = await getChats(session.session_id);
      setChats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load chats");
    }
  };

  const loadMessages = async (chatId: string) => {
    if (!session) return;
    try {
      const data = await getChatMessages(session.session_id, chatId);
      setMessages(
        data.map((m) => ({ role: m.role as "user" | "assistant", content: m.content }))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load messages");
    }
  };

  const handleCreateChat = async () => {
    if (!session) return;
    try {
      const newChat = await createChat(session.session_id);
      setChats([newChat, ...chats]);
      setSelectedChatId(newChat.id);
      setMessages([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create chat");
    }
  };

  const handleDeleteChat = async (chatId: string) => {
    if (!session) return;
    try {
      await deleteChat(session.session_id, chatId);
      setChats(chats.filter((c) => c.id !== chatId));
      if (selectedChatId === chatId) {
        setSelectedChatId(null);
        setMessages([]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete chat");
    }
  };

  const handleSend = async (message: string) => {
    if (!session || !selectedChatId) return;
    setError(null);
    const userMessage: Message = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setStreamingContent("");

    try {
      let fullResponse = "";

      for await (const chunk of streamMemoryChat(
        session.session_id,
        selectedChatId,
        message,
        temperature
      )) {
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

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  if (authLoading || !session) {
    return null;
  }

  return (
    <div className="container py-6 max-w-7xl">
      <div className="flex gap-6 h-[calc(100vh-8rem)]">
        <Card className="w-80 flex flex-col shadow-sm">
          <CardHeader className="border-b space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-base">{session.username}</CardTitle>
                <CardDescription className="text-xs">Logged in</CardDescription>
              </div>
              <Button variant="ghost" size="icon" onClick={handleLogout}>
                <LogOut className="w-4 h-4" />
              </Button>
            </div>
            <Button onClick={handleCreateChat} className="w-full" size="sm">
              <Plus className="w-4 h-4 mr-2" />
              New Chat
            </Button>
          </CardHeader>

          <ScrollArea className="flex-1 p-4">
            <div className="space-y-2">
              {chats.length === 0 && (
                <p className="text-sm text-muted-foreground text-center py-8">
                  No chats yet. Create one to start!
                </p>
              )}
              {chats.map((chat) => (
                <div
                  key={chat.id}
                  className={`flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-colors ${
                    selectedChatId === chat.id
                      ? "bg-primary/10 border border-primary/20"
                      : "hover:bg-muted"
                  }`}
                  onClick={() => setSelectedChatId(chat.id)}
                >
                  <MessageSquare className="w-4 h-4 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">
                      Chat {chat.id.slice(0, 8)}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(chat.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 flex-shrink-0"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteChat(chat.id);
                    }}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </div>
          </ScrollArea>
        </Card>

        <Card className="flex-1 flex flex-col shadow-sm">
          <CardHeader className="border-b py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Brain className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-lg font-semibold">Memory Chat</CardTitle>
              </div>
              <Badge variant="secondary" className="text-xs">Memory</Badge>
            </div>
          </CardHeader>

          <div className="flex-1 flex flex-col min-h-0">
            {!selectedChatId ? (
              <div className="flex-1 flex items-center justify-center text-muted-foreground">
                <p>Select or create a chat to start messaging</p>
              </div>
            ) : (
              <>
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
                  placeholder="Continue your conversation..."
                />
              </>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
