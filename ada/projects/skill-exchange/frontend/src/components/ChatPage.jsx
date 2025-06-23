import React, { useState, useEffect } from "react";
import "./ChatPage.css"; // (create this file for styling)
import ChatThread from "./ChatThread";
import MessageInput from "./MessageInput";
import RatingForm from "./RatingForm";
import UserDropdown from "./UserDropdown";
import axios from "axios";
import { API_URL } from "../App";

const ChatPage = ({ match, matches, onSelectConversation, onBack, user, onNavigate, onLogout, onRatingSuccess }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showRating, setShowRating] = useState(false);
  const [showBanner, setShowBanner] = useState(false);

  // Fetch messages when match changes
  useEffect(() => {
    if (match && user) {
      fetchMessages();
    }
  }, [match, user]);

  const getOtherUserAvatar = (conversation) => {
    const avatarUrl = conversation.other_user?.avatar;
    if (!avatarUrl) {
      return 'https://randomuser.me/api/portraits/lego/1.jpg';
    }
    return avatarUrl.startsWith('http') ? avatarUrl : `${API_URL}${avatarUrl}`;
  };

  if (!match) {
    return (
      <div className="no-chat-selected">
        <div className="no-chat-content">
          <h2>No Conversations</h2>
          <p>You don't have any active conversations yet.</p>
          <button 
            className="back-to-matches-btn"
            onClick={onBack}
          >
            Go to Match Suggestions
          </button>
        </div>
      </div>
    );
  }

  const fetchMessages = async () => {
    if (!match || !user) return;
    
    setLoading(true);
    try {
      const chatId = match.chat_id || match.id;
      const response = await axios.get(`${API_URL}/chats/${chatId}/messages`);
      // Handle new API response format: {"messages": [...]}
      const messagesData = response.data.messages || response.data || [];
      setMessages(messagesData);
    } catch (error) {
      console.error("Error fetching messages:", error);
      setMessages([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (messageContent) => {
    if (!match || !user || !messageContent.trim()) return;

    const newMessage = {
      content: messageContent,
      sender_id: user.id || user.user_id,
      chat_id: match.chat_id || match.id,
      sender_name: user.name,
      timestamp: new Date().toISOString()
    };

    try {
      // Optimistically add message to UI
      setMessages(prev => [...prev, newMessage]);
      
      // Send to backend
      const response = await axios.post(`${API_URL}/chats/${match.id}/messages`, newMessage);
      
      // Update with server response (in case of ID assignment, etc.)
      setMessages(prev => prev.map(msg => 
        msg === newMessage ? response.data : msg
      ));
    } catch (error) {
      console.error("Error sending message:", error);
      // Remove the optimistic message on error
      setMessages(prev => prev.filter(msg => msg !== newMessage));
      
      // Show user-friendly error message
      const errorMessage = error.response?.data?.message || "Failed to send message. Please try again.";
      alert(errorMessage);
    }
  };

  const handleRatingSubmit = async ({ rating, feedback }) => {
    if (!match || !user) {
      alert("Cannot submit rating. Missing information.");
      return;
    }

    const ratingData = {
      rater_id: user.id || user.user_id,
      rated_id: match.other_user.id,
      rating: rating,
      comment: feedback,
      chat_id: match.chat_id || match.id
    };

    try {
      await axios.post(`${API_URL}/ratings`, ratingData);
    setShowRating(false);
      alert('Thank you for your feedback!');
      if (onRatingSuccess) {
        onRatingSuccess(match.id);
      }
    } catch (error) {
      console.error("Error submitting rating:", error);
      alert(error.response?.data?.message || "Failed to submit rating. Please try again.");
    }
  };

  // Call this if user closes the modal without rating
  const handleRatingCancel = () => {
    setShowRating(false);
    setShowBanner(true);
  };

  return (
    <div>
      <div className="chat-topbar">
        <span className="chat-app-title">Skill Exchange App</span>
        <UserDropdown user={user} onNavigate={onNavigate} onLogout={onLogout} />
      </div>
      <div className="chat-root">
        <aside className="chat-sidebar">
          <h3>Messages</h3>
          <ul>
            {matches.map(conv => (
              <li
                key={conv.id}
                className={conv.id === match.id ? "active" : ""}
                onClick={() => onSelectConversation(conv)}
              >
                <img 
                  src={getOtherUserAvatar(conv)} 
                  alt={conv.other_user?.name} 
                  className="avatar" 
                />
                <div className="conversation-details">
                  <span>{conv.other_user?.name}</span>
                  {conv.unread_count > 0 && (
                    <span className="unread_count">{conv.unread_count}</span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </aside>
        <section className="chat-main">
          <header className="chat-header">
            <div className="chat-header-left">
              <img 
                src={getOtherUserAvatar(match)} 
                alt={match.other_user?.name} 
                className="avatar" 
              />
              <span className="chat-user">{match.other_user?.name}</span>
            </div>
            <div className="chat-header-right">
              {!match.is_rated_by_current_user && (
                <button
                  className="mark-complete-btn"
                  onClick={() => setShowRating(true)}
                >
                  Mark as Complete
                </button>
              )}
            </div>
          </header>
          <div className="chat-messages">
            {loading ? (
              <div className="loading-messages">Loading messages...</div>
            ) : (
              <ChatThread 
                messages={messages} 
                currentUser={user.id || user.user_id} 
              />
            )}
          </div>
          <MessageInput
            onSend={handleSendMessage}
            disabled={loading}
          />
        </section>
      </div>
      
      {/* Rating Modal */}
      {showRating && (
        <div className="modal-overlay">
          <div className="modal-content">
            <RatingForm
              onSubmit={handleRatingSubmit}
              onCancel={handleRatingCancel}
            />
          </div>
        </div>
      )}
      
      {/* Gentle Reminder Banner */}
      {showBanner && !match.is_rated_by_current_user && (
        <div className="rating-banner">
          How was your session with {match?.other_user?.name}?{" "}
          <button onClick={() => { setShowRating(true); setShowBanner(false); }}>
            Rate Now
          </button>
          <button className="close-banner" onClick={() => setShowBanner(false)}>×</button>
        </div>
      )}
    </div>
  );
};

export default ChatPage;
