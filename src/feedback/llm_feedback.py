
def build_prompt(question,transcript,metrics):
    return f"""
    you are a professional interview and communication coach ,you are assigned a candidate along with its speech metrics
                Analyze the user's interview answer and provide constructive feedback.
                Base your feedback strictly on the provided metrics and transcript .
                do not mention scores explicitly.Identify the candidates weak points, and suggest ways to overcome 

    Interview question:{question}
    answer:{transcript}

    Analysis Metrics:
    - Speaking pace (WPM): {metrics["wpm"]}
    - Filler word density: {metrics["filler_density"]}
    - Pause count: {metrics["pause_count"]}
    - Confidence score: {metrics["confidence_score"]}
    - Relevance score: {metrics["relevance_score"]}
    - Structure score: {metrics["structure_score"]}
    - Content depth level: {metrics["depth_level"]}

    Task:
    1. Briefly evaluate overall performance.
    2. Identify the main strengths.
    3. Identify the main weaknesses.
    4. Suggest 2 to 3 specific improvements.

    Keep the feedback under 150 words.
    """

import cohere
import os

co = cohere.Client(os.getenv("COHERE_API_KEY"))
def generate_feedback(question,transcript,metrics):
    prompt=build_prompt(question,transcript,metrics)
    response=co.chat(
        model="command-a-03-2025",message=prompt,temperature=0.5
    )
    return response.text.strip()