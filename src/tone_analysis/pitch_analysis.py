import librosa 
import numpy as np
def pitch(audio_path):
    y,sr=librosa.load(audio_path,sr=None)

    pitches,magnitude=librosa.piptrack(y=y,sr=sr)
    pitch_val=pitches[magnitude>np.median(magnitude)]
    pitch_val=pitch_val[pitch_val>0]

    if (len(pitch_val)==0):
        return 0.0
    pitch_var=np.var(pitch_val)
    normal_pitch=np.log1p(pitch_var)/np.log1p(1e6)
    normal_pitch=max(0.0,min(1.0,normal_pitch))
    return round(float(normal_pitch),3)    
