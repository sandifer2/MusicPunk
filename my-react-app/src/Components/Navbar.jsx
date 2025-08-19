import { Link } from "react-router-dom";
import '../CSS/NavBar.css'

export function Navbar() {
    return (
        <div className="nav-container">
            <div className="nav-header">
                <div className="nav-logo">MX</div>
                <div className="nav-status">ONLINE</div>
            </div>
            
            <div className="nav-links">
                <Link to="/home" className="nav-link">
                    <span className="nav-icon">⟨/⟩</span>
                    <span className="nav-text">HOME</span>
                    <span className="nav-line"></span>
                </Link>
                
                <Link to="/Profile" className="nav-link">
                    <span className="nav-icon">◈</span>
                    <span className="nav-text">PROFILE</span>
                    <span className="nav-line"></span>
                </Link>
                
                <Link to="/top-rated-albums" className="nav-link">
                    <span className="nav-icon">▲</span>
                    <span className="nav-text">TOP_RATED</span>
                    <span className="nav-line"></span>
                </Link>
            </div>
            
            <Link to="/" className="nav-link logout">
                <span className="nav-icon">⬡</span>
                <span className="nav-text">LOGOUT</span>
                <span className="nav-line"></span>
            </Link>
        </div>
    );
}