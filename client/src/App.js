import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './components/Home';
import AddBook from './components/AddBook';
import Books from './components/Books';
import BookDetail from './components/BookDetail';
import WordList from './components/WordList';
import WordAppearances from './components/WordAppearances';

import './index.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Sidebar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/books" element={<Books />} />
            <Route path="/add-book" element={<AddBook />} />
            <Route path="/book/:name" element={<BookDetail />} />
            <Route path="/search-words" element={<WordList />} />
            <Route path="/word/:word/appearances" element={<WordAppearances />} />
            <Route path="/statistics" element={<div>Statistics Page</div>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
