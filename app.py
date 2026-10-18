import streamlit as st
import tempfile
import uuid
from pathlib import Path
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


# Browser-based recording
audio = record_audio()


if audio is not None and audio.get("bytes"):
    audio_path = None
    st.markdown("### Debug: Recorded Audio")
    st.audio(audio["bytes"], format="audio/wav")
    st.write("Audio size:", len(audio["bytes"]), "bytes")
    st.write("Sample rate:", audio.get("sample_rate"))
    try:
        # Save browser-recorded audio temporarily for Whisper/librosa
        with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False
        ) as temp_audio:
            temp_audio.write(audio["bytes"])
            audio_path = temp_audio.name

        # Create a session ID for saving the transcript
        session_id = str(uuid.uuid4())

        with st.spinner("Transcribing audio..."):
            transcript, segments = transcribe_audio(audio_path)

        save_path = save_transcript(session_id, transcript, segments)

        st.success("Transcript generated successfully!")
        st.markdown("### 📝 Transcript")
        st.write(transcript)

        st.markdown("### 💾 Saved At")
        st.code(save_path)

        # Calculate duration from the final segment
        time_duration = (
            segments[-1]["end"] if segments else 0.0
        )

        # Speech analysis
        Speech_rate = speech_rate(transcript, time_duration)
        Filler_stats = filler_detect(transcript)
        rept = repetition(transcript)
        pause_analysis = detect_pause(segments)

        # Tone analysis
        pitch_variance = pitch(audio_path)
        Stability = stability(audio_path)
        hesitation = hesitation_index(
            pause_analysis, Filler_stats, pitch_variance
        )
        confidence = confidence_score(
            hesitation, Stability, pitch_variance
        )


        # Answer analysis
        relevance = analyze_relevance(question, transcript)
        structur_analysis = structure_score(transcript)
        depth_analysis = depth(question, transcript)

        # Metrics for the LLM
        metrics = {
            "wpm": Speech_rate,
            "pause_count": pause_analysis["pause_count"],
            "filler_density": Filler_stats["filler_density"],
            "repetition_score": rept["repetition score"],
            "confidence_score": confidence,
            "hesitation_score": hesitation,
            "pitch_variation": pitch_variance,
            "relevance_score": relevance["relevance score"],
            "structure_score": structur_analysis["structure_score"],
            "depth_level": depth_analysis["level"],
        }

        with st.spinner("Generating AI feedback..."):
            feedback = generate_feedback(
                question, transcript, metrics
            )

        st.markdown("### 🤖 AI Feedback")
        st.write(feedback)

        st.markdown("### Speech Analysis")
        st.write({
            "Speech Rate (WPM)": Speech_rate,
            "Total Fillers Used": Filler_stats["total fillers used"],
            "Filler Density": Filler_stats["filler_density"],
            "Repetition Score": rept["repetition score"],
            "Pauses": pause_analysis["pause_count"],
            "Average Pause": pause_analysis["avg pause"],
        })

        st.markdown("### 🎤 Tone and Confidence")
        st.write({
            "Pitch Variation": pitch_variance,
            "Stability": Stability,
            "Hesitation": hesitation,
            "Confidence Meter": confidence,
        })

        st.markdown("### Answer Analysis")
        st.write({
            "Relevance Score": relevance["relevance score"],
            "Semantic Similarity": relevance["semantic similarity"],
            "Keyword Overlap Ratio": relevance["keyword overlap ratio"],
        })

        if relevance["off topic sentences"]:
            st.markdown("### ⚠️ Off-topic segments")
            for sentence in relevance["off topic sentences"]:
                st.write("-", sentence)

        st.markdown("### Structure Analysis")
        st.write({
            "Length Score": structur_analysis["length_score"],
            "Ordering Score": structur_analysis["ordering_score"],
            "Sections Covered": structur_analysis["section_coverage"],
            "Structure Score": structur_analysis["structure_score"],
        })

        st.markdown("### Depth Analysis")
        st.write({
            "Coverage Score": depth_analysis["coverage_score"],
            "Specificity": depth_analysis["specificity_score"],
            "Depth": depth_analysis["depth_score"],
            "Level": depth_analysis["level"],
        })

    finally:
        # Delete the temporary audio file after processing
        if audio_path and Path(audio_path).exists():
            Path(audio_path).unlink()
