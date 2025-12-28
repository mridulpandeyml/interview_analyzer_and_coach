def speech_rate(transcript:str,time_duration:float):
    if not transcript or time_duration <=0.0:
        return 0.0
    
    words=transcript.strip().split()
    total_words=len(words)
    wpm=(total_words/time_duration)*60
    return round(wpm,2)