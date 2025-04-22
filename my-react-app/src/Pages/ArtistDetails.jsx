import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../CSS/Page.css';

function ArtistDetails() {
  const { artistId } = useParams();
  const [artistDetails, setArtistDetails] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [rating, setRating] = useState(3);
  const [reviewText, setReviewText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

    // Fetch artist reviews
    fetch(`http://127.0.0.1:5000/api/artist_reviews/${artistId}`)
      .then(response => response.json())
      .then(data => {
        setReviews(data);
      })
      .catch(error => console.error('Error fetching reviews:', error));
  }, [artistId]);

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
  
  if (!artistDetails) return <div className="page-container"><h2>No artist data available</h2></div>;

  return (
    <div className="page-container">
      <h1>{artistDetails.Artist_Name}</h1>

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
                  onChange={(e) => setRating(Number(e.target.value))}
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
                justifyContent: 'space-between',
                marginTop: '20px'
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
                  Submit
                </button>
                <button 
                  type="button"
                  onClick={() => setShowReviewModal(false)}
                  style={{
                    backgroundColor: '#282828',
                    color: 'white',
                    padding: '10px 20px',
                    border: '1px solid white',
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

      {/* Reviews List */}
      <div style={{ marginTop: '20px' }}>
        <h2>Reviews</h2>
        {reviews.length > 0 ? (
          reviews.map((review, index) => (
            <div 
              key={index}
              style={{
                backgroundColor: '#282828',
                padding: '15px',
                marginBottom: '10px',
                borderRadius: '5px'
              }}
            >
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '10px'
              }}>
                <span style={{ fontWeight: 'bold' }}>{review.reviewer_username}</span>
                <span>Rating: {review.rating}/5</span>
                <span>{new Date(review.created_at).toLocaleDateString()}</span>
              </div>
              <p style={{ margin: 0 }}>{review.review}</p>
            </div>
          ))
        ) : (
          <p>No reviews yet. Be the first to review!</p>
        )}
      </div>
    </div>
  );
}

export default ArtistDetails; 