import re
from src.nlp_analysis.embeddings import get_embedding,similarity
from src.nlp_analysis.overlap import overlap_ratio

def split(text:str):
    return [s.strip()for s in re.split(r"[.!?]", text) if len(s.strip()) > 10]


def analyze_relevance(question:str,answer:str):
    q_emb=get_embedding(question)
    a_emb=get_embedding(answer)

    semantic_similarity=similarity(q_emb,a_emb)
    key_overlap_ratio=overlap_ratio(question,answer)

    of_topic=[]
    for sentence in split(answer):
        s_emb=get_embedding(sentence)
        sim=similarity(q_emb,s_emb)
        if sim<0.35:
            of_topic.append(sentence)

    relevance_score=(0.7*semantic_similarity +0.3*key_overlap_ratio)
    relevance_score=max(0.0,min(1.0,relevance_score))
    return{
        "relevance score":round(float(relevance_score),3),
        "semantic similarity":semantic_similarity,
        "keyword overlap ratio":key_overlap_ratio,
        "off topic sentences":of_topic
    }