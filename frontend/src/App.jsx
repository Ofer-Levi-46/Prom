import React, { useEffect, useState } from 'react';

const App = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    useEffect(() => {
        const eventSource = new EventSource('http://localhost:8000/events');
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.message) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: data.message, type: 'received' },
                ]);
            }
        };
        return () => eventSource.close();
    }, []);

    const handleSend = () => {
        if (input.trim()) {
            setMessages([...messages, { text: input, type: 'sent' }]);
            setInput('');

            fetch('http://localhost:8000/generate-wave', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input }),
            }).catch((error) => console.error('Error:', error));
        }
    };

    return (
        <div
            style={{
                fontFamily: 'Arial, sans-serif',
                padding: '10px',
                maxWidth: '400px',
                margin: '0 auto',
            }}
        >
            <h1 style={{ textAlign: 'center' }}>Chat App</h1>

            <div
                style={{
                    height: '70vh',
                    border: '1px solid #ccc',
                    borderRadius: '8px',
                    padding: '10px',
                    marginBottom: '10px',
                    backgroundColor: '#f9f9f9',
                }}
            >
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        style={{
                            marginBottom: '10px',
                            padding: '8px',
                            backgroundColor:
                                msg.type === 'received' ? '#d4edda' : '#e1f5fe',
                            borderRadius: '8px',
                            alignSelf: 'flex-start',
                        }}
                    >
                        {msg.text}
                    </div>
                ))}
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
                <input
                    type='text'
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder='Type a message...'
                    style={{
                        flex: 1,
                        padding: '10px',
                        borderRadius: '8px',
                        border: '1px solid #ccc',
                    }}
                />
                <button
                    onClick={handleSend}
                    style={{
                        padding: '10px 15px',
                        backgroundColor: '#007bff',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '8px',
                    }}
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default App;
