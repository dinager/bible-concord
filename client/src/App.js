import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './components/Home';
import AddBook from './components/AddBook';

// import './App.css';
import './index.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Sidebar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/add-book" element={<AddBook />} />
            <Route path="/statistics" element={<div>Statistics Page</div>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
