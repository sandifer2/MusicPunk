// import { useState } from "react";
// import { Link } from "react-router-dom"
// import Table from "./Table";
// import '../CSS/Home.css'

// function Home() {


//   const [selectedCategory, setSelectedCategory] = useState("songs");
//   const [searchQuery, setSearchQuery] = useState("");
//   const [results, setResults] = useState([]);
//   const [tableCategory, setTableCategory] = useState("");
//   const handleSearch = (e) => {
//     e.preventDefault()
//     if (searchQuery.trim() === "") {
//       setResults([]); // or show a message saying "Please enter a search term"
//       return;
//     }
//     const category = selectedCategory || "songs";
//     fetch(`http://127.0.0.1:5000/api/${category}?search=${encodeURIComponent(searchQuery)}`)
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Failed to fetch songs");
//         }
//         return response.json();
//       })
//       .then((data) => {
//         setResults(data); // save songs from backend to state
//         console.log("Fetched songs:", data);

//       })
//       .catch((error) => {
//         console.error("Error fetching songs:", error);
//       });
//   };

//   return (
//     <div className="home-container">
//       <form onSubmit={handleSearch} className="search-form">
//         <select
//           value={selectedCategory}
//           onChange={(e) => setSelectedCategory(e.target.value)}
//           className="search-dropdown"
//         >
//           <option value="songs">Songs</option>
//           <option value="albums">Albums</option>
//           <option value="artists">Artists</option>
//         </select>

//         <input
//           type="text"
//           placeholder="Search..."
//           className="search-input"
//           value={searchQuery}
//           onChange={(e) => setSearchQuery(e.target.value)}
//         />

//         <button type="submit" className="search-button">Search</button>
//       </form>

//       {results.length > 0 && (
//         <div className="search-results">
//           <h2>Results:</h2>
//           <ul>
//             {results.map((item, index) => (
//               <li key={index}>
//                 {selectedCategory === "songs" && (
//                   <>
//                     <strong>{item.artist_name}</strong> — {item.song_title}
//                     <br />
//                     <span className="album-info">Album: {item.album_name}</span>
//                   </>
//                 )}

//                 {selectedCategory === "albums" && (
//                   <>
//                     <strong>{item.album_name}</strong>
//                     <br />
//                     <span className="album-info">By: {item.artist_name}</span>
//                   </>
//                 )}

//                 {selectedCategory === "artists" && (
//                   <>
//                     <strong>{item.artist_name}</strong>
//                     <br />
//                     <span className="album-info">Genre: {item.genre}</span>
//                   </>
//                 )}
//               </li>
//             ))}
//           </ul>
//         </div>
//       )}

//       <h1 className="home-title">Welcome to MusicBox!</h1>
//       <p className="home-subtitle">Please select an option you would like to rate:</p>

//       <div className="button-group">
//         <button className="category-button" onClick={() => setTableCategory("Artists")}>Artists</button>
//         <button className="category-button" onClick={() => setTableCategory("Songs")}>Songs</button>
//         <button className="category-button" onClick={() => setTableCategory("Albums")}>Albums</button>
//       </div>

//       <Table tableCategory={tableCategory} />
//     </div>
//   );


// }

// const buttonStyle = {
//   padding: "10px 20px",
//   margin: "0 10px",
//   border: "none",
//   borderRadius: "5px",
//   backgroundColor: "#1DB954", // Spotify Green
//   color: "white",
//   fontSize: "1rem",
//   cursor: "pointer",
//   transition: "0.3s",
// };

// export default Home;
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
                    // Assuming Spotify_ID is used for song identification
                    handleSongClick(item.spotify_id);
                  }
                }}
                style={{ cursor: selectedCategory === 'songs' ? 'pointer' : 'default' }}
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