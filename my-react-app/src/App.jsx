import { useState } from "react";
import Table from "./Table";

function App() {
  const [selectedCategory, setSelectedCategory] = useState("");

  return (
    <div style={{ textAlign: "center", fontFamily: "Arial, sans-serif", color: "white", backgroundColor: "#181818", height: "100vh", paddingTop: "50px" }}>
      <h1 style={{ fontSize: "2.5rem" }}>Welcome to MusicBox!</h1>
      <p style={{ fontSize: "1.2rem", marginBottom: "20px" }}>Please select an option you would like to rate:</p>

      {/* Main Buttons */}
      <div style={{ marginBottom: "40px" }}>
        <button style={buttonStyle} onClick={() => setSelectedCategory("Artists")}>Artists</button>
        <button style={buttonStyle} onClick={() => setSelectedCategory("Songs")}>Songs</button>
        <button style={buttonStyle} onClick={() => setSelectedCategory("Albums")}>Albums</button>
      </div>

      {/* Table Section */}
      <Table selectedCategory={selectedCategory} />
    </div>
  );
}

const buttonStyle = {
  padding: "10px 20px",
  margin: "0 10px",
  border: "none",
  borderRadius: "5px",
  backgroundColor: "#1DB954", // Spotify Green
  color: "white",
  fontSize: "1rem",
  cursor: "pointer",
  transition: "0.3s",
};

export default App;