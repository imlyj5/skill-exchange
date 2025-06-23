import React, { useState } from "react";
import axios from "axios";
import { API_URL } from "../../App";

// Generic authentication form for login/signup
// Handles dynamic fields, API call, and error display
const AuthForm = ({ 
  fields, 
  buttonText, 
  onSubmit, 
  endpoint, 
  onSuccess, 
  errorMessage = "Authentication failed"
}) => {
  const [formData, setFormData] = useState(
    fields.reduce((acc, field) => {
      acc[field.name] = "";
      return acc;
    }, {})
  );
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    
    try {
      const res = await axios.post(
        `${API_URL}${endpoint}`,
        formData,
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true
        }
      );
      
      if (onSuccess) {
        onSuccess(res.data);
      } else {
        onSubmit(res.data);
      }
    } catch (err) {
      console.error("Authentication failed:", err);
      if (err.response) {
        console.error("Error response data:", err.response.data);
      }
      setError(errorMessage);
    }
  };

  const handleInputChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      {fields.map((field) => (
        <input
          key={field.name}
          type={field.type || "text"}
          value={formData[field.name]}
          onChange={(e) => handleInputChange(field.name, e.target.value)}
          placeholder={field.placeholder}
          required={field.required !== false}
        />
      ))}
      <button type="submit" className="auth-submit-btn">{buttonText}</button>
      {error && <div className="error">{error}</div>}
    </form>
  );
};

export default AuthForm; 