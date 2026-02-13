import streamlit as st
from src.input.audio_capture import record_audio
from src.stt.whisper_stt import transcribe_audio
from src.storage.session_logger import save_transcript
from src.speech_analysis.speech_rate import speech_rate
from src.speech_analysis.filler_detection import filler_detect
from src.speech_analysis.repetition_detection import repetition
from src.speech_analysis.pause_detection import detect_pause
from src.tone_analysis.pitch_analysis import pitch
from src.tone_analysis.stability import stability
from src.tone_analysis.hesitation_confidence import hesitation_index,confidence_score
from src.nlp_analysis.relevance import analyze_relevance
from src.nlp_analysis.structure import structure_score
from src.depth_analysis.specificity_depth import depth
from src.feedback.llm_feedback import generate_feedback
#from src.feedback import metrics
st.title("🎤 AI Interview & Communication Coach")
st.subheader(" Audio to Transcript")
question=st.text_input("### Interview Questions")

duration = st.slider("Recording duration (seconds)", 5, 60, 30)

if st.button("Start Recording"):
    audio_path, session_id = record_audio(duration)
    
    with st.spinner("Transcribing audio..."):
        transcript, segments = transcribe_audio(audio_path)

    save_path = save_transcript(session_id, transcript, segments)

    st.success("Transcript generated successfully!")

    st.markdown("### 📝 Transcript")
    st.write(transcript)
    st.markdown("### 💾 Saved At")
    st.code(save_path)
    time_duration=segments[1]["end"] if segments else 0.0
    # Speech Analysis
    Speech_rate=speech_rate(transcript,time_duration)
    Filler_stats=filler_detect(transcript)
    rept=repetition(transcript)
    pause_analysis=detect_pause(segments)
    # Tone Analysis
    pitch_variance=pitch(audio_path)
    Stability=stability(audio_path)
    hesitation=hesitation_index(pause_analysis,Filler_stats,pitch_variance)
    confidence=confidence_score(hesitation,Stability,pitch_variance)
    # Relevance
    relevance=analyze_relevance(question,transcript)
    # Structure
    structur_analysis=structure_score(transcript)
    # DEPTH 
    depth_analysis=depth(question,transcript)

    #analysis=st.selectbox("Analyze",["SPEECH","TONE","ANSWER RELEVANCE"])
    st.markdown("### Speech Analysis")
    st.write({
    "Speech Rate (WPM)": Speech_rate,
    "Total Fillers Used": Filler_stats["total fillers used"],
    "Filler Density": Filler_stats["filler_density"],
    "Repetition Score": rept["repetition score"],
    "Pauses":pause_analysis["pause_count"],
    "avg pause":pause_analysis["avg pause"]
    })
    
    st.markdown("### 🎤 Tone and Confidence")
    st.write({
        "Pitch variation":pitch_variance,
        "stability":Stability,
        "Hesitation":hesitation,
        "Confidence meter":confidence
    })

    st.markdown("### Answer Analysis")
    st.write({
    "relevance Score": relevance["relevance score"],
    "semantic similarity": relevance["semantic similarity"],
    "keyword overlap ratio": relevance["keyword overlap ratio"]
    })

    if relevance["off topic sentences"]:
        st.markdown("### ⚠️ Off-topic segments")
        for s in relevance["off topic sentences"]:
            st.write("-", s)
    
    st.markdown("### Structure Analysis")
    st.write({
        "length score":structur_analysis["length_score"],
        "ordering score":structur_analysis["ordering_score"],
        "section covered":structur_analysis["section_coverage"],
        "structure score":structur_analysis["structure_score"]
    })
    #DEPTH

    st.markdown("### depth analysis")
    st.write({
        "coverage score":depth_analysis["coverage_score"],
        "specificity":depth_analysis["specificity_score"],
        "depth":depth_analysis["depth_score"],
        "level":depth_analysis["level"]

    })
    metrics = {
    "wpm":Speech_rate,    
    "pause_count": pause_analysis["pause_count"], 
    "filler_density": Filler_stats["filler_density"], 
    "repetition_score": rept["repetition score"],
    "confidence_score": confidence, 
    "hesitation_score": hesitation, 
    "pitch_variation": pitch_variance,
    "relevance_score": relevance["relevance score"],
    "structure_score": structur_analysis["structure_score"],     
    "depth_level": depth_analysis["level"]
}

    feedback=generate_feedback(
        question,
        transcript,
        metrics
    )
    st.markdown("### AI FEEDBACK")
    st.write(feedback)