import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import {getGroups, addGroup, parseErrorResponse} from '../../services/api';
import AddGroup from './AddGroup';

const GroupsList = () => {
    const [groups, setGroups] = useState([]);
    const [showAddGroup, setShowAddGroup] = useState(false);
    const navigate = useNavigate();

    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

    useEffect(() => {
        fetchGroups();
    }, []);

    const fetchGroups = async () => {
        const response = await getGroups();
        setGroups(response.groups);
    };

    const handleAddGroup = async (groupName) => {
        try {
            await addGroup(groupName);
            setMessage(`Group "${groupName}" added successfully to ${groupName}!`);
            setMessageType('success');
        } catch (error) {
            setMessage(`Failed to add group "${groupName}". ${parseErrorResponse(error)}`);
            setMessageType('error');
        }
        fetchGroups();
        setShowAddGroup(false);
    };

    return (
        <div>
            <h1>Groups</h1>
            <button onClick={() => setShowAddGroup(true)}>Add Group</button>
            {showAddGroup && <AddGroup onAddGroup={handleAddGroup}/>}
            {message && <p className={`n-message ${messageType}`}>{message}</p>}

            <table>
                <thead>
                <tr>
                    <th>Group Name</th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {groups.map((group, index) => (
                    <tr className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                        <td>{group}</td>
                        <td>
                            <button onClick={() => navigate(`/groups/${group}/words`)}>View Words</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

        </div>
    );
};

export default GroupsList;
