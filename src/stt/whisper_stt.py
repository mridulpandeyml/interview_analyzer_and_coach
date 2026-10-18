
import whisper
import soundfile as sf
import numpy as np
from scipy.signal import resample_poly
from math import gcd

model = whisper.load_model("base")


def transcribe_audio(audio_path):
    # Load WAV without invoking FFmpeg
    audio, sample_rate = sf.read(audio_path, dtype="float32")

    # Convert stereo to mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # Whisper expects audio sampled at 16 kHz
    if sample_rate != 16000:
        divisor = gcd(sample_rate, 16000)
        audio = resample_poly(
            audio,
            16000 // divisor,
            sample_rate // divisor
        ).astype(np.float32)

    result = model.transcribe(
        audio,
        language="en",
        task="transcribe",
        fp16=False,
        temperature=0.0,
        condition_on_previous_text=False,
        verbose=False,
    )

    return result["text"].strip(), result["segments"]
