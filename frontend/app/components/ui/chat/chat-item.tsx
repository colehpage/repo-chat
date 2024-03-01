"use client";

import { marked } from "marked";
import ChatAvatar from "./chat-avatar";
import { Message } from "./chat-messages";

interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer = ({ content }: MarkdownRendererProps) => {
  const parsedContent = marked.parse(content);

  return <div dangerouslySetInnerHTML={{ __html: parsedContent }}></div>;
};

export default function ChatItem(message: Message) {
  return (
    <div
      style={{
        display: "flex",
        gap: "1rem",
        alignItems: "center",
        justifyContent: "flex-start",
        width: "100%",
        padding: ".5rem",
        fontSize: "1rem",
        lineHeight: "1.2rem",
      }}
    >
      <div
        style={{
          height: "100%",
          display: "flex",
          justifyContent: "flex-start",
          marginBottom: "auto",
        }}
      >
        <ChatAvatar {...message} />
      </div>
      <p
        style={{
          overflowWrap: "break-word",
          wordWrap: "break-word",
          wordBreak: "break-word",
          fontWeight: message.role === "assistant" ? "normal" : "bold",
          color:
            message.role === "assistant"
              ? "var(--c-neon-orange)"
              : "var(--c-white)",
        }}
      >
        <MarkdownRenderer content={message.content} />
      </p>
    </div>
  );
}
