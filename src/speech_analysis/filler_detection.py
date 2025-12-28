import re
from config.fillers import Filler_words

def filler_detect(transcript:str):
    if not transcript:
        return{ "fillers":0,"filler_density":0.0}
    text=transcript.lower()
    words=text.split()
    total_words=len(words)

    filler=0
    for fillers in Filler_words:
        filler+=len(re.findall(rf"\b{fillers}\b",text))

    filler_density=round(filler/total_words,3) if total_words>0 else 0.0

    return{
        "total fillers used":filler,
        "filler_density":filler_density
    }
