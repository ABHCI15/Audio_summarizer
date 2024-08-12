import streamlit as st
import pathlib
import google.generativeai as gemini
from pytubefix import YouTube
import whisper
import soundfile as sf
from tempfile import NamedTemporaryFile
from pytube.innertube import _default_clients

_default_clients["ANDROID_MUSIC"] = _default_clients["WEB"]
gemini.configure(api_key=st.secrets["api_key"])
# model = gemini.GenerativeModel(model_name="gemini-1.5-pro")
# data = gemini.upload_file(path='test.mp3')
# prompt = "generate an english only transcription of this audio file"
# response = model.generate_content([prompt, data])
# print(response.text)

st.title("Audio Summarizer")
# st.balloons()
file = st.file_uploader("upload your audio file", type=["mp3", "wav"])
st.header("Or enter a YT link")
yt_url = st.text_input("Enter YouTube URL")
engem_tc = st.button("Generate English Transcription with Gemini")
eng_tc = st.button("Generate English Transcription with Whisper")
oth_tc = st.button("Generate Another Language Transcription with Whisper")
summarize_wh = st.button("Summarize with Whisper")
summarize_gem = st.button("Summarize with Gemini")
download_mp3 = st.button("Download MP3")
download_mp4 = st.button("Download MP4")

def streamer(response):
    for chunk in response:
        yield chunk.text



if download_mp3:
    if yt_url:
        yt = YouTube(yt_url)
        st.write(yt.title)
        ys = yt.streams.get_highest_resolution()
        ys.download(filename="audio.mp3")
        with open('audio.mp3', 'rb') as f:
            st.download_button('Download mp3', f, file_name='audio.mp3', mime='audio/mp3') 

if download_mp4:
    if yt_url:
        yt = YouTube(yt_url)
        st.write(yt.title)
        ys = yt.streams.get_highest_resolution()
        ys.download(filename="audio.mp4")
        with open('audio.mp4', 'rb') as f:
            st.download_button('Download mp4', f, file_name='audio.mp4')

if eng_tc:
    if file is not None:
        with st.spinner("Processing..."):
            with NamedTemporaryFile(suffix=".mp3") as temp:
                temp.write(file.getvalue())
                temp.seek(0)
                model = whisper.load_model("tiny.en")
                result = model.transcribe(temp.name)
                st.write(result["text"])
    if yt_url:
        with st.spinner("Processing..."):
            yt = YouTube(yt_url)
            st.write(yt.title)
            ys = yt.streams.get_highest_resolution()
            ys.download(mp3=True,filename="audio")
            model = whisper.load_model("tiny.en")
            result = model.transcribe("audio.mp3", word_timestamps=True)
            st.write(result["text"])

if oth_tc:
    if file is not None:
        with st.spinner("Processing..."):
            with NamedTemporaryFile(suffix=".mp3") as temp:
                temp.write(file.getvalue())
                temp.seek(0)
                model = whisper.load_model("tiny")
                result = model.transcribe(temp.name)
                st.write(result["text"])
    if yt_url:
        with st.spinner("Processing..."):
            yt = YouTube(yt_url)
            st.write(yt.title)
            ys = yt.streams.get_highest_resolution()
            ys.download(mp3=True,filename="audio")
            model = whisper.load_model("tiny")
            result = model.transcribe("audio.mp3", word_timestamps=True)
            st.write(result["text"])

if engem_tc:
    if file is not None:
        with st.spinner("Processing..."):
            with NamedTemporaryFile(suffix=".mp3") as temp:
                temp.write(file.getvalue())
                temp.seek(0)
                # st.write(temp.name)
                model = gemini.GenerativeModel(model_name="gemini-1.5-pro")
                data = gemini.upload_file(path=temp.name)
                prompt = "generate a transcription of this audio file"
                response = model.generate_content([prompt, data])
                st.write(response.text)
    if yt_url:
        with st.spinner("Processing..."):
            yt = YouTube(yt_url)
            st.write(yt.title)
            ys = yt.streams.get_highest_resolution()
            ys.download(mp3=True,filename="audio")
            model = gemini.GenerativeModel(model_name="gemini-1.5-pro")
            data = gemini.upload_file(path="audio.mp3")
            prompt = "generate a english only transcription of this audio file"
            response = model.generate_content([prompt, data])
            st.write(response.text)

if summarize_gem:
    if file is not None:
        with st.spinner("Processing..."):
            with NamedTemporaryFile(suffix=".mp3") as temp:
                temp.write(file.getvalue())
                temp.seek(0)
                # st.write(temp.name)
                model = gemini.GenerativeModel(model_name="gemini-1.5-pro")
                data = gemini.upload_file(path=temp.name)
                prompt = "generate a thorough summary with notes of this audio file"
                response = model.generate_content([prompt, data])
                st.write(response.text)
    if yt_url:
        with st.spinner("Processing..."):
            try:
                yt = YouTube(yt_url)
            except:
                yt = YouTube(yt_url,use_oauth=True, allow_oauth_cache=True)
            ys = yt.streams.get_highest_resolution()
            ys.download(mp3=True,filename="audio")
            model = gemini.GenerativeModel(model_name="gemini-1.5-pro-exp-0801", generation_config=gemini.GenerationConfig(max_output_tokens=8192))
            data = gemini.upload_file(path="audio.mp3")
            prompt = "Write thorough notes with excellent detail and attention, similar to how a student would in a condensed manner such that the reader remembers everything from the audio, include every important section. You have access to over 8000 tokens in output tokens, use them all if necessary."
            response = model.generate_content([prompt, data], stream=True)
            st.write_stream(streamer(response))

if summarize_wh:
    if file is not None:
        with st.spinner("Processing..."):
            with NamedTemporaryFile(suffix=".mp3") as temp:
                temp.write(file.getvalue())
                temp.seek(0)
                model = whisper.load_model("tiny")
                result = model.transcribe(temp.name)
                print(result["text"])
                model = gemini.GenerativeModel(model_name="gemini-1.5-pro")
                response = model.generate_content(f"generate a thorough summary with notes of this transcription: {result['text']}")
                st.write(response.text)
    if yt_url:
        with st.spinner("Processing..."):
            yt = YouTube(yt_url)
            st.write(yt.title)
            ys = yt.streams.get_highest_resolution()
            ys.download(mp3=True,filename="audio")
            model = whisper.load_model("tiny")
            result = model.transcribe("audio.mp3", word_timestamps=True)
            print(result["text"])
            model = gemini.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content(f"generate a thorough summary with notes of this transcription: {result['text']}")
            st.write(response.text)
