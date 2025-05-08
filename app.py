import streamlit as st
import tempfile
import os
from predictor import predict
from run import download_with_ytdlp

st.set_page_config(page_title="Accent Classifier", page_icon="🗣️")
st.title("🗣️ English Accent Classifier")

st.markdown("""
Upload a short `.wav` or `.mp4` file, or paste a YouTube URL.
We'll try to identify the English accent from the speaker.
""")

option = st.radio("Select Input Type", ["Upload File", "YouTube URL"])

if option == "Upload File":
    uploaded_file = st.file_uploader("Choose a WAV or MP4 file", type=["wav", "mp4"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("Classifying accent..."):
            accent, confidence = predict(tmp_path)

        os.remove(tmp_path)
        st.success(f"Predicted Accent: **{accent}**")
        st.info(f"Confidence: {confidence:.2f}%")

elif option == "YouTube URL":
    url = st.text_input("Paste the YouTube video URL")
    if url:
        try:
            with st.spinner("Downloading and processing video..."):
                video_path = download_with_ytdlp(url)
                accent, confidence = predict(video_path)
                os.remove(video_path)

            st.success(f"Predicted Accent: **{accent}**")
            st.info(f"Confidence: {confidence:.2f}%")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
