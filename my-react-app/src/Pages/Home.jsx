import { useState } from "react";
import { Link, useNavigate } from "react-router-dom"
import Table from "./Table";
import '../CSS/Home.css'


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
    <div className="home-container">
      <form onSubmit={handleSearch} className="search-form">
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="search-dropdown"
        >
          <option value="songs">Songs</option>
          <option value="albums">Albums</option>
          <option value="artists">Artists</option>
        </select>

        <input
          type="text"
          placeholder="Search..."
          className="search-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />

        <button type="submit" className="search-button">Search</button>
      </form>

      {results.length > 0 && (
        <div className="search-results">
          <h2>Results:</h2>
          <ul>
            {results.map((item, index) => (
              <li 
                key={index} 
                onClick={() => {
                  if (selectedCategory === 'songs') {
                    handleSongClick(item.spotify_id);
                  } else if (selectedCategory === 'albums') {
                    handleAlbumClick(item.Album_ID);
                  } else if (selectedCategory === 'artists') {
                    handleArtistClick(item.Artist_ID);
                  }
                }}
                style={{ cursor: (selectedCategory === 'songs' || selectedCategory === 'albums' || selectedCategory === 'artists') ? 'pointer' : 'default' }}
              >
                {selectedCategory === "songs" && (
                  <>
                    <strong>{item.artist_name}</strong> — {item.song_title}
                    <br />
                    <span className="album-info">Album: {item.album_name}</span>
                  </>
                )}

                {selectedCategory === "albums" && (
                  <>
                    <strong>{item.album_name}</strong>
                    <br />
                    <span className="album-info">By: {item.artist_name}</span>
                  </>
                )}
                {selectedCategory === "artists" && (
                  <>
                    <strong>{item.artist_name}</strong>
                    <br />
                    <span className="album-info">Genre: {item.genre}</span>
                  </>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      <h1 className="home-title">Welcome to MusicBox!</h1>
      <p className="home-subtitle">Please select an option you would like to rate:</p>

      <div className="button-group">
        <button className="category-button" onClick={() => setTableCategory("Artists")}>Artists</button>
        <button className="category-button" onClick={() => setTableCategory("Songs")}>Songs</button>
        <button className="category-button" onClick={() => setTableCategory("Albums")}>Albums</button>
      </div>

      <Table tableCategory={tableCategory} />
    </div>
  );
}

export default Home;