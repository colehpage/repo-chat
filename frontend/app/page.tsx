import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";

export default function Home() {
  return (
    <main
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        width: "100vw",
        padding: "1rem",
        backgroundColor: "var(--c-black)",
      }}
    >
      <Header />
      <ChatSection />
    </main>
  );
}
