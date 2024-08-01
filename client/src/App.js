import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './components/Home';
import AddBook from './components/AddBook';
import Books from './components/Books';
import BookDetail from './components/BookDetail';
import WordList from './components/search/WordList';
import WordAppearances from './components/search/WordAppearances';
import GroupsList from './components/groups/GroupsList';
import GroupWords from './components/groups/GroupWords';
import AddFromWordList from './components/groups/AddFromWordList';
import PhrasesList from './components/phrases/PhrasesList';
import PhraseDetail from './components/phrases/PhraseDetail';
import PhraseContext from './components/phrases/PhraseContext';
import AddPhraseFromText from './components/phrases/AddPhraseFromText';


import './index.css';

function App() {
    return (
        <Router>
            <div className="App">
                <Sidebar/>
                <div className="content">
                    <Routes>
                        <Route path="/" element={<Home/>}/>
                        <Route path="/books" element={<Books/>}/>
                        <Route path="/add-book" element={<AddBook/>}/>
                        <Route path="/book/:name" element={<BookDetail/>}/>
                        <Route path="/search-words" element={<WordList/>}/>
                        <Route path="/search-words/:groupName" element={<WordList/>}/>
                        <Route path="/word/:word/appearances" element={<WordAppearances/>}/>
                        <Route path="/word/:word/appearances/group/:groupName" element={<WordAppearances/>}/>
                        <Route path="/groups" element={<GroupsList/>}/>
                        <Route path="/groups/:groupName/words" element={<GroupWords/>}/>
                        <Route path="/groups/:groupName/add-word-from-list" element={<AddFromWordList/>}/>
                        <Route path="/statistics" element={<div>Statistics Page</div>}/>
                        <Route path="/phrases" element={<PhrasesList/>}/>
                        <Route path="/phrase/:phraseText/context" element={<PhraseDetail/>}/>
                        <Route path="/phrase/:phraseText/book/:book_title/chapter_num/:chapter_num/verse_num/:verse_num/word_position/:word_position" element={<PhraseContext/>}/>
                        <Route path="/add-phrase-from-text" element={<AddPhraseFromText />} />
                        <Route path="/book-to-delete/:name" element={<Books />} />

                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;
