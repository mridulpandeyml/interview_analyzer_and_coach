import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import uuid
import os

SAMPLE_RATE = 16000

def record_audio(duration, save_dir="data/raw/audio"):
    os.makedirs(save_dir, exist_ok=True)

    session_id = str(uuid.uuid4())
    file_path = os.path.join(save_dir, f"{session_id}.wav")

    print("🎙️ Recording started...")
    audio = sd.rec(int(duration * SAMPLE_RATE),
                    samplerate=SAMPLE_RATE,
                    channels=1,
                    dtype='int16')
    sd.wait()
    print("✅ Recording finished")

    write(file_path, SAMPLE_RATE, audio)

    return file_path, session_id
