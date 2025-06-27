import React from "react";
import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div className="auth-form-wrapper">
      <div className="auth-form">
        <h1>Get To The Bag Today!</h1>
        {/* ...existing code (search bar, etc)... */}
        <Link to="/login">
          <button>Login</button>
        </Link>
        <Link to="/sign-up">
          <button>Sign Up</button>
        </Link>
      </div>
    </div>)
}

export default HomePage;