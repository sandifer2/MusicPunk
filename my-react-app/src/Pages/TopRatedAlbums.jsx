import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../CSS/Page.css';

function TopRatedAlbums() {
  const [topAlbums, setTopAlbums] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/top-rated-albums')
      .then(response => {
        if (!response.ok) {
          throw new Error(`Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setTopAlbums(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching top rated albums:', error);
        setError(`Failed to load top rated albums: ${error.message}`);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="page-container"><h2>Loading...</h2></div>;
  
  if (error) return (
    <div className="page-container">
      <h2>Error: {error}</h2>
      <p>Please try again later or contact support if the problem persists.</p>
      <button 
        onClick={() => window.location.reload()}
        style={{ 
          backgroundColor: '#1DB954', 
          color: 'white',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer' 
        }}
      >
        Try Again
      </button>
    </div>
  );

  return (
    <div className="page-container">
      <h1>Top Rated Albums</h1>
      <p>Albums with an average rating of 4.0 or higher and at least 3 reviews</p>
      
      {topAlbums.length === 0 ? (
        <p>No albums meet the criteria yet</p>
      ) : (
        <div className="album-grid">
          {topAlbums.map(album => (
            <div 
              key={album.Album_ID}
              className="album-card"
              style={{
                backgroundColor: '#282828',
                padding: '20px',
                borderRadius: '10px',
                marginBottom: '20px'
              }}
            >
              <h2>{album.Album_Name}</h2>
              <p>Artist: {album.Artist_Name}</p>
              <div style={{ marginTop: '10px' }}>
                <span style={{ 
                  backgroundColor: '#1DB954',
                  color: 'white',
                  padding: '5px 10px',
                  borderRadius: '15px',
                  marginRight: '10px'
                }}>
                  ★ {album.avg_rating}
                </span>
                <span style={{ color: '#b3b3b3' }}>
                  {album.review_count} {album.review_count === 1 ? 'review' : 'reviews'}
                </span>
              </div>
              <Link 
                to={`/album/${album.Album_ID}`}
                style={{
                  display: 'inline-block',
                  marginTop: '15px',
                  color: '#1DB954',
                  textDecoration: 'none'
                }}
              >
                View Details
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TopRatedAlbums; 