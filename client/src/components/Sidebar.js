import React from 'react';
import {Link} from 'react-router-dom';

const Sidebar = () => {
    return (
        <div className="sidebar">
            <h2>Library</h2>
            <ul>
                <li>
                    <Link to="/">Home</Link>
                </li>
                <li>
                    <Link to="/books">Books
                    </Link>
                </li>
                <li>
                    <Link to="/search-words">Search Words</Link>
                </li>
                <li>
                    <Link to="/statistics">Statistics</Link>
                </li>
            </ul>
        </div>
    );
};

export default Sidebar;
