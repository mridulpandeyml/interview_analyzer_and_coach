import numpy as np 
from src.depth_analysis.coverage import concept_coverage

def specificity(answer):
    atext=answer.lower().split()

    vague_words=["stuff","things","whatever","only","actually","basically","literally","i think","really",
                 "very","good","nice","interesting"]
    
    meaningful=[w for w in atext if w not in vague_words]
    if not meaningful:
        return 0.0
    specificity_score=len(meaningful)/len(atext)
    return round(specificity_score,3)


def depth(question,answer):
    coverage,missing=concept_coverage(question,answer)
    specificity_score=specificity(answer)

    score=(
        0.4*coverage+
        0.6*specificity_score
    )

    if score<0.4:
        level="shallow"
    elif score<0.7:
        level="adequate"
    else:
        level="strong"
    
    
    return{
        "coverage_score":coverage,
        "specificity_score":specificity_score,
        "depth_score":round(score,3),
        "level":level
    }