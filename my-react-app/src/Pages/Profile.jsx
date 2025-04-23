import React, { useState, useEffect } from "react";
import { useOutletContext, useNavigate } from "react-router-dom";
import '../CSS/ProfilePage.css';

export default function Profile() {
    const [songReviews, setSongReviews] = useState([]);
    const [albumReviews, setAlbumReviews] = useState([]);
    const [artistReviews, setArtistReviews] = useState([]);
    const [activeTab, setActiveTab] = useState("songs");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pinnedReviews, setPinnedReviews] = useState({
        songs: [],
        albums: [],
        artists: []
    });
    const [dataFetched, setDataFetched] = useState(false);
    const { refreshTokenCount } = useOutletContext();
    const navigate = useNavigate();
    const username = localStorage.getItem('username');

    useEffect(() => {
        // Only fetch data once
        if (!dataFetched) {
            fetchAllReviews();
            // Load pinned reviews from localStorage on component mount
            const savedPinnedReviews = localStorage.getItem(`pinnedReviews_${username}`);
            console.log("Loaded pinned reviews from localStorage:", savedPinnedReviews);
            
            if (savedPinnedReviews) {
                try {
                    const parsed = JSON.parse(savedPinnedReviews);
                    console.log("Parsed pinned reviews:", parsed);
                    
                    // Make sure we have all three arrays, even if the saved data doesn't
                    setPinnedReviews({
                        songs: Array.isArray(parsed.songs) ? parsed.songs : [],
                        albums: Array.isArray(parsed.albums) ? parsed.albums : [],
                        artists: Array.isArray(parsed.artists) ? parsed.artists : []
                    });
                } catch (e) {
                    console.error("Error parsing pinned reviews from localStorage:", e);
                    // Initialize with empty arrays if parse fails
                    setPinnedReviews({
                        songs: [],
                        albums: [],
                        artists: []
                    });
                    
                    // Reset localStorage to a valid initial state
                    localStorage.setItem(`pinnedReviews_${username}`, JSON.stringify({
                        songs: [],
                        albums: [],
                        artists: []
                    }));
                }
            } else {
                // Initialize localStorage if it doesn't exist
                localStorage.setItem(`pinnedReviews_${username}`, JSON.stringify({
                    songs: [],
                    albums: [],
                    artists: []
                }));
            }
            setDataFetched(true);
        }
    }, [dataFetched, username]);

    const fetchAllReviews = async () => {
        setLoading(true);
        try {
            if (!username) {
                throw new Error("User not logged in");
            }

            // Fetch song reviews
            const songResponse = await fetch(`http://127.0.0.1:5000/api/user/reviews?username=${username}`);
            if (!songResponse.ok) {
                throw new Error(`HTTP error! Status: ${songResponse.status}`);
            }
            const songData = await songResponse.json();
            setSongReviews(songData);

            // Fetch album reviews
            try {
                const albumResponse = await fetch(`http://127.0.0.1:5000/api/user/album_reviews?username=${username}`);
                if (albumResponse.ok) {
                    const albumData = await albumResponse.json();
                    setAlbumReviews(albumData);
                } else {
                    console.log("Album reviews endpoint not available or returned error");
                    setAlbumReviews(getMockAlbumReviews());
                }
            } catch (err) {
                console.log("Using mock album reviews data");
                setAlbumReviews(getMockAlbumReviews());
            }

            // Fetch artist reviews
            try {
                const artistResponse = await fetch(`http://127.0.0.1:5000/api/user/artist_reviews?username=${username}`);
                if (artistResponse.ok) {
                    const artistData = await artistResponse.json();
                    setArtistReviews(artistData);
                } else {
                    console.log("Artist reviews endpoint not available or returned error");
                    setArtistReviews(getMockArtistReviews());
                }
            } catch (err) {
                console.log("Using mock artist reviews data");
                setArtistReviews(getMockArtistReviews());
            }

            setLoading(false);
        } catch (err) {
            console.error("Error fetching user reviews:", err);
            setError(err.message);
            
            // Using mock data for testing in case the endpoint isn't ready
            setSongReviews(getMockSongReviews());
            setAlbumReviews(getMockAlbumReviews());
            setArtistReviews(getMockArtistReviews());
            setLoading(false);
        }
    };

    const getMockSongReviews = () => {
        return [
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
            }
        ];
    };

    const getMockAlbumReviews = () => {
        return [
            {
                review_id: 201,
                album_id: "1",
                album_name: "Dark Side of the Moon",
                artist_name: "Pink Floyd",
                rating: 5,
                review: "A perfect album from start to finish. Every song flows into the next creating a complete experience.",
                created_at: "2024-01-05T10:30:00Z"
            },
            {
                review_id: 202,
                album_id: "2",
                album_name: "Abbey Road",
                artist_name: "The Beatles",
                rating: 5,
                review: "The Beatles at their peak. The second side medley is one of the greatest achievements in music history.",
                created_at: "2024-02-20T16:45:00Z"
            },
            {
                review_id: 203,
                album_id: "3",
                album_name: "Rumours",
                artist_name: "Fleetwood Mac",
                rating: 4,
                review: "Amazing album born from personal turmoil. The harmonies and production are flawless.",
                created_at: "2024-03-15T14:25:00Z"
            }
        ];
    };

    const getMockArtistReviews = () => {
        return [
            {
                review_id: 301,
                artist_id: "1",
                artist_name: "David Bowie",
                rating: 5,
                review: "The ultimate musical chameleon. His ability to reinvent himself while maintaining quality is unmatched.",
                created_at: "2024-02-10T11:20:00Z"
            },
            {
                review_id: 302,
                artist_id: "2",
                artist_name: "Radiohead",
                rating: 5,
                review: "Constantly evolving and challenging themselves. From OK Computer to In Rainbows, they never disappoint.",
                created_at: "2024-01-25T15:30:00Z"
            },
            {
                review_id: 303,
                artist_id: "3",
                artist_name: "Kendrick Lamar",
                rating: 4,
                review: "One of the most important voices in modern music. His albums are cohesive artistic statements.",
                created_at: "2024-03-05T09:45:00Z"
            }
        ];
    };

    const handlePinReview = (reviewId, type) => {
        console.log(`Attempting to pin/unpin review ${reviewId} for type ${type}`);
        console.log("Current pinnedReviews state:", pinnedReviews);
        
        // Convert reviewId to a number if it's a string
        const idToPin = typeof reviewId === 'string' ? parseInt(reviewId, 10) : reviewId;
        
        // Create a deep copy of the current pinnedReviews state
        const updatedPinnedReviews = {
            songs: [...pinnedReviews.songs],
            albums: [...pinnedReviews.albums],
            artists: [...pinnedReviews.artists]
        };
        
        // Check if review is already pinned
        if (pinnedReviews[type].includes(idToPin)) {
            console.log(`Unpinning review ${idToPin} from ${type}`);
            // Unpin the review
            updatedPinnedReviews[type] = pinnedReviews[type].filter(id => id !== idToPin);
        } else {
            // Check if already have 3 pinned reviews of this type
            if (pinnedReviews[type].length >= 3) {
                alert(`You can only pin up to 3 ${type} reviews. Please unpin one first.`);
                return;
            }
            
            console.log(`Pinning review ${idToPin} to ${type}`);
            // Pin the review
            updatedPinnedReviews[type] = [...pinnedReviews[type], idToPin];
        }
        
        console.log("Updated pinnedReviews will be:", updatedPinnedReviews);
        
        // Update state and localStorage
        setPinnedReviews(updatedPinnedReviews);
        localStorage.setItem(`pinnedReviews_${username}`, JSON.stringify(updatedPinnedReviews));
    };

    const isPinned = (reviewId, type) => {
        // Convert to number for comparison if needed
        const idToCheck = typeof reviewId === 'string' ? parseInt(reviewId, 10) : reviewId;
        return pinnedReviews[type] && pinnedReviews[type].includes(idToCheck);
    };

    const navigateToDetails = (id, type) => {
        if (type === 'song') {
            navigate(`/song/${id}`);
        } else if (type === 'album') {
            navigate(`/album/${id}`);
        } else if (type === 'artist') {
            navigate(`/artist/${id}`);
        }
    };

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    // Sort reviews to show pinned ones first
    const getSortedReviews = (reviews, type) => {
        if (!reviews || !Array.isArray(reviews)) {
            return [];
        }
        
        return [...reviews].sort((a, b) => {
            const aIsPinned = isPinned(a.review_id, type);
            const bIsPinned = isPinned(b.review_id, type);
            
            if (aIsPinned && !bIsPinned) return -1;
            if (!aIsPinned && bIsPinned) return 1;
            
            // For pinned reviews, sort by the order they were pinned
            if (aIsPinned && bIsPinned && pinnedReviews[type]) {
                return pinnedReviews[type].indexOf(a.review_id) - pinnedReviews[type].indexOf(b.review_id);
            }
            
            // For unpinned reviews, sort by date (newest first)
            return new Date(b.created_at) - new Date(a.created_at);
        });
    };

    // Only compute these when needed based on the active tab
    let sortedReviews = [];
    if (activeTab === 'songs') {
        sortedReviews = getSortedReviews(songReviews, 'songs');
    } else if (activeTab === 'albums') {
        sortedReviews = getSortedReviews(albumReviews, 'albums');
    } else if (activeTab === 'artists') {
        sortedReviews = getSortedReviews(artistReviews, 'artists');
    }

    return (
        <div className="profile-container">
            <div className="username-display">
                Welcome, {username}!
            </div>
            <h1>My Profile</h1>
            
            <div className="profile-content">
                <div className="review-tabs">
                    <button 
                        className={`tab-button ${activeTab === 'songs' ? 'active' : ''}`}
                        onClick={() => setActiveTab('songs')}
                    >
                        Songs ({songReviews.length})
                    </button>
                    <button 
                        className={`tab-button ${activeTab === 'albums' ? 'active' : ''}`}
                        onClick={() => setActiveTab('albums')}
                    >
                        Albums ({albumReviews.length})
                    </button>
                    <button 
                        className={`tab-button ${activeTab === 'artists' ? 'active' : ''}`}
                        onClick={() => setActiveTab('artists')}
                    >
                        Artists ({artistReviews.length})
                    </button>
                </div>
                
                <div className="profile-section">
                    {activeTab === 'songs' && (
                        <>
                            <h2>My Song Reviews</h2>
                            <p className="review-info">You can pin up to 3 song reviews to highlight your favorites</p>
                            
                            {loading ? (
                                <div className="loading-spinner">Loading...</div>
                            ) : error ? (
                                <div className="error-message">
                                    <p>Error loading reviews: {error}</p>
                                    <button onClick={() => { setDataFetched(false); }} className="retry-button">Try Again</button>
                                </div>
                            ) : sortedReviews.length === 0 ? (
                                <div className="no-reviews">
                                    <p>You haven't written any song reviews yet.</p>
                                    <button onClick={() => navigate('/home')} className="action-button">
                                        Find Songs to Review
                                    </button>
                                </div>
                            ) : (
                                <div className="reviews-list">
                                    {sortedReviews.map((review) => (
                                        <div 
                                            key={review.review_id} 
                                            className={`review-card ${isPinned(review.review_id, 'songs') ? 'pinned' : ''}`}
                                        >
                                            {isPinned(review.review_id, 'songs') && (
                                                <div className="pinned-badge">
                                                    <span className="pin-icon">📌</span>
                                                    <span>Pinned</span>
                                                </div>
                                            )}
                                            <div className="review-header">
                                                <h3 
                                                    className="song-title" 
                                                    onClick={() => navigateToDetails(review.song_id, 'song')}
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
                                                    className={`pin-button ${isPinned(review.review_id, 'songs') ? 'pinned' : ''}`}
                                                    onClick={() => handlePinReview(review.review_id, 'songs')}
                                                >
                                                    {isPinned(review.review_id, 'songs') ? 'Unpin' : 'Pin'}
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </>
                    )}

                    {activeTab === 'albums' && (
                        <>
                            <h2>My Album Reviews</h2>
                            <p className="review-info">You can pin up to 3 album reviews to highlight your favorites</p>
                            
                            {loading ? (
                                <div className="loading-spinner">Loading...</div>
                            ) : error ? (
                                <div className="error-message">
                                    <p>Error loading reviews: {error}</p>
                                    <button onClick={() => { setDataFetched(false); }} className="retry-button">Try Again</button>
                                </div>
                            ) : sortedReviews.length === 0 ? (
                                <div className="no-reviews">
                                    <p>You haven't written any album reviews yet.</p>
                                    <button onClick={() => navigate('/home')} className="action-button">
                                        Find Albums to Review
                                    </button>
                                </div>
                            ) : (
                                <div className="reviews-list">
                                    {sortedReviews.map((review) => (
                                        <div 
                                            key={review.review_id} 
                                            className={`review-card ${isPinned(review.review_id, 'albums') ? 'pinned' : ''}`}
                                        >
                                            {isPinned(review.review_id, 'albums') && (
                                                <div className="pinned-badge">
                                                    <span className="pin-icon">📌</span>
                                                    <span>Pinned</span>
                                                </div>
                                            )}
                                            <div className="review-header">
                                                <h3 
                                                    className="song-title" 
                                                    onClick={() => navigateToDetails(review.album_id, 'album')}
                                                    style={{ cursor: 'pointer' }}
                                                >
                                                    {review.album_name}
                                                </h3>
                                                <p className="artist">by {review.artist_name}</p>
                                                <div className="rating">
                                                    Rating: {review.rating}/5
                                                </div>
                                            </div>
                                            <p className="review-text">{review.review}</p>
                                            <div className="review-footer">
                                                <span className="review-date">{formatDate(review.created_at)}</span>
                                                <button 
                                                    className={`pin-button ${isPinned(review.review_id, 'albums') ? 'pinned' : ''}`}
                                                    onClick={() => handlePinReview(review.review_id, 'albums')}
                                                >
                                                    {isPinned(review.review_id, 'albums') ? 'Unpin' : 'Pin'}
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </>
                    )}

                    {activeTab === 'artists' && (
                        <>
                            <h2>My Artist Reviews</h2>
                            <p className="review-info">You can pin up to 3 artist reviews to highlight your favorites</p>
                            
                            {loading ? (
                                <div className="loading-spinner">Loading...</div>
                            ) : error ? (
                                <div className="error-message">
                                    <p>Error loading reviews: {error}</p>
                                    <button onClick={() => { setDataFetched(false); }} className="retry-button">Try Again</button>
                                </div>
                            ) : sortedReviews.length === 0 ? (
                                <div className="no-reviews">
                                    <p>You haven't written any artist reviews yet.</p>
                                    <button onClick={() => navigate('/home')} className="action-button">
                                        Find Artists to Review
                                    </button>
                                </div>
                            ) : (
                                <div className="reviews-list">
                                    {sortedReviews.map((review) => (
                                        <div 
                                            key={review.review_id} 
                                            className={`review-card ${isPinned(review.review_id, 'artists') ? 'pinned' : ''}`}
                                        >
                                            {isPinned(review.review_id, 'artists') && (
                                                <div className="pinned-badge">
                                                    <span className="pin-icon">📌</span>
                                                    <span>Pinned</span>
                                                </div>
                                            )}
                                            <div className="review-header">
                                                <h3 
                                                    className="song-title" 
                                                    onClick={() => navigateToDetails(review.artist_id, 'artist')}
                                                    style={{ cursor: 'pointer' }}
                                                >
                                                    {review.artist_name}
                                                </h3>
                                                <div className="rating">
                                                    Rating: {review.rating}/5
                                                </div>
                                            </div>
                                            <p className="review-text">{review.review}</p>
                                            <div className="review-footer">
                                                <span className="review-date">{formatDate(review.created_at)}</span>
                                                <button 
                                                    className={`pin-button ${isPinned(review.review_id, 'artists') ? 'pinned' : ''}`}
                                                    onClick={() => handlePinReview(review.review_id, 'artists')}
                                                >
                                                    {isPinned(review.review_id, 'artists') ? 'Unpin' : 'Pin'}
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}