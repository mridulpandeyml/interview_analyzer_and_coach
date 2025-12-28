from collections import Counter

def repetition(transcript:str,n=2):
    if not transcript:
        return {"repetition score":0.0}
    
    words=transcript.strip().split()
    bigram=list(zip(*[words[i:]for i in range(n)]))
    count=Counter(bigram)
    repeated=sum(c for c in count.values() if c>1)

    repetition_score=round(repeated/len(bigram),3)if count else 0.0

    return{"repetition score":repetition_score}