import React from "react";
import AuthForm from "../AuthForm/AuthForm";

// Signup form wrapper for AuthForm
const SignupForm = ({ onSignup }) => {
  const signupFields = [
    { name: "name", placeholder: "Name" },
    { name: "email", placeholder: "Email", type: "email" },
    { name: "password", placeholder: "Password", type: "password" }
  ];

  return (
    <AuthForm
      fields={signupFields}
      buttonText="Sign Up"
      endpoint="/auth/signup"
      onSuccess={onSignup}
      errorMessage="Signup failed"
    />
  );
};

export default SignupForm;
