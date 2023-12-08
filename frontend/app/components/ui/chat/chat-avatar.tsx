"use client";

import Image from "next/image";
import { Message } from "./chat-messages";

export default function ChatAvatar(message: Message) {
  if (message.role === "user") {
    return (
      <div
        style={{
          display: "flex",
          height: "2rem",
          width: "2rem",
          flexShrink: 0,
          userSelect: "none",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: "25%",
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          border: "1px solid var(--c-grey)",
          color: "var(--c-white)",
        }}
      >
        <svg
          viewBox="0 0 24 24"
          width="20"
          height="20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g id="SVGRepo_iconCarrier">
            <path
              d="M10 13C9.44772 13 9 13.4477 9 14C9 14.5523 9.44772 15 10 15H14C14.5523 15 15 14.5523 15 14C15 13.4477 14.5523 13 14 13H10Z"
              fill="currentColor"
            ></path>{" "}
            <path
              d="M17 14C17 13.4477 17.4477 13 18 13C18.5523 13 19 13.4477 19 14C19 14.5523 18.5523 15 18 15C17.4477 15 17 14.5523 17 14Z"
              fill="currentColor"
            ></path>{" "}
            <path
              d="M6 13C5.44772 13 5 13.4477 5 14C5 14.5523 5.44772 15 6 15C6.55229 15 7 14.5523 7 14C7 13.4477 6.55229 13 6 13Z"
              fill="currentColor"
            ></path>{" "}
            <path
              d="M5 10C5 9.44772 5.44772 9 6 9C6.55229 9 7 9.44772 7 10C7 10.5523 6.55229 11 6 11C5.44772 11 5 10.5523 5 10Z"
              fill="currentColor"
            ></path>{" "}
            <path
              d="M10 9C9.44771 9 9 9.44772 9 10C9 10.5523 9.44771 11 10 11C10.5523 11 11 10.5523 11 10C11 9.44772 10.5523 9 10 9Z"
              fill="currentColor"
            ></path>{" "}
            <path
              d="M13 10C13 9.44772 13.4477 9 14 9C14.5523 9 15 9.44772 15 10C15 10.5523 14.5523 11 14 11C13.4477 11 13 10.5523 13 10Z"
              fill="currentColor"
            ></path>{" "}
            <path
              d="M18 9C17.4477 9 17 9.44772 17 10C17 10.5523 17.4477 11 18 11C18.5523 11 19 10.5523 19 10C19 9.44772 18.5523 9 18 9Z"
              fill="currentColor"
            ></path>
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M20 5C21.6569 5 23 6.34315 23 8V16C23 17.6569 21.6569 19 20 19H4C2.34315 19 1 17.6569 1 16V8C1 6.34315 2.34315 5 4 5H20ZM20 7C20.5523 7 21 7.44772 21 8V16C21 16.5523 20.5523 17 20 17H4C3.44772 17 3 16.5523 3 16V8C3 7.44772 3.44772 7 4 7H20Z"
              fill="currentColor"
            ></path>
          </g>
        </svg>
      </div>
    );
  }

  return (
    <div
      style={{
        display: "flex",
        height: "2rem",
        width: "2rem",
        flexShrink: 0,
        userSelect: "none",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: "25%",
        backgroundColor: "rgba(255, 255, 255, 0.1)",
        border: "1px solid var(--c-grey)",
        color: "var(--c-white)",
      }}
    >
      <svg
        fill="#000000"
        viewBox="0 0 24 24"
        width="20"
        height="20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g>
          <path
            fill-rule="evenodd"
            fill="currentColor"
            d="M12 21a1.75 1.75 0 110-3.5 1.75 1.75 0 010 3.5zm-3.25-1.75a3.25 3.25 0 106.5 0 3.25 3.25 0 00-6.5 0zm-3-12.75a1.75 1.75 0 110-3.5 1.75 1.75 0 010 3.5zM2.5 4.75a3.25 3.25 0 106.5 0 3.25 3.25 0 00-6.5 0zM18.25 6.5a1.75 1.75 0 110-3.5 1.75 1.75 0 010 3.5zM15 4.75a3.25 3.25 0 106.5 0 3.25 3.25 0 00-6.5 0z"
          ></path>
          <path
            fill-rule="evenodd"
            fill="currentColor"
            d="M6.5 7.75v1A2.25 2.25 0 008.75 11h6.5a2.25 2.25 0 002.25-2.25v-1H19v1a3.75 3.75 0 01-3.75 3.75h-6.5A3.75 3.75 0 015 8.75v-1h1.5z"
          ></path>
          <path
            fill-rule="evenodd"
            fill="currentColor"
            d="M11.25 16.25v-5h1.5v5h-1.5z"
          ></path>
        </g>
      </svg>
    </div>
  );
}
