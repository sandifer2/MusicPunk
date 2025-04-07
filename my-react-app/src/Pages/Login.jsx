import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../CSS/Login.css';

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to login");
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        navigate('/home');
      } else {
        alert(data.message);
      }
    })
    .catch((error) => {
      console.error("Error Logging in:", error);
      alert("Login failed. Please try again.");
    });
  };

  return (
    <section>
      {[...Array(200)].map((_, index) => (
        <span key={index}></span>
      ))}
      <div className="signin">
        <div className="content">
          <h2>Sign In</h2>
          <div className="form">
            <div className="inputBox">
              <input 
                type="text" 
                required 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <i>Username</i>
            </div>
            <div className="inputBox">
              <input 
                type="password" 
                required 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <i>Password</i>
            </div>
            <div className="links">
              <a href="#">Forgot Password</a>
              <a href="#">Signup</a>
            </div>
            <div className="inputBox">
              <input type="submit" value="Login" onClick={handleLogin} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Login;




