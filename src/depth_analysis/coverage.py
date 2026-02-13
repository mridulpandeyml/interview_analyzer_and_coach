import re

def extract_concept(text):
    words=re.findall(r"\b[a-zA-Z]{4,}\b",text.lower())
    stopwords={"about", "your", "what", "explain", "describe", "tell"}
    return set(w for w in words if w not in stopwords)


def concept_coverage(question,answer):
    q_concept=extract_concept(question)
    a_text=answer.lower()

    if not q_concept:
        return 0.0,[]
    covered=[c for c in q_concept if c in a_text]
    missing=list(q_concept-set(covered))

    score=len(covered)/len(q_concept)
    return round(score,3),missing