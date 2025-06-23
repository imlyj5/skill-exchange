import React from "react";
import UserDropdown from "../UserDropdown/UserDropdown";
import "../LandingPage/LandingPage.css";
import LandingImg from "../../assets/Landing.png";

// How It Works informational page
const HowItWorksPage = ({ user, onNavigate, onLogout }) => {
  return (
    <div className="landing-root">
      <nav className="landing-nav">
        <span className="logo">Skill Exchange App</span>
        {user ? (
          <UserDropdown user={user} onNavigate={onNavigate} onLogout={onLogout} />
        ) : (
          <div className="nav-links">
            <button className="nav-btn" onClick={() => onNavigate && onNavigate('landing')}>Home</button>
          </div>
        )}
      </nav>
      <div className="landing-content">
        <div className="landing-left">
          <h1 className="landing-title">HOW IT WORKS</h1>
          <ol className="howitworks-steps">
            <li>
              <span role="img" aria-label="explore">🔍</span> Explore match cards
            </li>
            <li>
              <span role="img" aria-label="find">👤</span> Find the person you want to chat
            </li>
            <li>
              <span role="img" aria-label="chat">💬</span> Start a chat
            </li>
            <li>
              <span role="img" aria-label="calendar">📅</span> Discuss a time to learn together
            </li>
            <li>
              <span role="img" aria-label="meet">🤝</span> Meet and learn together
            </li>
            <li>
              <span role="img" aria-label="rate">⭐</span> After the session, mark complete to rate your partner
            </li>
          </ol>
        </div>
        <div className="landing-right">
          <img
            src={LandingImg}
            alt="People illustration"
            className="landing-illustration"
          />
        </div>
      </div>
    </div>
  );
};

export default HowItWorksPage;
