import { Link } from "react-router-dom";
import '../CSS/NavBar.css'



export function Navbar() {
    return (
        <div className="nav-container">
            <Link to="/home">
                <button className="NavBarButtons">🏠</button>
            </Link>
            <Link to="/SongReview">
                <button className="NavBarButtons">Review a Song</button>
            </Link>

            <Link to="/Page2">
                <button className="NavBarButtons">Page 2</button>
            </Link>
            <Link to="/Profile">
                <button className="NavBarButtons">👤</button>
            </Link>
            <Link to="/">
                <button className="NavBarButtons">Back to login</button>
            </Link>
            <Link to="/top-rated-albums">
                <button className="NavBarButtons">Top Rated Albums</button>
            </Link>
        </div>
    );
}
