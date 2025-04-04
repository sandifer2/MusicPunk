import { useState } from "react";
import { Link } from "react-router-dom"
import Table from "./Table";
import "../Home.css"; //  Import the CSS


function Home() {
    const [selectedCategory, setSelectedCategory] = useState("");

    return (
        <div className="home-container">
            <h1 className="home-title">Welcome to MusicBox!</h1>
            {/* <Link to="/">Home </Link>
            <Link to="/Page1">Page1 </Link> */}
            <p className="home-subtitle">Please select an option you would like to rate:</p>

            <div className="home-buttons">
                <button className="home-button" onClick={() => setSelectedCategory("Artists")}>Artists</button>
                <button className="home-button" onClick={() => setSelectedCategory("Songs")}>Songs</button>
                <button className="home-button" onClick={() => setSelectedCategory("Albums")}>Albums</button>
            </div>

            <Table selectedCategory={selectedCategory} />
        </div>
    );
}

export default Home;