import librosa
import numpy as np

def stability(audio_path):
    y,sr=librosa.load(audio_path,sr=None)
    rms=librosa.feature.rms(y=y)

    if(len(rms)==0):
        return 0.0
    stable=1-(np.std(rms)/(np.mean(rms)+1e-6))
    stable=max(0.0,min(1.0,stable))

    return round(float(stable),3)