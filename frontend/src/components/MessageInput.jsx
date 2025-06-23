import React, { useState } from "react";
import "./MessageInput.css";

const MessageInput = ({ onSend, disabled }) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="message-input"
        placeholder="Type a message..."
        value={input}
        onChange={e => setInput(e.target.value)}
        disabled={disabled}
        autoComplete="off"
      />
      <button
        type="submit"
        className="send-btn"
        disabled={disabled || !input.trim()}
        aria-label="Send"
      >
        <span role="img" aria-label="send">➤</span>
      </button>
    </form>
  );
};

export default MessageInput;
