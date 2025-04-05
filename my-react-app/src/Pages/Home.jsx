import { useState } from "react";
import { Link } from "react-router-dom"
import Table from "./Table";

function Home() {
    const [selectedCategory, setSelectedCategory] = useState("");
    const [searchQuery, setSearchQuery] = useState("");
    const [songs, setSongs] = useState([]);
    const handleSearch = (e) => {
        e.preventDefault()
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
        <div style={{ textAlign: "center", fontFamily: "Arial, sans-serif", color: "white", backgroundColor: "#181818", height: "100vh", paddingTop: "50px" }}>

            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    placeholder="Search for songs"
                    className="search-input"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type="submit" className="search-Button">Search</button>
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

export default Home;