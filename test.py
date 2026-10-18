
import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.title("Microphone Recorder Test")
st.write("Click Start, speak, then click Stop.")

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True,
    format="wav",
    key="mic_test"
)

if audio:
    st.success("Recording captured successfully!")

    st.audio(audio["bytes"], format="audio/wav")

    st.write("Sample rate:", audio["sample_rate"])
    st.write("Audio size:", len(audio["bytes"]), "bytes")

    st.download_button(
        "Download recording",
        data=audio["bytes"],
        file_name="test_recording.wav",
        mime="audio/wav"
    )
