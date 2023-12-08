"use client";

export interface ChatInputProps {
  /** The current value of the input */
  input?: string;
  /** An input/textarea-ready onChange handler to control the value of the input */
  handleInputChange?: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>
  ) => void;
  /** Form submission handler to automatically reset input and append a user message  */
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
  multiModal?: boolean;
}

export default function ChatInput(props: ChatInputProps) {
  const { handleSubmit, handleInputChange } = props;
  return (
    <>
      <form
        onSubmit={props.handleSubmit}
        style={{
          position: "relative",
          padding: ".5rem 1rem",
          display: "flex",
          gap: "1rem",
          justifyContent: "space-between",
          alignItems: "center",
          overflowY: "visible",
          width: "100%",
          backgroundColor: "rgba(0,0,0,0.2)",
          borderRadius: ".5rem",
          border: "1px solid var(--c-grey)",
          transition: ".15s",
        }}
      >
        <input
          style={{
            position: "relative",
            flex: 1,
            overflowX: "auto",
            overflowY: "scroll",
            color: "var(--c-white)",
            background: "transparent",
            fontSize: "1rem",
            boxSizing: "border-box",
            resize: "none",
            border: "none",
            outline: "none",
          }}
          autoComplete="off"
          id="query-input"
          value={props.input}
          name="message"
          autoFocus
          placeholder="Ask something!"
          onChange={handleInputChange}
        ></input>
        <button
          disabled={props.isLoading}
          type="submit"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "2rem",
            width: "2rem",
            flexShrink: 0,
            userSelect: "none",
            borderRadius: "25%",
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            border: "1px solid var(--c-grey)",
            color: "var(--c-white)",
            transition: ".15s",
          }}
        >
          <svg
            viewBox="0 0 24 24"
            width="20"
            height="20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g>
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                width={24}
                height={24}
                d="M9.39862 4.32752C9.69152 4.03463 10.1664 4.03463 10.4593 4.32752L16.8232 10.6915C17.5067 11.3749 17.5067 12.4829 16.8232 13.1664L10.4593 19.5303C10.1664 19.8232 9.69152 19.8232 9.39863 19.5303C9.10573 19.2374 9.10573 18.7625 9.39863 18.4697L15.7626 12.1057C15.8602 12.0081 15.8602 11.8498 15.7626 11.7521L9.39863 5.38818C9.10573 5.09529 9.10573 4.62041 9.39862 4.32752Z"
                fill="var(--c-white)"
              ></path>
            </g>
          </svg>
        </button>
      </form>
    </>
  );
}
