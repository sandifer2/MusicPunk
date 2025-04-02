import { Link } from "react-router-dom";

export function Navbar() {
    return (
        <>
            <Link to="/">
                <button>Home</button>
            </Link>
            <Link to="/Page1">
                <button>Page1</button>
            </Link>
        </>
    );
}
