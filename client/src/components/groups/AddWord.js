import React, {useState} from 'react';

const AddWord = ({onAddWord}) => {
    const [word, setWord] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onAddWord(word);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={word}
                onChange={(e) => setWord(e.target.value)}
                placeholder="Enter word"
                required
            />
            <button type="submit">Add Word</button>
        </form>
    );
};

export default AddWord;
