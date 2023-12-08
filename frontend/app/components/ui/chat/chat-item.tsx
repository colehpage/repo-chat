"use client";

import ChatAvatar from "./chat-avatar";
import { Message } from "./chat-messages";

export default function ChatItem(message: Message) {
  console.log(message);
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
              ? "var(--c-fuchsia)"
              : "var(--c-white)",
        }}
      >
        {message.content}
      </p>
    </div>
  );
}
