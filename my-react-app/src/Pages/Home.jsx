import { useState } from "react";
import { Link, useNavigate } from "react-router-dom"
import Table from "./Table";
import '../CSS/Home.css'
import { motion } from 'framer-motion'


function Home() {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState("songs");
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState([]);
  const [tableCategory, setTableCategory] = useState("");

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim() === "") {
      setResults([]); 
      return;
    }
    const category = selectedCategory || "songs";
    fetch(`http://127.0.0.1:5000/api/${category}?search=${encodeURIComponent(searchQuery)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch songs");
        }
        return response.json();
      })
      .then((data) => {
        setResults(data);
        console.log("Fetched songs:", data);
      })
      .catch((error) => {
        console.error("Error fetching songs:", error);
      });
  };

  const handleSongClick = (spotifyId) => {
    navigate(`/song/${spotifyId}`);
  };

  const handleAlbumClick = (albumId) => {
    navigate(`/album/${albumId}`);
  };

  const handleArtistClick = (artistId) => {
    navigate(`/artist/${artistId}`);
  };

  return (
    <motion.div
    initial={{ opacity: 0}}
    animate ={{opacity: 1}}
    exit = {{opacity: 0}}
    transition = {{ duration: 1}}
    >
      <div className="home-container">
      {/* Cyberpunk Background Effects */}
      <div className="cyber-grid"></div>
      <div className="scan-lines"></div>
      
      {/* Hero Section */}
      <div className="cyber-hero">
        <div className="glitch" data-text="MUSICPUNK">MUSICPUNK</div>
        <div className="hero-subtitle">
          <span className="cyber-text">NEURAL_MUSIC_INTERFACE_</span>
          <span className="blink">▮</span>
        </div>
      </div>

      {/* Search Terminal */}
      <div className="search-terminal">
        <div className="terminal-header">
          <span className="terminal-dots">
            <span className="dot dot-red"></span>
            <span className="dot dot-yellow"></span>
            <span className="dot dot-green"></span>
          </span>
          <span className="terminal-title">SEARCH_PROTOCOL_V2.0</span>
        </div>
        
        <form onSubmit={handleSearch} className="cyber-search-form">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="cyber-select"
          >
            <option value="songs">[SONGS]</option>
            <option value="albums">[ALBUMS]</option>
            <option value="artists">[ARTISTS]</option>
          </select>

          <input
            type="text"
            placeholder="ENTER_QUERY..."
            className="cyber-input"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />

          <button type="submit" className="cyber-button">
            <span>EXECUTE</span>
          </button>
        </form>
      </div>

      {/* Category Cards */}
      <div className="cyber-categories">
        <div className="category-card" onClick={() => setTableCategory("Artists")}>
          <div className="card-inner">
            <span className="card-number">01</span>
            <span className="card-title">ARTISTS</span>
            <div className="card-glow"></div>
          </div>
        </div>
        
        <div className="category-card" onClick={() => setTableCategory("Songs")}>
          <div className="card-inner">
            <span className="card-number">02</span>
            <span className="card-title">SONGS</span>
            <div className="card-glow"></div>
          </div>
        </div>
        
        <div className="category-card" onClick={() => setTableCategory("Albums")}>
          <div className="card-inner">
            <span className="card-number">03</span>
            <span className="card-title">ALBUMS</span>
            <div className="card-glow"></div>
          </div>
        </div>
      </div>

      {/* Results Display - Keep your existing logic but with new styling */}
      {results.length > 0 && (
        <div className="cyber-results">
          <h2 className="results-header">
            <span className="results-icon">▶</span> DATA_RETRIEVED
          </h2>
          <div className="results-grid">
            {results.map((item, index) => (
              <div key={index} className="result-card">
                {/* Keep your existing result display logic */}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Table - wrapped in cyber styling */}
      <div className="cyber-table-container">
        <Table tableCategory={tableCategory} />
      </div>
    </div>
  );
    </motion.div>
  );
}

export default Home;