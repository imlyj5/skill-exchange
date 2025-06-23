import React, { useState, useEffect } from "react";
import "./MatchSuggestionsPage.css";
import MatchCard from "../MatchCard/MatchCard";
import UserDropdown from "../UserDropdown/UserDropdown";
import ProfilePage from "../ProfilePage/ProfilePage";
import { API_URL } from "../../App";

const CARDS_PER_VIEW = 3;

const MatchSuggestionsPage = ({
  onChat,
  onNavigateProfile,
  onNavigate,
  user,
  viewedUser,
  setViewedUser,
  onLogout,
}) => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [startIdx, setStartIdx] = useState(0);
  const [aiEnabled, setAiEnabled] = useState(false);

  useEffect(() => {
    if (user && user.id) {
      setLoading(true);
      fetch(`${API_URL}/matches/${user.id}`)
        .then(res => res.json())
        .then(data => {
          setMatches(data.matches || []);
          setAiEnabled(data.ai_enabled);
        })
        .catch(() => setMatches([]))
        .finally(() => setLoading(false));
    }
  }, [user]);

  useEffect(() => {
    console.log("MATCHES STATE UPDATED in MatchSuggestionsPage:", matches);
  }, [matches]);

  const handlePrev = () => {
    setStartIdx((prev) => Math.max(prev - CARDS_PER_VIEW, 0));
  };

  const handleNext = () => {
    setStartIdx((prev) =>
      Math.min(prev + CARDS_PER_VIEW, (matches || []).length - CARDS_PER_VIEW)
    );
  };

  const visibleMatches = (matches || []).slice(startIdx, startIdx + CARDS_PER_VIEW);

  if (loading) {
    return <div className="match-bg"><div>Loading matches...</div></div>;
  }

  if (viewedUser) {
    return (
      <div className="match-bg">
        <button
          onClick={() => setViewedUser(null)}
          style={{ margin: '24px auto 16px', display: 'block' }}
        >
          &larr; Back to Matches
        </button>
        <ProfilePage user={viewedUser} isReadOnly={true} />
      </div>
    );
  }

  return (
    <div className="match-bg">
      <div className="match-header">
        <span className="match-logo" onClick={onNavigateProfile} style={{ cursor: "pointer" }}>
          Skill Exchange App
        </span>
        <UserDropdown user={user} onNavigate={onNavigate} onLogout={onLogout} />
      </div>
      <div className="match-title">
        <h1 className="match-suggestions-title">Match Suggestions</h1>
        <p>Here are your perfect learning partner! Chat Now!</p>
      </div>
      <div className="match-cards-row">
        <button
          className="arrow-btn"
          aria-label="Previous"
          onClick={handlePrev}
          disabled={startIdx === 0}
        >{'<'}</button>
        {visibleMatches.length === 0 ? (
          <div>No matches found.</div>
        ) : (
          visibleMatches.map((user) => (
            <MatchCard key={user.id} user={user} onChat={onChat} onViewProfile={setViewedUser} />
          ))
        )}
        <button
          className="arrow-btn"
          aria-label="Next"
          onClick={handleNext}
          disabled={startIdx + CARDS_PER_VIEW >= (matches || []).length}
        >{'>'}</button>
      </div>
      {aiEnabled ? (
        <div className="ai-status ai-enabled">
          AI Matching is enabled!
        </div>
      ) : (
        <div className="ai-status ai-disabled">
          AI Matching is currently unavailable due to quota may be exceeded.
        </div>
      )}
    </div>
  );
};

export default MatchSuggestionsPage;