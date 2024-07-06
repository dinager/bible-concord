import React, {useState} from 'react';

const AddGroup = ({onAddGroup}) => {
    const [groupName, setGroupName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onAddGroup(groupName);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={groupName}
                onChange={(e) => setGroupName(e.target.value)}
                placeholder="Enter group name"
                required
            />
            <button type="submit">Add Group</button>
        </form>
    );
};

export default AddGroup;
