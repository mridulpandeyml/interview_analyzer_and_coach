
import streamlit as st
from streamlit_mic_recorder import mic_recorder


def record_audio():
    audio = mic_recorder(
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="communication_enhancer_mic",
    )

    if audio is None:
        return None

    if not audio.get("bytes"):
        st.warning("No audio was captured. Please try recording again.")
        return None

    return audio
