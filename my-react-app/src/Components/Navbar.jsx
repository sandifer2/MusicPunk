import { Link } from "react-router-dom";
import '../CSS/NavBar.css'

export function Navbar() {
    return (
        <div className="nav-container">
            <Link to="/home">
                <button className="NavBarButtons">🏠</button>
            </Link>
            <Link to="/Profile">
                <button className="NavBarButtons">👤</button>
            </Link>
            <Link to="/top-rated-albums">
                <button className="NavBarButtons">Top Rated Albums</button>
            </Link>
            <Link to="/">
                <button className="NavBarButtons">Logout</button>
            </Link>
        </div>
    );
}
