import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare, Zap, Users, Brain, Sparkles, Github } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
      <div className="w-full max-w-5xl px-6 space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-semibold tracking-tight">
            Llama 3.2 Chat Demo
          </h1>
          <p className="text-base text-muted-foreground">
            Explore different chat patterns with Llama 3.2
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <MessageSquare className="w-4 h-4 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Simple Chat</CardTitle>
              </div>
              <CardDescription className="text-xs">
                Request-response pattern
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/simple">
                <Button className="w-full" size="sm">Open</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <Zap className="w-4 h-4 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Streaming Chat</CardTitle>
              </div>
              <CardDescription className="text-xs">
                Real-time streaming with SSE
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/streaming">
                <Button className="w-full" size="sm">Open</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <Users className="w-4 h-4 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Persona Chat</CardTitle>
              </div>
              <CardDescription className="text-xs">
                AI personalities with custom prompts
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/persona">
                <Button className="w-full" size="sm">Open</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <Brain className="w-4 h-4 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Memory Chat</CardTitle>
              </div>
              <CardDescription className="text-xs">
                Sessions with conversation history
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/memory">
                <Button className="w-full" size="sm">Open</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <Sparkles className="w-4 h-4 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Structured Outputs</CardTitle>
              </div>
              <CardDescription className="text-xs">
                Extract structured data from text
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/extraction">
                <Button className="w-full" size="sm">Open</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="shadow-sm hover:shadow-md transition-shadow border-primary/20">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <Github className="w-4 h-4 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Tool Calling</CardTitle>
              </div>
              <CardDescription className="text-xs">
                GitHub agent with multi-tool calling
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/github">
                <Button className="w-full" size="sm" variant="default">Open</Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-muted/30 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-base">API Endpoints</CardTitle>
          </CardHeader>
          <CardContent className="text-xs">
            <ul className="space-y-1.5 text-muted-foreground">
              <li>
                <code className="bg-muted px-1.5 py-0.5 rounded">POST /api/chat</code> - Simple request/response
              </li>
              <li>
                <code className="bg-muted px-1.5 py-0.5 rounded">POST /api/chat/stream</code> - Streaming with SSE
              </li>
              <li>
                <code className="bg-muted px-1.5 py-0.5 rounded">POST /api/chat/persona</code> - Custom system prompts
              </li>
              <li>
                <code className="bg-muted px-1.5 py-0.5 rounded">POST /api/chat/memory</code> - With conversation history
              </li>
              <li>
                <code className="bg-muted px-1.5 py-0.5 rounded">POST /api/chat/extract</code> - Structured data extraction
              </li>
              <li>
                <code className="bg-muted px-1.5 py-0.5 rounded">POST /api/github/chat</code> - GitHub agent with tool calling
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
