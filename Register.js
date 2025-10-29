import React, { useState } from "react";
import "./Register.css";

export default function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Đăng ký thành công!");
  };

  return (
    <div className="register-page">
      <div className="form-container">
        <h1 className="logo">3CE <span className="title">Room Search</span></h1>
        <h2 className="create-title">Create an account</h2>
        <p className="subtitle">Enter your email to sign up for this website</p>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="input"
          />
          <input
            type="email"
            placeholder="email@domain.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input"
          />

          <button type="submit" className="signup-btn">
            Sign up
          </button>
        </form>

        <a href="/" className="home-link">Go to Home Page</a>

        <p className="policy-text">
          By clicking continue, you agree to our <strong>Terms of Service</strong> and <strong>Privacy Policy</strong>
        </p>
      </div>
    </div>
  );
}
