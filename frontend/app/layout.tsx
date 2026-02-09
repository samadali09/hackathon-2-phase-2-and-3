import type { Metadata } from "next";
import { Inter } from "next/font/google"; // Changed from Geist
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans", // Changed variable name
});

export const metadata: Metadata = {
  title: "Todo App - Manage Your Tasks",
  description: "A modern task management application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning><body className={`font-sans ${inter.variable} bg-dark-background text-dark-text antialiased`}>{children}</body></html>
  );
}
