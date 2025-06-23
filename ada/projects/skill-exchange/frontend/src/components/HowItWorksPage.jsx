import React, { useState } from "react";
import UserDropdown from "./UserDropdown";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";
import "./LandingPage.css";
import LandingImg from "../assets/Landing.png";

const HowItWorksPage = ({ user, onLogin, onNavigate, onLogout }) => {
  const [showModal, setShowModal] = useState(false);
  const [mode, setMode] = useState("login"); // or "signup"
  const [signupSuccess, setSignupSuccess] = useState(false);

  const handleLogin = (userData) => {
    onLogin && onLogin(userData);
    setShowModal(false);
    setSignupSuccess(false);
  };

  const handleSignup = () => {
    setSignupSuccess(true);
    setMode("login");
  };

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
          {!user && (
            <button className="landing-btn" onClick={() => setShowModal(true)}>
              Login / Sign up
            </button>
          )}
        </div>
        <div className="landing-right">
          <img
            src={LandingImg}
            alt="People illustration"
            className="landing-illustration"
          />
        </div>
      </div>
      {showModal && !user && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="auth-toggle">
              <button
                className={mode === "login" ? "active" : ""}
                onClick={() => setMode("login")}
              >
                Login
              </button>
              <button
                className={mode === "signup" ? "active" : ""}
                onClick={() => setMode("signup")}
              >
                Sign Up
              </button>
            </div>
            {signupSuccess && (
              <div className="success-message">
                Sign up successful! Please login.
              </div>
            )}
            {mode === "login" ? (
              <LoginForm onLogin={handleLogin} />
            ) : (
              <SignupForm onSignup={handleSignup} />
            )}
            <button className="close-modal" onClick={() => setShowModal(false)}>×</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default HowItWorksPage;
