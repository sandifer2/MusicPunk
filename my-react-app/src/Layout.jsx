import { Navbar } from "./Components/Navbar"
import { Outlet } from "react-router-dom"
import { useState, useEffect } from "react"
import "./CSS/Layout.css"
import tokenIcon from './images/token.png'

export function Layout() {
    const [tokenCount, setTokenCount] = useState(0)

    const fetchTokenCount = async () => {
        try {
            const username = localStorage.getItem('username');
            const response = await fetch(`http://127.0.0.1:5000/api/user/tokens?username=${username}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            setTokenCount(data.tokenCount);
        } catch (error) {
            console.error('Error fetching token count:', error);
        }
    };

    useEffect(() => {
        fetchTokenCount();
    }, []);

    return (
        <>
            <Navbar />
            <div className="token-display">
                <img src={tokenIcon} alt="Token" className="token-icon" />
                <span className="token-count">{tokenCount}</span>
            </div>
            <main>
                <Outlet context={{ refreshTokenCount: fetchTokenCount }} />
            </main>
        </>
    )
}