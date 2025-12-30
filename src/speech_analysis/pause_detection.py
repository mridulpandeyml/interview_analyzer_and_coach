def detect_pause(segments,pause_threshold=0.5):
    pause=[]

    for i in range(1,len(segments)):
        end=segments[i-1]["end"]
        start=segments[i]["start"]
        if (start-end)>pause_threshold:
            pause.append(start-end)

    avg_pause=round(sum(pause)/len(pause),2) if len(pause)>0 else 0.0
    return{
        "pause_count":len(pause),
        "avg pause":avg_pause
    }

