import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { MessageSquare } from "lucide-react";
import { NavLink } from "@/components/nav-link";

const inter = Inter({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Llama Chat Demo",
  description: "Demo application for Llama 3.2 chat endpoints",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>
        <div className="min-h-screen flex flex-col">
          <header className="border-b bg-background">
            <div className="container flex items-center gap-8 h-16 px-8">
              <Link href="/" className="flex items-center gap-2.5 font-semibold">
                <MessageSquare className="w-5 h-5" />
                <span>Llama Chat Demo</span>
              </Link>
              <nav className="flex gap-6">
                <NavLink href="/simple">Simple Chat</NavLink>
                <NavLink href="/streaming">Streaming Chat</NavLink>
                <NavLink href="/persona">Persona Chat</NavLink>
                <NavLink href="/memory">Memory Chat</NavLink>
              </nav>
            </div>
          </header>
          <main className="flex-1">{children}</main>
        </div>
      </body>
    </html>
  );
}
