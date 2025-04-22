import React, { useState, useEffect } from 'react';
import { useParams, useOutletContext } from 'react-router-dom';
import '../CSS/Page.css';
import '../CSS/SongDetails.css';

function AlbumDetails() {
  const { albumId } = useParams();
  const { refreshTokenCount } = useOutletContext();
  console.log("AlbumDetails component mounted");
  console.log("Album ID from URL params:", albumId);

  const [albumDetails, setAlbumDetails] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [rating, setRating] = useState(3);
  const [reviewText, setReviewText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviewedAlbum, setReviewedAlbum] = useState(null);
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [tokensAvailable, setTokensAvailable] = useState(0);
  const [unlockCost] = useState(5);

  // Fetch album details and reviews when component mounts
  useEffect(() => {
    if (!albumId) {
      setError("Album ID is missing");
      setLoading(false);
      return;
    }

    console.log("Making API request to:", `http://127.0.0.1:5000/api/album/${albumId}`);
    
    // Fetch album details
    fetch(`http://127.0.0.1:5000/api/album/${albumId}`)
      .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
          return response.json().then(errorData => {
            console.error("Error data:", errorData);
            throw new Error(`Status: ${response.status}, Message: ${errorData.error || 'Unknown error'}`);
          }).catch(err => {
            throw new Error(`Status: ${response.status}`);
          });
        }
        return response.json();
      })
      .then(data => {
        console.log("Fetched album details:", data);
        setAlbumDetails(data);
        setLoading(false);
      })  
      .catch(error => {
        console.error('Error fetching album details:', error);
        setError(`Failed to load album details: ${error.message}`);
        setLoading(false);
      });

    // First check if user has already reviewed this album
    const username = localStorage.getItem('username');
    fetch(`http://127.0.0.1:5000/api/album_reviews/${albumId}`)
      .then(response => response.json())
      .then(data => {
        console.log("Fetched reviews:", data);
        setReviews(data);
        // Check if the current user has reviewed this album
        const userReview = data.find(review => review.reviewer_username === username);
        if (userReview) {
          setReviewedAlbum(1);
          setIsUnlocked(true);
        } else {
          setReviewedAlbum(0);
        }
      })
      .catch(error => console.error('Error fetching reviews:', error));

    // Then check unlock status
    fetch(`http://127.0.0.1:5000/api/check_album_unlock/${albumId}?username=${username}`)
      .then(response => response.json())
      .then(data => {
        // Only update isUnlocked if user hasn't reviewed yet
        if (reviewedAlbum === 0) {
          setIsUnlocked(data.is_unlocked);
        }
        setTokensAvailable(data.tokens_available);
      })
      .catch(error => console.error('Error checking unlock status:', error));
  }, [albumId]);

  const handleSubmitReview = (e) => {
    e.preventDefault();
    
    // Get username from localStorage or use a test username for now
    const username = localStorage.getItem('username') || "testuser";

    fetch('http://127.0.0.1:5000/api/submit_album_review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        album_id: albumId,
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

        // Update reviewedAlbum state to indicate user has reviewed
        setReviewedAlbum(1);

        // Refresh token count in the top right
        refreshTokenCount();

        // Show success message with token reward
        alert(`Review submitted successfully! You earned ${data.tokens_earned} tokens! Your new balance is ${data.new_token_balance} tokens.`);
      } else {
        alert(data.message);
      }
    })
    .catch(error => {
      console.error('Error submitting review:', error);
      alert('Failed to submit review');
    });
  };

  const calculateAverageRating = () => {
    if (reviews.length === 0) return 0;
    const sum = reviews.reduce((total, review) => total + review.rating, 0);
    return (sum / reviews.length).toFixed(1);
  };

  const handleUnlockAlbum = () => {
    const username = localStorage.getItem("username");
    fetch('http://127.0.0.1:5000/api/unlock_album', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, album_id: albumId })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setIsUnlocked(true);
          setTokensAvailable(data.tokens_remaining);
          refreshTokenCount();
          fetchReviews(); // Fetch reviews after unlocking
          alert("Album unlocked successfully!");
        } else {
          alert(data.error || "Failed to unlock album.");
        }
      })
      .catch(error => {
        console.error("Unlock error:", error);
        alert("Something went wrong.");
      });
  };

  const fetchReviews = () => {
    fetch(`http://127.0.0.1:5000/api/album_reviews/${albumId}`)
      .then(response => response.json())
      .then(data => setReviews(data))
      .catch(error => console.error('Error fetching reviews:', error));
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
  
  if (!albumDetails) return <div className="page-container"><h2>No album data available</h2></div>;

  return (
    <div className="song-details-container">
      <h1 className="song-details-title">{albumDetails.Album_Name}</h1>
      <div className="song-details-info">
        <p>Artist: {albumDetails.Artist_Name}</p>
        {isUnlocked && (
          <div className="rating-summary">
            <p className="average-rating">
              Average Rating: <strong>{calculateAverageRating()}</strong>/5
              <span className="review-count">({reviews.length} {reviews.length === 1 ? 'review' : 'reviews'})</span>
            </p>
          </div>
        )}
        {isUnlocked && reviewedAlbum === 0 && (
          <p className="token-incentive">Add a review to earn 10 tokens!</p>
        )}
      </div>

      {isUnlocked ? (
        <>
          {reviewedAlbum === 0 && (
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
          )}
          {/* Reviews Section */}
          <div className="reviews-section">
            <h2>Reviews</h2>
            {reviews.length === 0 ? (
              <p>No reviews yet</p>
            ) : (
              <div>
                {reviews.map((review, index) => (
                  <div key={index} className="review-card">
                    <div className="review-header">
                      <strong>{review.reviewer_username}</strong>
                      {' '}rated it {review.rating}/5
                      {review.created_at && (
                        <span className="review-date">
                          • {new Date(review.created_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    <p className="review-content">{review.review}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      ) : (
        <div className="unlock-section">
          <p>You must unlock this album to view and leave reviews.</p>
          <p>You have <strong>{tokensAvailable}</strong> tokens.</p>
          <p>Cost to unlock: <strong>{unlockCost}</strong> tokens</p>
          <button className="add-review-button" onClick={handleUnlockAlbum}>
            Unlock Album
          </button>
        </div>
      )}

      {/* Review Modal */}
      {showReviewModal && (
        <div className="review-modal-overlay">
          <div className="review-modal">
            <h2>Add Review</h2>
            <form onSubmit={handleSubmitReview}>
              <div className="review-form-group">
                <label>Rating:</label>
                <select 
                  value={rating} 
                  onChange={(e) => setRating(Number(e.target.value))}
                >
                  {[1,2,3,4,5].map(num => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>
              <div className="review-form-group">
                <label>Review:</label>
                <textarea 
                  value={reviewText}
                  onChange={(e) => setReviewText(e.target.value)}
                  required
                />
              </div>
              <div className="review-form-buttons">
                <button type="submit" className="submit-review-button">
                  Submit
                </button>
                <button 
                  type="button" 
                  className="cancel-review-button"
                  onClick={() => setShowReviewModal(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default AlbumDetails; 