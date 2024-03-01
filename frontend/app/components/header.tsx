export default function Header() {
  return (
    <div
      style={{
        display: "flex",
        width: "100%",
        height: "auto",
        gap: "1rem",
        maxWidth: "1200px",
        marginBottom: "1rem",
        userSelect: "none",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "flex-start",
          fontWeight: "bold",
          color: "var(--c-white)",
          width: "100%",
          gap: ".5rem",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "flex-start",
            alignItems: "center",
            gap: "1rem",
          }}
        >
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
                  fillRule="evenodd"
                  fill="currentColor"
                  d="M12 21a1.75 1.75 0 110-3.5 1.75 1.75 0 010 3.5zm-3.25-1.75a3.25 3.25 0 106.5 0 3.25 3.25 0 00-6.5 0zm-3-12.75a1.75 1.75 0 110-3.5 1.75 1.75 0 010 3.5zM2.5 4.75a3.25 3.25 0 106.5 0 3.25 3.25 0 00-6.5 0zM18.25 6.5a1.75 1.75 0 110-3.5 1.75 1.75 0 010 3.5zM15 4.75a3.25 3.25 0 106.5 0 3.25 3.25 0 00-6.5 0z"
                ></path>
                <path
                  fillRule="evenodd"
                  fill="currentColor"
                  d="M6.5 7.75v1A2.25 2.25 0 008.75 11h6.5a2.25 2.25 0 002.25-2.25v-1H19v1a3.75 3.75 0 01-3.75 3.75h-6.5A3.75 3.75 0 015 8.75v-1h1.5z"
                ></path>
                <path
                  fillRule="evenodd"
                  fill="currentColor"
                  d="M11.25 16.25v-5h1.5v5h-1.5z"
                ></path>
              </g>
            </svg>
          </div>
          <h3>Repo Chatbot</h3>
        </div>
        <p
          style={{
            fontSize: "1rem",
            lineHeight: "1.2rem",
            fontWeight: "normal",
          }}
        >
          Talk to your Repo!
        </p>
      </div>
    </div>
  );
}
