import React, { useState } from "react";
import "./RatingForm.css";

const MAX_STARS = 5;

const RatingForm = ({ onSubmit, onCancel, initialRating = 0, initialFeedback = "" }) => {
  const [rating, setRating] = useState(initialRating);
  const [hover, setHover] = useState(0);
  const [feedback, setFeedback] = useState(initialFeedback);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ rating, feedback });
  };

  return (
    <form className="rating-form" onSubmit={handleSubmit}>
      <h2>Rate Your Session</h2>
      <div className="stars">
        {Array.from({ length: MAX_STARS }).map((_, i) => (
          <span
            key={i}
            className={`star${(hover || rating) > i ? " filled" : ""}`}
            onClick={() => setRating(i + 1)}
            onMouseEnter={() => setHover(i + 1)}
            onMouseLeave={() => setHover(0)}
            role="button"
            tabIndex={0}
            aria-label={`Rate ${i + 1} star${i > 0 ? "s" : ""}`}
          >
            ★
          </span>
        ))}
      </div>
      <textarea
        className="feedback-input"
        placeholder="Leave feedback (optional)..."
        value={feedback}
        onChange={e => setFeedback(e.target.value)}
        rows={3}
      />
      <div className="rating-form-actions">
        <button type="submit" className="submit-btn" disabled={rating === 0}>
          Submit
        </button>
        <button type="button" className="cancel-btn" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
};

export default RatingForm;
