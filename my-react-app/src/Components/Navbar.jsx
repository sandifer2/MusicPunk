import { Link } from "react-router-dom";
import '../CSS/NavBar.css'



export function Navbar() {
    return (
        <div className="nav-container">
            <Link to="/home">
                <button className="NavBarButtons">🏠</button>
            </Link>
            <Link to="/Page1">
                <button className="NavBarButtons">Page 1</button>
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
        </div>
    );
}
