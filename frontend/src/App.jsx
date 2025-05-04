import React, { useRef, useState } from 'react';

const App = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const [recording, setRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

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
            })
                .then((response) => response.json())
                .then((data) => playAudio(data.wav))
                .catch((error) => console.error('Error:', error));

            const playAudio = (data) => {
                const audioContext = new (window.AudioContext ||
                    window.webkitAudioContext)();
                const buffer = audioContext.createBuffer(1, data.length, 48000);
                buffer.getChannelData(0).set(data);
                const source = audioContext.createBufferSource();
                source.buffer = buffer;
                source.connect(audioContext.destination);
                source.start(0);
            };
        }
    };

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });

        // create a new MediaRecorder instance of wav files recording at a sample rate of 48000 Hz
        const mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/wav',
        });
        mediaRecorderRef.current = mediaRecorder;
        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunksRef.current.push(event.data);
                console.log('Audio chunk available:', event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunksRef.current, {
                type: 'audio/mp4',
            });
            const reader = new FileReader();

            reader.onloadend = () => {
                const arrayBuffer = reader.result;
                const audioContext = new (window.AudioContext ||
                    window.webkitAudioContext)();
                audioContext.decodeAudioData(arrayBuffer, (decodedData) => {
                    const audioDataArray = decodedData.getChannelData(0);
                    console.log(audioDataArray); // Process or send the audio data array as needed
                });
            };

            reader.readAsArrayBuffer(audioBlob);
        };

        mediaRecorder.start();
        setRecording(true);
    };

    const stopRecording = () => {
        mediaRecorderRef.current.stop();
        setRecording(false);
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
                        cursor: recording ? 'not-allowed' : 'pointer',
                        opacity: recording ? 0.5 : 1,
                        pointerEvents: recording ? 'none' : 'auto',
                        transition:
                            'background-color 0.1s ease, opacity 0.1s ease',
                    }}
                >
                    Send
                </button>
            </div>
            <button
                onClick={recording ? stopRecording : startRecording}
                style={{
                    marginTop: '10px',
                    padding: '10px 15px',
                    backgroundColor: recording ? '#dc3545' : '#28a745',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    width: '100%',
                }}
            >
                {recording ? 'Stop Recording' : 'Start Recording'}
            </button>
        </div>
    );
};

export default App;
