import React, { useState } from "react";
import "./app.css";

function Body() {
  // State for customer name and email
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would send data to the backend
    setSubmitted(true);
  };

  return (
    <main>
      <div id="body">
        
      </div>
    <div class="left-panel">
    </div>

    </main>
  );
}

export default Body;
