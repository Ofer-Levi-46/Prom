from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from scipy.io.wavfile import write, read

import signal_processing as sig
import sounddevice as sd
import numpy as np
import json
import os
import asyncio
import threading
import time


app = FastAPI()
subscribers = []
is_sending = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or use ["*"] for all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/events")
async def events(request: Request):
    queue = asyncio.Queue()
    subscribers.append(queue)

    async def event_stream():
        try:
            while True:
                if await request.is_disconnected():
                    break
                data = await queue.get()
                yield f"data: {data}\n\n"
        finally:
            subscribers.remove(queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/send")
async def send(data: dict):
    message = f'{{"message": "{data["text"]}"}}'
    for q in subscribers:
        await q.put(message)
    return {"status": "sent"}


@app.post("/generate-wave")
async def generate_wave_req(request: Request):
    global is_sending

    is_sending = True
    data = await request.json()
    message = sig.record_start_key + data['message'] + sig.record_end_key
    wav_data = sig.generate_wave(sig.encode(sig.string_to_bits(message)))
    wav_data = wav_data / np.max(np.abs(wav_data))  # Normalize the audio data

    sd.play(wav_data, sig.fs)
    sd.wait()

    # set timeout to set is_sending to False
    time.sleep(0.5)
    is_sending = False
    
    return {"status": "ok"}

def on_start(signal):
    return

def while_interest(signal):
    return

def on_end(data):
    global is_sending

    if is_sending:
        return

    for q in subscribers:
        asyncio.run(q.put(f'{{"message": "{data}"}}'))

def blocking_listener():
    listener = sig.Listener(sig.fs, sig.record_start_key, sig.record_end_key, on_start, while_interest, on_end)
    listener.start_listening()

@app.on_event("startup")
def start_blocking_listener():
    thread = threading.Thread(target=blocking_listener, daemon=True)
    thread.start()