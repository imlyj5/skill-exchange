import React from "react";
import AuthForm from "../AuthForm/AuthForm";

// Login form wrapper for AuthForm
const LoginForm = ({ onLogin }) => {
  const loginFields = [
    { name: "email", placeholder: "Email", type: "email" },
    { name: "password", placeholder: "Password", type: "password" }
  ];

  return (
    <AuthForm
      fields={loginFields}
      buttonText="Login"
      endpoint="/auth/login"
      onSubmit={onLogin}
      errorMessage="Invalid credentials"
    />
  );
};

export default LoginForm;
