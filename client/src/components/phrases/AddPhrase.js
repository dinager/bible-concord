import React, {useState} from 'react';

const AddPhrase = ({onAddPhrase}) => {
    const [phraseName, setPhraseName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onAddPhrase(phraseName);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={phraseName}
                onChange={(e) => setPhraseName(e.target.value)}
                placeholder="Enter phrase name"
                required
            />
            <button type="submit">Add phrase</button>
        </form>
    );
};

export default AddPhrase;
