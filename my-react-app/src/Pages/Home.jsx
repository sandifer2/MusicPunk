import { useState } from "react";
import { Link } from "react-router-dom"
import Table from "./Table";
import '../CSS/Home.css'

function Home() {


  const [selectedCategory, setSelectedCategory] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [songs, setSongs] = useState([]);
  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim() === "") {
      setSongs([]); // or show a message saying "Please enter a search term"
      return;
    }
    fetch(`http://127.0.0.1:5000/api/songs?search=${encodeURIComponent(searchQuery)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch songs");
        }
        return response.json();
      })
      .then((data) => {
        setSongs(data); // save songs from backend to state
        console.log("Fetched songs:", data);

      })
      .catch((error) => {
        console.error("Error fetching songs:", error);
      });
  };





  return (
    <div className="home-container">
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search for songs"
          className="search-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="search-button">Search</button>
      </form>

      {songs.length > 0 && (
        <div className="search-results">
          <h2>Results:</h2>
          <ul>
            {songs.map((song, index) => (
              <li key={index}>
                <strong>{song.Artist_Name}</strong> — {song.Title}
              </li>
            ))}
          </ul>
        </div>
      )}

      <h1 className="home-title">Welcome to MusicBox!</h1>
      <p className="home-subtitle">Please select an option you would like to rate:</p>

      <div className="button-group">
        <button className="category-button" onClick={() => setSelectedCategory("Artists")}>Artists</button>
        <button className="category-button" onClick={() => setSelectedCategory("Songs")}>Songs</button>
        <button className="category-button" onClick={() => setSelectedCategory("Albums")}>Albums</button>
      </div>

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

export default Home;