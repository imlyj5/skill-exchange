import React from "react";
import "./MatchCard.css";
import { API_URL } from "../App";

const MatchCard = ({ user, onChat, onViewProfile }) => {
  const getImageUrl = () => {
    if (!user.image_url) {
      return 'https://randomuser.me/api/portraits/lego/1.jpg';
    }
    if (user.image_url.startsWith('http')) {
      return user.image_url;
    }
    return `${API_URL}${user.image_url}`;
  };

  return (
  <div className="match-card">
      <div className="match-card-header">
        <img 
          src={getImageUrl()} 
          alt={user.name} 
          className="match-card-avatar" 
        />
    <div className="match-card-name">
      <span style={{ cursor: 'pointer', textDecoration: 'underline' }} onClick={() => onViewProfile && onViewProfile(user)}>{user.name}</span>
        </div>
    </div>
    <div className="match-card-info">
      <div>
        <b>Skill I offer:</b> {(user.skills_to_offer || []).join(", ")}
      </div>
      <div>
        <b>Wants to learn:</b> {(user.skills_to_learn || []).join(", ")}
      </div>
    </div>
    <div className="match-card-rating">
      {Array.from({ length: 5 }).map((_, i) => (
          <span key={i} className={i < Math.round(user.average_rating || 0) ? "star filled" : "star"}>★</span>
      ))}
    </div>
    <button className="chat-btn" onClick={() => onChat(user)}>Chat</button>
  </div>
);
};

export default MatchCard;
