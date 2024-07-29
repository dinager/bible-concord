import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getGroups, addGroup, deleteGroup, parseErrorResponse } from '../../services/api'; // Make sure deleteGroup is imported
import AddGroup from './AddGroup';
import './css/GroupsList.css'; // Import the CSS file

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
        try {
            const response = await getGroups();
            setGroups(response.groups);
        } catch (error) {
            console.error('Error fetching groups:', error);
        }
    };

    const handleAddGroup = async (groupName) => {
        try {
            await addGroup(groupName);
            setMessage(`Group "${groupName}" added successfully!`);
            setMessageType('success');
        } catch (error) {
            setMessage(`Failed to add group "${groupName}". ${parseErrorResponse(error)}`);
            setMessageType('error');
        }
        fetchGroups();
        setShowAddGroup(false);
    };

    const handleDelete = async (groupName) => {
        const confirmDelete = window.confirm(`Are you sure you want to delete the group: ${groupName}?`);
        if (confirmDelete) {
            try {
                await deleteGroup(groupName);
                setGroups((prevGroups) => prevGroups.filter(group => group !== groupName));
                setMessage(`Group "${groupName}" deleted successfully!`);
                setMessageType('success');
            } catch (error) {
                setMessage(`Failed to delete group "${groupName}". ${parseErrorResponse(error)}`);
                setMessageType('error');
            }
        }
    };

    return (
        <div>
            <h1>Groups</h1>
            <button onClick={() => setShowAddGroup(true)} className="button-add-group">Add Group</button>
            {showAddGroup && <AddGroup onAddGroup={handleAddGroup} />}
            {message && <p className={`n-message ${messageType}`}>{message}</p>}

            <table>
                <thead>
                    <tr>
                        <th>Group Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {groups.map((group, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                            <td>{group}</td>
                            <td>
                                <button
                                    type="button"
                                    onClick={() => navigate(`/groups/${group}/words`)}
                                    className="button-spacing button-view-words"
                                >
                                    View Words
                                </button>
                                <button
                                    type="button"
                                    onClick={(e) => { e.stopPropagation(); handleDelete(group); }}
                                    className="button-spacing button-delete"
                                >
                                    Delete Group
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default GroupsList;
