import React, { useState, useRef } from "react";
import axios from "axios";
import "./ProfilePage.css";
import UserDropdown from "../UserDropdown/UserDropdown";
import { API_URL } from "../../App";
import LegoAvatar from "../../assets/lego-avatar.jpg";

// Profile page for viewing and editing user information
// Handles avatar upload, field editing, and profile section rendering
const ProfilePage = ({ user, onSave, onNavigate, isReadOnly, onLogout }) => {
  const [editField, setEditField] = useState(null);
  const [editValue, setEditValue] = useState("");
  const [uploadPreview, setUploadPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  // Handle edit button: set the field to be edited and initialize edit value
  const handleEdit = (field) => {
    setEditField(field);
    if (field === "user_info") {
      setEditValue({
        name: user.name || "",
        pronouns: user.pronouns || "",
        email: user.email || ""
      });
    } else if (field === "skills_to_learn" || field === "skills_to_offer") {
      setEditValue([...(user[field] || []), "", "", ""].slice(0,3));
    } else {
      setEditValue(user[field] || "");
    }
  };

  // Handle image selection: preview and upload new avatar
  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Preview the selected image
      const reader = new FileReader();
      reader.onloadend = () => {
        setUploadPreview(reader.result);
      };
      reader.readAsDataURL(file);

      // Upload the image
      handleImageUpload(file);
    }
  };

  // Handle image upload: send file to backend and update user
  const handleImageUpload = async (file) => {
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await axios.post(`${API_URL}/upload/profile-image/${user.id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Update the user data with the new image URL
      const updatedUser = {
        ...user,
        image_url: response.data.image_url
      };
      onSave(updatedUser);
      setUploadPreview(null);
    } catch (error) {
      console.error('Error uploading image:', error);
      alert('Failed to upload image. Please try again.');
      setUploadPreview(null);
    } finally {
      setUploading(false);
    }
  };

  // Handle save: update profile field via API and update parent state
  const handleSave = async () => {
    try {
      let value = editValue;
      let payload = {};
      if (editField === "skills_to_learn" || editField === "skills_to_offer") {
        value = editValue.map(s => s.trim()).filter(Boolean).slice(0,3);
        payload[editField] = value;
      } else if (editField === "user_info") {
        payload = {
          name: editValue.name,
          pronouns: editValue.pronouns,
          email: editValue.email
        };
      } else {
        payload[editField] = editValue;
      }
      const res = await axios.put(`${API_URL}/profile/${user.id}`, payload);
      onSave(res.data);
      setEditField(null);
      setEditValue("");
    } catch (err) {
      alert("Failed to update profile.");
    }
  };

  // Handle cancel: reset edit state
  const handleCancel = () => {
    setEditField(null);
    setEditValue("");
  };

  return (
    <div className="profile-bg">
      { !isReadOnly && (
        <div className="profile-header">
          <span className="profile-logo">Skill Exchange App</span>
          <UserDropdown user={user} onNavigate={onNavigate} onLogout={onLogout} />
        </div>
      )}
      <div className="profile-main">
        <div className="profile-card profile-left">
          <div className="profile-avatar-section">
            <div className="profile-avatar-container">
              {uploadPreview ? (
                <img src={uploadPreview} alt="preview" className="profile-avatar" />
              ) : (
                <img 
                  src={user.image_url ? (user.image_url.startsWith('http') ? user.image_url : `${API_URL}${user.image_url}`) : LegoAvatar} 
                  alt="avatar" 
                  className="profile-avatar" 
                />
              )}
              {uploading && <div className="upload-overlay">Uploading...</div>}
            </div>
            {!isReadOnly && (
              <>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageSelect}
                  accept="image/*"
                  style={{ display: 'none' }}
                />
                <button 
                  className="profile-upload-btn"
                  onClick={() => fileInputRef.current.click()}
                  disabled={uploading}
                >
                  {uploading ? 'Uploading...' : 'Upload Photo'}
                </button>
              </>
            )}
          </div>
          <div className="profile-section">
            <div className="profile-section-header">
              User Info {(!isReadOnly && editField !== "user_info") && (<button className="profile-edit-btn" onClick={() => handleEdit("user_info")}>Edit</button>)}
            </div>
            <div className="profile-section-content">
              {editField === "user_info" ? (
                <>
                  <div>Your Name: <input value={editValue.name} onChange={e => setEditValue({ ...editValue, name: e.target.value })} /></div>
                  <div>Pronouns: <input value={editValue.pronouns} onChange={e => setEditValue({ ...editValue, pronouns: e.target.value })} /></div>
                  <div>Email: <input value={editValue.email} onChange={e => setEditValue({ ...editValue, email: e.target.value })} /></div>
                  <button onClick={handleSave}>Save</button>
                  <button onClick={handleCancel}>Cancel</button>
                </>
              ) : (
                <>
                  <div>Your Name: <b>{user.name || "Not set"}</b></div>
                  <div>Pronouns: <b>{user.pronouns || "Not set"}</b></div>
                  <div>Email: <b>{user.email || "Not set"}</b></div>
                </>
              )}
            </div>
          </div>
          <div className="profile-section">
            <div className="profile-section-header">
              About Me {(!isReadOnly && editField !== "bio") && (<button className="profile-edit-btn" onClick={() => handleEdit("bio")}>Edit</button>)}
            </div>
            <div className="profile-section-content">
              {editField === "bio" ? (
                <>
                  <textarea
                    value={editValue}
                    onChange={e => setEditValue(e.target.value)}
                  />
                  <button onClick={handleSave}>Save</button>
                  <button onClick={handleCancel}>Cancel</button>
                </>
              ) : (
                <div>{user.bio || "Not set"}</div>
              )}
            </div>
          </div>
          <div className="profile-section">
            <div className="profile-section-header">
              Want to Learn {(!isReadOnly && editField !== "skills_to_learn") && (<button className="profile-edit-btn" onClick={() => handleEdit("skills_to_learn")}>Edit</button>)}
            </div>
            <div className="profile-section-content">
              {editField === "skills_to_learn" ? (
                <>
                  {[0,1,2].map(i => (
                    <input
                      key={i}
                      value={editValue[i] || ""}
                      onChange={e => {
                        const newSkills = [...editValue];
                        newSkills[i] = e.target.value;
                        setEditValue(newSkills);
                      }}
                      placeholder={`Skill ${i+1}`}
                    />
                  ))}
                  <button onClick={handleSave}>Save</button>
                  <button onClick={handleCancel}>Cancel</button>
                </>
              ) : (
                (user.skills_to_learn && user.skills_to_learn.length > 0)
                  ? user.skills_to_learn.map(skill => (
                      <span className="profile-skill" key={skill}>{skill}</span>
                    ))
                  : "Not set"
              )}
            </div>
          </div>
          <div className="profile-section">
            <div className="profile-section-header">
              Skill to Offer {(!isReadOnly && editField !== "skills_to_offer") && (<button className="profile-edit-btn" onClick={() => handleEdit("skills_to_offer")}>Edit</button>)}
            </div>
            <div className="profile-section-content">
              {editField === "skills_to_offer" ? (
                <>
                  {[0,1,2].map(i => (
                    <input
                      key={i}
                      value={editValue[i] || ""}
                      onChange={e => {
                        const newSkills = [...editValue];
                        newSkills[i] = e.target.value;
                        setEditValue(newSkills);
                      }}
                      placeholder={`Skill ${i+1}`}
                    />
                  ))}
                  <button onClick={handleSave}>Save</button>
                  <button onClick={handleCancel}>Cancel</button>
                </>
              ) : (
                (user.skills_to_offer && user.skills_to_offer.length > 0)
                  ? user.skills_to_offer.map(skill => (
                      <span className="profile-skill" key={skill}>{skill}</span>
                    ))
                  : "Not set"
              )}
            </div>
          </div>
        </div>
        <div className="profile-card profile-right">
          <div className="profile-section">
            <div className="profile-section-header">
              Location {(!isReadOnly && editField !== "location") && (<button className="profile-edit-btn" onClick={() => handleEdit("location")}>Edit</button>)}
            </div>
            <div className="profile-section-content">
              {editField === "location" ? (
                <>
                  <input value={editValue} onChange={e => setEditValue(e.target.value)} />
                  <button onClick={handleSave}>Save</button>
                  <button onClick={handleCancel}>Cancel</button>
                </>
              ) : (
                user.location || "Not set"
              )}
            </div>
          </div>
          <div className="profile-section">
            <div className="profile-section-header">
              Availability {(!isReadOnly && editField !== "availability") && (<button className="profile-edit-btn" onClick={() => handleEdit("availability")}>Edit</button>)}
            </div>
            <div className="profile-section-content">
              {editField === "availability" ? (
                <>
                  <input value={editValue} onChange={e => setEditValue(e.target.value)} />
                  <button onClick={handleSave}>Save</button>
                  <button onClick={handleCancel}>Cancel</button>
                </>
              ) : (
                user.availability || "Not set"
              )}
            </div>
          </div>
          <div className="profile-section">
            <div className="profile-section-header">
              Learning Style {(!isReadOnly && editField !== "learning_style") && (<button className="profile-edit-btn" onClick={() => handleEdit("learning_style")}>Edit</button>)}
            </div>
            <div className="profile-section-content">
              {editField === "learning_style" ? (
                <>
                  <input value={editValue} onChange={e => setEditValue(e.target.value)} />
                  <button onClick={handleSave}>Save</button>
                  <button onClick={handleCancel}>Cancel</button>
                </>
              ) : (
                user.learning_style || "Not set"
              )}
            </div>
          </div>
          <div className="profile-section">
            <div className="profile-section-header">Average Rating</div>
            <div className="profile-section-content">
              {Array.from({ length: 5 }).map((_, i) => (
                <span key={i} className={i < Math.round(user.average_rating || 0) ? "star filled" : "star"}>★</span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;