import numpy as np

def length_score(answer:str):
    word_count=len(answer.split())

    if word_count<=40:
        return 0.3
    elif word_count<=150:
        return 1
    elif word_count>250:
        return 0.7
    else:
        return 0.6
    

def section_detected(answer:str):

    sections={"intro":["i am","talking about the project","project","idea"],
             "body":["worked on", "experience", "project", "skills"],
            "conclusion": ["looking to", "aim", "aspire", "want to"]
            }
    a=answer.lower()

    detected={
        sec:any(k in a for k in keys) for sec,keys in sections.items()
    }
    return detected


def ordering_score(answer:str,sections_detected:dict):
    a=answer.lower()
    positions={}
    for sec,present in sections_detected.items():
        if present:
            positions[sec]=a.find(sec)
        
    if not positions:
        return 0.0
    score = 1.0
    if "intro" in positions and "body" in positions:
        score *= 1.0 if positions["intro"] <= positions["body"] else 0.6
    if "body" in positions and "conclusion" in positions:
        score *= 1.0 if positions["body"] <= positions["conclusion"] else 0.6

    return round(score, 2)


def structure_score(answer:str):
    l_score=length_score(answer)
    secs=section_detected(answer)
    order=ordering_score(answer,secs)
    coverage=sum(secs.values())/len(secs)
    score=(
        0.4*l_score +
        0.4*coverage +
        0.2*order
    )
    return {
        "structure_score": round(score, 3),
        "length_score": l_score,
        "section_coverage": secs,
        "ordering_score": order
    }