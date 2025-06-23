import React, { useEffect, useRef } from "react";
import "./ChatThread.css";

const ChatThread = ({ messages, currentUser }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatTime = (timestamp) => {
    if (!timestamp) return "";
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getSenderName = (message) => {
    // If the message has a sender_name, use it
    if (message.sender_name) {
      return message.sender_id === currentUser ? "You" : message.sender_name;
    }
    // If it's the current user, show "You"
    if (message.sender_id === currentUser) {
      return "You";
    }
    // Otherwise show "Other User" or a default
    return "Other User";
  };

  return (
    <div className="chat-thread">
      {messages.length === 0 ? (
        <div className="no-messages">No messages yet. Start the conversation!</div>
      ) : (
        messages.map((msg, idx) => (
          <div
            key={msg.id || idx}
            className={`chat-message ${msg.sender_id === currentUser ? "me" : "them"}`}
          >
            <div className="chat-bubble">
              <span className="chat-content">{msg.content}</span>
            </div>
            <div className="chat-meta">
              <span className="chat-sender">{getSenderName(msg)}</span>
              <span className="chat-time">{formatTime(msg.timestamp)}</span>
            </div>
          </div>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatThread;
