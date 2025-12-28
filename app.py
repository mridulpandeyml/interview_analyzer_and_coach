import streamlit as st
from src.input.audio_capture import record_audio
from src.stt.whisper_stt import transcribe_audio
from src.storage.session_logger import save_transcript
from src.speech_analysis.speech_rate import speech_rate
from src.speech_analysis.filler_detection import filler_detect
from src.speech_analysis.repetition_detection import repetition

st.title("🎤 AI Interview & Communication Coach")
st.subheader("Phase 1: Audio to Transcript")

duration = st.slider("Recording duration (seconds)", 10, 60, 30)

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
    Speech_rate=speech_rate(transcript,time_duration)
    Filler_stats=filler_detect(transcript)
    rept=repetition(transcript)

    st.markdown("Speech Analysis")
    st.write({
    "Speech Rate (WPM)": Speech_rate,
    "Total Fillers Used": Filler_stats["total fillers used"],
    "Filler Density": Filler_stats["filler_density"],
    "Repetition Score": rept["repetition score"]
})