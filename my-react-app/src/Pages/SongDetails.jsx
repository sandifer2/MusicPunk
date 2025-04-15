import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../CSS/Page.css';

function SongDetails() {
  const { songId } = useParams();
  console.log("SongDetails component mounted");
  console.log("Song ID from URL params:", songId);

  const [songDetails, setSongDetails] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [rating, setRating] = useState(3);
  const [reviewText, setReviewText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch song details and reviews when component mounts
  useEffect(() => {
    if (!songId) {
      setError("Song ID is missing");
      setLoading(false);
      return;
    }

    console.log("Making API request to:", `http://127.0.0.1:5000/api/song/${songId}`);
    
    // Fetch song details
    fetch(`http://127.0.0.1:5000/api/song/${songId}`)
      .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
          return response.json().then(errorData => {
            console.error("Error data:", errorData);
            throw new Error(`Status: ${response.status}, Message: ${errorData.error || 'Unknown error'}`);
          }).catch(err => {
            // If can't parse error as JSON
            throw new Error(`Status: ${response.status}`);
          });
        }
        return response.json();
      })
      .then(data => {
        console.log("Fetched song details:", data);
        setSongDetails(data);
        setLoading(false);
      })  
      .catch(error => {
        console.error('Error fetching song details:', error);
        setError(`Failed to load song details: ${error.message}`);
        setLoading(false);
      });

    // Fetch reviews for this song
    fetch(`http://127.0.0.1:5000/api/song_reviews/${songId}`)
      .then(response => response.json())
      .then(data => {
        console.log("Fetched reviews:", data);
        setReviews(data);
      })
      .catch(error => console.error('Error fetching reviews:', error));
  }, [songId]);

  const handleSubmitReview = (e) => {
    e.preventDefault();
    
    // Get username from localStorage or use a test username for now
    const username = localStorage.getItem('username') || "testuser";

    fetch('http://127.0.0.1:5000/api/submit_review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        song_id: songId,
        rating: rating,
        review_text: reviewText
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Refresh reviews or add the new review to the list
        setReviews([...reviews, {
          reviewer_username: username,
          rating: rating,
          review: reviewText,
          created_at: new Date().toISOString()
        }]);
        
        // Reset form and close modal
        setRating(3);
        setReviewText('');
        setShowReviewModal(false);
      } else {
        alert(data.message);
      }
    })
    .catch(error => {
      console.error('Error submitting review:', error);
      alert('Failed to submit review');
    });
  };

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
  
  if (!songDetails) return <div className="page-container"><h2>No song data available</h2></div>;

  return (
    <div className="page-container">
      <h1>{songDetails.Title}</h1>
      <p>Artist: {songDetails.Artist_Name}</p>
      <p>Album: {songDetails.Album_Name}</p>

      <button 
        onClick={() => setShowReviewModal(true)}
        style={{
          backgroundColor: '#1DB954',
          color: 'white',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginBottom: '20px'
        }}
      >
        Add Review
      </button>

      {/* Review Modal */}
      {showReviewModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: '#282828',
            padding: '20px',
            borderRadius: '10px',
            width: '300px'
          }}>
            <h2>Add Review</h2>
            <form onSubmit={handleSubmitReview}>
              <div>
                <label>Rating:</label>
                <select 
                  value={rating} 
                  onChange={(e) => setRating(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '10px',
                    marginBottom: '10px'
                  }}
                >
                  {[1,2,3,4,5].map(num => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>
              <div>
                <label>Review:</label>
                <textarea 
                  value={reviewText}
                  onChange={(e) => setReviewText(e.target.value)}
                  required
                  style={{
                    width: '100%',
                    padding: '10px',
                    marginBottom: '10px',
                    minHeight: '100px'
                  }}
                />
              </div>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between'
              }}>
                <button 
                  type="submit"
                  style={{
                    backgroundColor: '#1DB954',
                    color: 'white',
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer'
                  }}
                >
                  Submit Review
                </button>
                <button 
                  type="button"
                  onClick={() => setShowReviewModal(false)}
                  style={{
                    backgroundColor: '#ff4136',
                    color: 'white',
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer'
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Reviews Section */}
      <h2>Reviews</h2>
      {reviews.length === 0 ? (
        <p>No reviews yet</p>
      ) : (
        <div>
          {reviews.map((review, index) => (
            <div 
              key={index} 
              style={{
                backgroundColor: '#282828',
                padding: '15px',
                marginBottom: '10px',
                borderRadius: '5px'
              }}
            >
              <p>
                <strong>{review.reviewer_username}</strong> 
                {' '}rated it {review.rating}/5
                {review.created_at && <span style={{color: '#999', fontSize: '0.8em'}}> • {new Date(review.created_at).toLocaleDateString()}</span>}
              </p>
              <p>{review.review}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SongDetails;