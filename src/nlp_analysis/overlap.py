import re

def kwrod_xtrct(text:str):
    words=re.findall(r"\b[a-zA-Z]{3,}\b",text.lower())
    return set(words)


def overlap_ratio(question:str,answer:str):
    q_embd=kwrod_xtrct(question)
    a_embd=kwrod_xtrct(answer)

    if not q_embd:
        return 0.0
    overlap=q_embd.intersection(a_embd)
    ratio=len(overlap)/len(q_embd)
    return round(float(ratio),3)