import type { Metadata } from "next";
import "./css/styles.css";

export const metadata: Metadata = {
  title: "Repo Chatbot",
  description: "Talk to your repo!",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
