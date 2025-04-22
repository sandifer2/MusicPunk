// import { Link } from "react-router-dom";
// import '../CSS/ProfilePage.css'

// export default function Profile(){
//     return(
//         <div className = "profile-container">
//             <h1>This is the profile page</h1>    
//         </div>
//     );
// }

import React, { useState, useEffect } from "react";
import { useOutletContext, useNavigate } from "react-router-dom";
import '../CSS/ProfilePage.css';

export default function Profile() {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pinnedReviews, setPinnedReviews] = useState([]);
    const { refreshTokenCount } = useOutletContext();
    const navigate = useNavigate();
    const username = localStorage.getItem('username');

    useEffect(() => {
        fetchUserReviews();
        // Load pinned reviews from localStorage on component mount
        const savedPinnedReviews = localStorage.getItem(`pinnedReviews_${username}`);
        if (savedPinnedReviews) {
            setPinnedReviews(JSON.parse(savedPinnedReviews));
        }
    }, []);

    const fetchUserReviews = async () => {
        setLoading(true);
        try {
            const username = localStorage.getItem('username');
            if (!username) {
                throw new Error("User not logged in");
            }

            const response = await fetch(`http://127.0.0.1:5000/api/user/reviews?username=${username}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            setReviews(data);
            setLoading(false);
        } catch (err) {
            console.error("Error fetching user reviews:", err);
            setError(err.message);
            
            // Using mock data for testing in case the endpoint isn't ready
            const username = localStorage.getItem('username') || 'testuser';
            const mockReviews = [
                {
                    review_id: 101,
                    song_id: "spotify:track:1",
                    song_title: "Bohemian Rhapsody",
                    artist_name: "Queen",
                    album_name: "A Night at the Opera",
                    rating: 5,
                    review: "A masterpiece that never gets old. The composition and vocal range are incredible.",
                    created_at: "2024-02-15T14:30:00Z"
                },
                {
                    review_id: 102,
                    song_id: "spotify:track:2",
                    song_title: "Billie Jean",
                    artist_name: "Michael Jackson",
                    album_name: "Thriller",
                    rating: 4,
                    review: "Classic pop track with an iconic bassline. Michael's vocals are perfect.",
                    created_at: "2024-03-10T09:15:00Z"
                },
                {
                    review_id: 103,
                    song_id: "spotify:track:3",
                    song_title: "Stairway to Heaven",
                    artist_name: "Led Zeppelin",
                    album_name: "Led Zeppelin IV",
                    rating: 5,
                    review: "Probably the greatest rock song ever written. A journey from start to finish.",
                    created_at: "2024-01-20T18:45:00Z"
                },
                {
                    review_id: 104,
                    song_id: "spotify:track:4",
                    song_title: "Purple Haze",
                    artist_name: "Jimi Hendrix",
                    album_name: "Are You Experienced",
                    rating: 4,
                    review: "Groundbreaking guitar work. Hendrix was truly ahead of his time.",
                    created_at: "2024-03-25T11:20:00Z"
                },
                {
                    review_id: 105,
                    song_id: "spotify:track:5",
                    song_title: "Imagine",
                    artist_name: "John Lennon",
                    album_name: "Imagine",
                    rating: 5,
                    review: "A timeless message of peace and unity. Lennon's best solo work.",
                    created_at: "2024-02-28T16:10:00Z"
                }
            ];
            setReviews(mockReviews);
            setLoading(false);
        }
    };

    const handlePinReview = (reviewId) => {
        // Check if review is already pinned
        if (pinnedReviews.includes(reviewId)) {
            // Unpin the review
            const updatedPinnedReviews = pinnedReviews.filter(id => id !== reviewId);
            setPinnedReviews(updatedPinnedReviews);
            const username = localStorage.getItem('username');
            localStorage.setItem(`pinnedReviews_${username}`, JSON.stringify(updatedPinnedReviews));
        } else {
            // Check if already have 3 pinned reviews
            if (pinnedReviews.length >= 3) {
                alert("You can only pin up to 3 reviews. Please unpin one first.");
                return;
            }
            
            // Pin the review
            const updatedPinnedReviews = [...pinnedReviews, reviewId];
            setPinnedReviews(updatedPinnedReviews);
            const username = localStorage.getItem('username');
            localStorage.setItem(`pinnedReviews_${username}`, JSON.stringify(updatedPinnedReviews));
        }
    };

    // Sort reviews to show pinned ones first
    const sortedReviews = [...reviews].sort((a, b) => {
        const aIsPinned = pinnedReviews.includes(a.review_id);
        const bIsPinned = pinnedReviews.includes(b.review_id);
        
        if (aIsPinned && !bIsPinned) return -1;
        if (!aIsPinned && bIsPinned) return 1;
        
        // For pinned reviews, sort by the order they were pinned
        if (aIsPinned && bIsPinned) {
            return pinnedReviews.indexOf(a.review_id) - pinnedReviews.indexOf(b.review_id);
        }
        
        // For unpinned reviews, sort by date (newest first)
        return new Date(b.created_at) - new Date(a.created_at);
    });

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return (
        <div className="profile-container">
            <div className="username-display">
                Welcome, {username}!
            </div>
            <h1>My Profile</h1>
            
            <div className="profile-content">
                <div className="profile-section">
                    <h2>My Reviews</h2>
                    <p className="review-info">You can pin up to 3 reviews to highlight your favorites</p>
                    
                    {loading ? (
                        <div className="loading-spinner">Loading...</div>
                    ) : error ? (
                        <div className="error-message">
                            <p>Error loading reviews: {error}</p>
                            <button onClick={fetchUserReviews} className="retry-button">Try Again</button>
                        </div>
                    ) : reviews.length === 0 ? (
                        <div className="no-reviews">
                            <p>You haven't written any reviews yet.</p>
                            <button onClick={() => window.location.href = '/home'} className="action-button">
                                Find Songs to Review
                            </button>
                        </div>
                    ) : (
                        <div className="reviews-list">
                            {sortedReviews.map((review) => (
                                <div 
                                    key={review.review_id} 
                                    className={`review-card ${pinnedReviews.includes(review.review_id) ? 'pinned' : ''}`}
                                >
                                    {pinnedReviews.includes(review.review_id) && (
                                        <div className="pinned-badge">
                                            <span className="pin-icon">📌</span>
                                            <span>Pinned</span>
                                        </div>
                                    )}
                                    <div className="review-header">
                                        <h3 
                                            className="song-title" 
                                            onClick={() => navigate(`/song/${review.song_id}`)}
                                            style={{ cursor: 'pointer' }}
                                        >
                                            {review.song_title}
                                        </h3>
                                        <p className="artist">by {review.artist_name}</p>
                                        <p className="album">{review.album_name}</p>
                                        <div className="rating">
                                            Rating: {review.rating}/5
                                        </div>
                                    </div>
                                    <p className="review-text">{review.review}</p>
                                    <div className="review-footer">
                                        <span className="review-date">{formatDate(review.created_at)}</span>
                                        <button 
                                            className={`pin-button ${pinnedReviews.includes(review.review_id) ? 'pinned' : ''}`}
                                            onClick={() => handlePinReview(review.review_id)}
                                        >
                                            {pinnedReviews.includes(review.review_id) ? 'Unpin' : 'Pin'}
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}