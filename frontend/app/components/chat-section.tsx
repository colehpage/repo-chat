"use client";

import { MODEL } from "@/constants";
import { useChat } from "ai/react";
import { ChatInput, ChatMessages } from "./ui/chat";

export default function ChatSection() {
  const {
    messages,
    input,
    isLoading,
    handleSubmit,
    handleInputChange,
    reload,
    stop,
  } = useChat({ api: process.env.NEXT_PUBLIC_CHAT_API });

  console.log(isLoading, messages);

  return (
    <div
      style={{
        display: "flex",
        gap: "1rem",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "auto",
        width: "100%",
        maxWidth: "1200px",
      }}
    >
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
        reload={reload}
        stop={stop}
      />
      <ChatInput
        input={input}
        handleSubmit={handleSubmit}
        handleInputChange={handleInputChange}
        isLoading={isLoading}
        multiModal={MODEL === "gpt-3.5-turbo"}
      />
    </div>
  );
}
