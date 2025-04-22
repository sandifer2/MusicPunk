import React, { useState, useEffect } from 'react';
import { useParams, useOutletContext } from 'react-router-dom';
import '../CSS/Page.css';
import '../CSS/SongDetails.css';

function ArtistDetails() {
  const { artistId } = useParams();
  const { refreshTokenCount } = useOutletContext();
  const [artistDetails, setArtistDetails] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [rating, setRating] = useState(3);
  const [reviewText, setReviewText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviewedArtist, setReviewedArtist] = useState(null);
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [tokensAvailable, setTokensAvailable] = useState(0);
  const [unlockCost] = useState(5);

  useEffect(() => {
    if (!artistId) {
      setError("Artist ID is missing");
      setLoading(false);
      return;
    }

    // Fetch artist details
    fetch(`http://127.0.0.1:5000/api/artist/${artistId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setArtistDetails(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching artist details:', error);
        setError(`Failed to load artist details: ${error.message}`);
        setLoading(false);
      });

    // First check if user has already reviewed this artist
    const username = localStorage.getItem('username');
    fetch(`http://127.0.0.1:5000/api/artist_reviews/${artistId}`)
      .then(response => response.json())
      .then(data => {
        setReviews(data);
        // Check if the current user has reviewed this artist
        const userReview = data.find(review => review.reviewer_username === username);
        if (userReview) {
          setReviewedArtist(1);
          setIsUnlocked(true); // If user has reviewed, they should be able to see the reviews
        } else {
          setReviewedArtist(0);
        }
      })
      .catch(error => console.error('Error fetching reviews:', error));

    // Then check unlock status
    fetch(`http://127.0.0.1:5000/api/check_artist_unlock/${artistId}?username=${username}`)
      .then(response => response.json())
      .then(data => {
        // Only update isUnlocked if user hasn't reviewed yet
        if (reviewedArtist === 0) {
          setIsUnlocked(data.is_unlocked);
        }
        setTokensAvailable(data.tokens_available);
      })
      .catch(error => console.error('Error checking unlock status:', error));
  }, [artistId]);

  const handleUnlockArtist = () => {
    const username = localStorage.getItem("username");
    fetch('http://127.0.0.1:5000/api/unlock_artist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, artist_id: artistId })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setIsUnlocked(true);
          setTokensAvailable(data.tokens_remaining);
          refreshTokenCount();
          fetchReviews(); // Fetch reviews after unlocking
          alert("Artist unlocked successfully!");
        } else {
          alert(data.error || "Failed to unlock artist.");
        }
      })
      .catch(error => {
        console.error("Unlock error:", error);
        alert("Something went wrong.");
      });
  };

  const fetchReviews = () => {
    fetch(`http://127.0.0.1:5000/api/artist_reviews/${artistId}`)
      .then(response => response.json())
      .then(data => setReviews(data))
      .catch(error => console.error('Error fetching reviews:', error));
  };

  const handleSubmitReview = (e) => {
    e.preventDefault();
    const username = localStorage.getItem('username');
    if (!username) {
      alert('Please log in to submit a review');
      return;
    }

    fetch('http://127.0.0.1:5000/api/submit_artist_review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        artist_id: artistId,
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

        // Update reviewedArtist state to indicate user has reviewed
        setReviewedArtist(1);

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
  
  if (!artistDetails) return <div className="page-container"><h2>No artist data available</h2></div>;

  return (
    <div className="song-details-container">
      <h1 className="song-details-title">{artistDetails.Artist_Name}</h1>
      <div className="song-details-info">
        {isUnlocked && (
          <div className="rating-summary">
            <p className="average-rating">
              Average Rating: <strong>{calculateAverageRating()}</strong>/5
              <span className="review-count">({reviews.length} {reviews.length === 1 ? 'review' : 'reviews'})</span>
            </p>
          </div>
        )}
        {isUnlocked && reviewedArtist === 0 && (
          <p className="token-incentive">Add a review to earn 10 tokens!</p>
        )}
      </div>
      {isUnlocked ? (
        <>
          {reviewedArtist === 0 && (
            <button className="add-review-button" onClick={() => setShowReviewModal(true)}>
              Add Review
            </button>
          )}
          {/* Reviews Section - Only shown when unlocked */}
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
          <p>You must unlock this artist to view and leave reviews.</p>
          <p>You have <strong>{tokensAvailable}</strong> tokens.</p>
          <p>Cost to unlock: <strong>{unlockCost}</strong> tokens</p>
          <button className="add-review-button" onClick={handleUnlockArtist}>
            Unlock Artist
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

export default ArtistDetails; 