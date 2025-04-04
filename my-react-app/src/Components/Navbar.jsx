import { Link } from "react-router-dom";
import '../CSS/NavBar.css'



export function Navbar() {
    return (
        <div className="nav-container">
            <Link to="/">
                <button className="NavBarButtons">Home</button>
            </Link>
            <Link to="/Page1">
                <button className="NavBarButtons">Page 1</button>
            </Link>

            <Link to="/Page2">
                <button className="NavBarButtons">Page 2</button>
            </Link>
            <Link to="/Profile">
                <button className="NavBarButtons">Profile</button>
            </Link>
        </div>
    );
}
