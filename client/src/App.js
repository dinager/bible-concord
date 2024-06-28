import React from 'react';
import logo from './logo.jpg';
import './App.css';
import UploadBook from './UploadBook';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Bible Concord
        </p>
        <UploadBook/>
      </header>
    </div>
  );
}

export default App;
