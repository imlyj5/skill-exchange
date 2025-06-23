import React, { useState, useRef, useEffect } from "react";
import "./UserDropdown.css";
import { API_URL } from "../../App";
import LegoAvatar from "../../assets/lego-avatar.jpg";

const UserDropdown = ({ user, onNavigate, onLogout }) => {
  const [open, setOpen] = useState(false);
  const ref = useRef();

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (!user) return null;

  const handleLogout = () => {
    setOpen(false);
    onLogout && onLogout();
  };
  
  const getImageUrl = () => {
    if (!user.image_url) {
      return LegoAvatar;
    }
    if (user.image_url.startsWith('http')) {
      return user.image_url;
    }
    return `${API_URL}${user.image_url}`;
  };

  return (
    <div className="user-dropdown" ref={ref}>
      <button className="user-dropdown-btn" onClick={() => setOpen((o) => !o)}>
        <img 
          src={getImageUrl()} 
          alt={user.name} 
          className="user-dropdown-avatar" 
        />
        <span>
          Welcome back,<br />
          <b>{user.name}</b>
        </span>
        <span className="user-dropdown-arrow">{open ? "▲" : "▼"}</span>
      </button>
      {open && (
        <div className="user-dropdown-menu">
          <button onClick={() => { onNavigate("howitworks"); setOpen(false); }}>How it works</button>
          <button onClick={() => { onNavigate("profile"); setOpen(false); }}>Profile</button>
          <button onClick={() => { onNavigate("chat"); setOpen(false); }}>Messages</button>
          <button onClick={() => { 
            onNavigate("matches"); 
            setOpen(false); 
          }}>Match Suggestions</button>
          <div className="user-dropdown-divider"></div>
          <button onClick={handleLogout} className="user-dropdown-logout">Logout</button>
        </div>
      )}
    </div>
  );
};

export default UserDropdown;
