
import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import "./suppress-overlays";

export const metadata: Metadata = {
  title: "The Factory | C-Suite Dashboard",
  description: "AI Agent Orchestration Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
