import React, { useState } from "react";
import "./LandingPage.css";
import LoginForm from "../LoginForm/LoginForm";
import SignupForm from "../SignupForm/SignupForm";
// Illustration source: https://blush.design/collections/2CS20tnIa14HG1NsRPdP/brazuca
import LandingImg from "../../assets/Landing.png";

// Landing page for unauthenticated users
// Handles login/signup modal and navigation to How It Works
const LandingPage = ({ onLogin, onNavigate }) => {
  const [showModal, setShowModal] = useState(false);
  const [mode, setMode] = useState("login");
  const [signupSuccess, setSignupSuccess] = useState(false);

  // Handle login: call parent handler, close modal, reset signup state
  const handleLogin = (userData) => {
    onLogin && onLogin(userData);
    setShowModal(false);
    setSignupSuccess(false);
  };

  // Handle signup: show success message and switch to login mode
  const handleSignup = () => {
    setSignupSuccess(true);
    setMode("login");
  };

  return (
    <div className="landing-root">
      <nav className="landing-nav">
        <span className="logo">Skill Exchange App</span>
        <div className="nav-links">
          <button className="nav-btn" onClick={() => onNavigate("howitworks")}>How it works</button>
        </div>
      </nav>
      <div className="landing-content">
        <div className="landing-left">
          <h1 className="landing-title">
            YOUR NEXT SKILL IS ONE <br /> MATCH AWAY
          </h1>
          <p className="landing-subtitle">
            Make learning feel like meeting a friend. Match with people who share your interests, exchange skills, and grow together.
          </p>
          <button className="landing-btn" onClick={() => setShowModal(true)}>
            Login / Sign up
          </button>
        </div>
        <div className="landing-right">
          <img
            src={LandingImg}
            alt="People illustration"
            className="landing-illustration"
          />
        </div>
      </div>
      {showModal && (
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

export default LandingPage;
