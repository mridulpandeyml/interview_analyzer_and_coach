import numpy as np
from sentence_transformers import SentenceTransformer
_model=SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text:str):
    if not text or not text.strip():
        return None
    embedding=_model.encode(text,normalize_embeddings=True)
    return embedding


def similarity(vect1,vect2):
    if vect1 is None or vect2 is None:
        return 0.0
    
    similar=np.dot(vect1,vect2)
    return round(float(similar),3)


