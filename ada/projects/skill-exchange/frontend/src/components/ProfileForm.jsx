import React, { useState } from "react";
import "./ProfileForm.css";

const MAX_SKILLS = 3;

const ProfileForm = ({
  initialProfile,
  onSave,
  onCancel
}) => {
  const [form, setForm] = useState(initialProfile);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  // Handle skills (comma separated)
  const handleSkillChange = (e, type) => {
    let skills = e.target.value.split(",").map(s => s.trim()).filter(Boolean);
    if (skills.length > MAX_SKILLS) skills = skills.slice(0, MAX_SKILLS);
    setForm({ ...form, [type]: skills });
  };

  // Handle availability (comma separated)
  const handleAvailabilityChange = (e) => {
    let days = e.target.value.split(",").map(d => d.trim()).filter(Boolean);
    setForm({ ...form, availability: days });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(form);
  };

  return (
    <form className="profile-form" onSubmit={handleSubmit}>
      <h2>Edit Profile</h2>
      <label>
        Name:
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Pronouns:
        <input
          name="pronouns"
          value={form.pronouns}
          onChange={handleChange}
        />
      </label>
      <label>
        Email:
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Bio:
        <textarea
          name="bio"
          value={form.bio}
          onChange={handleChange}
          rows={3}
        />
      </label>
      <label>
        Want to Learn (comma separated, max 3):
        <input
          value={form.wantToLearn.join(", ")}
          onChange={e => handleSkillChange(e, "wantToLearn")}
          placeholder="e.g. Guitar, Painting, Coding"
        />
      </label>
      <label>
        Skills to Offer (comma separated, max 3):
        <input
          value={form.skillsToOffer.join(", ")}
          onChange={e => handleSkillChange(e, "skillsToOffer")}
          placeholder="e.g. Golf, Violin"
        />
      </label>
      <label>
        Location:
        <input
          name="location"
          value={form.location}
          onChange={handleChange}
        />
      </label>
      <label>
        Availability (comma separated):
        <input
          value={form.availability.join(", ")}
          onChange={handleAvailabilityChange}
          placeholder="e.g. Mon, Tue, Wed"
        />
      </label>
      <label>
        Learning Style:
        <select
          name="learningStyle"
          value={form.learningStyle}
          onChange={handleChange}
        >
          <option value="in-person">In-person</option>
          <option value="online">Online</option>
          <option value="hybrid">Hybrid</option>
        </select>
      </label>
      <div className="profile-form-actions">
        <button type="submit" className="save-btn">Save</button>
        <button type="button" className="cancel-btn" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
};

export default ProfileForm;
