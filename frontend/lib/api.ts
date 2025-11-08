const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  message: string;
  temperature?: number;
}

export interface PersonaRequest extends ChatRequest {
  persona_name?: string;
  custom_system_prompt?: string;
}

export interface ChatResponse {
  response: string;
  model: string;
}

export interface PersonaResponse extends ChatResponse {
  persona_used: string;
}

export async function sendMessage(message: string, temperature: number = 0.7): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, temperature }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function* streamMessage(
  message: string,
  temperature: number = 0.7
): AsyncGenerator<string, void, unknown> {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, temperature }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error("No response body");
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6));
          if (data.content) {
            yield data.content;
          }
          if (data.error) {
            throw new Error(data.error);
          }
        } catch (e) {
          if (e instanceof Error && e.message.includes("error")) {
            throw e;
          }
        }
      }
    }
  }
}

export async function* streamPersonaMessage(
  message: string,
  personaName?: string,
  customPrompt?: string,
  temperature: number = 0.7
): AsyncGenerator<{ type: "metadata" | "content"; data: string | { persona: string } }, void, unknown> {
  const body: PersonaRequest = {
    message,
    temperature,
    ...(personaName && { persona_name: personaName }),
    ...(customPrompt && { custom_system_prompt: customPrompt }),
  };

  const response = await fetch(`${API_BASE_URL}/chat/persona`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error("No response body");
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6));
          if (data.persona) {
            yield { type: "metadata", data };
          }
          if (data.content) {
            yield { type: "content", data: data.content };
          }
          if (data.error) {
            throw new Error(data.error);
          }
        } catch (e) {
          if (e instanceof Error && e.message.includes("error")) {
            throw e;
          }
        }
      }
    }
  }
}

export interface Persona {
  name: string;
  description: string;
}

export async function getPersonas(): Promise<Record<string, string>> {
  const response = await fetch(`${API_BASE_URL}/personas`);

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  session_id: string;
  user_id: number;
  username: string;
}

export interface ChatSession {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface MessageHistory {
  role: string;
  content: string;
  created_at: string;
}

export async function register(username: string, password: string): Promise<{ user_id: number; username: string }> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Registration failed");
  }

  return response.json();
}

export async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
}

export async function getChats(sessionId: string): Promise<ChatSession[]> {
  const response = await fetch(`${API_BASE_URL}/chats`, {
    headers: { Authorization: `Bearer ${sessionId}` },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function createChat(sessionId: string): Promise<ChatSession> {
  const response = await fetch(`${API_BASE_URL}/chats`, {
    method: "POST",
    headers: { Authorization: `Bearer ${sessionId}` },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function deleteChat(sessionId: string, chatId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/chats/${chatId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${sessionId}` },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }
}

export async function getChatMessages(sessionId: string, chatId: string): Promise<MessageHistory[]> {
  const response = await fetch(`${API_BASE_URL}/chats/${chatId}/messages`, {
    headers: { Authorization: `Bearer ${sessionId}` },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function* streamMemoryChat(
  sessionId: string,
  chatId: string,
  message: string,
  temperature: number = 0.7
): AsyncGenerator<string, void, unknown> {
  const response = await fetch(`${API_BASE_URL}/chat/memory`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${sessionId}`,
      "X-Chat-Id": chatId,
    },
    body: JSON.stringify({ message, temperature }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error("No response body");
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6));
          if (data.content) {
            yield data.content;
          }
          if (data.error) {
            throw new Error(data.error);
          }
        } catch (e) {
          if (e instanceof Error && e.message.includes("error")) {
            throw e;
          }
        }
      }
    }
  }
}

export interface ExtractionSchema {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: string;
  system_prompt: string;
  example_text: string;
}

export interface ExtractionRequest {
  text: string;
  schema_name: string;
}

export interface ExtractionResponse {
  data: Record<string, unknown>;
  schema_used: string;
}

export async function getExtractionSchemas(): Promise<ExtractionSchema[]> {
  const response = await fetch(`${API_BASE_URL}/extraction/schemas`);

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  const result = await response.json();
  return result.schemas;
}

export async function extractData(
  text: string,
  schemaName: string
): Promise<ExtractionResponse> {
  const response = await fetch(`${API_BASE_URL}/chat/extract`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, schema_name: schemaName }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Extraction failed");
  }

  return response.json();
}

export interface GitHubChatRequest {
  message: string;
  github_token?: string;
}

export interface GitHubStreamEvent {
  type: "text" | "annotation" | "done" | "error";
  content?: string;
  annotation_type?: "tool_call" | "tool_result";
  tool?: string;
  args?: Record<string, unknown>;
  result_preview?: string;
  result?: unknown;
  timestamp?: string;
  tools_used?: string[];
  message?: string;
}

export async function* streamGitHubMessage(
  message: string,
  temperature: number = 0.7
): AsyncGenerator<GitHubStreamEvent, void, unknown> {
  const body: ChatRequest = {
    message,
    temperature,
  };

  const response = await fetch(`${API_BASE_URL}/github/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error("No response body");
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6));

          if (data.type === "annotation") {
            // Tool call or tool result annotation
            yield {
              type: "annotation",
              annotation_type: data.annotation_type,
              tool: data.tool,
              args: data.args,
              result_preview: data.result_preview,
              result: data.result,
              timestamp: data.timestamp,
            };
          } else if (data.type === "text" && data.content) {
            yield {
              type: "text",
              content: data.content,
            };
          } else if (data.type === "done") {
            yield {
              type: "done",
              tools_used: data.tools_used || [],
            };
          } else if (data.type === "error") {
            yield {
              type: "error",
              message: data.message,
            };
            throw new Error(data.message);
          }
          // Legacy support for old format
          else if (data.content) {
            yield {
              type: "text",
              content: data.content,
            };
          } else if (data.done) {
            yield {
              type: "done",
            };
          } else if (data.error) {
            yield {
              type: "error",
              message: data.error,
            };
            throw new Error(data.error);
          }
        } catch (e) {
          if (e instanceof Error && e.message.includes("error")) {
            throw e;
          }
        }
      }
    }
  }
}
