import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

prompt =" You are a Youtube video summarizer.You will be taking trascript and summarize entire video in less than 100 words.The transcript text will be appended here"

##Getting the transcript from YT Video
def extract_transcript_details(youtube_video_url):
    try:
        video_id ="HFfXvfFe9F8"
        # video_id = youtube_video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.fetch(video_id)
        print(transcript)
        # transcript_list = YouTubeTranscriptApi.fetch(video_id)
        # print(transcript_text)

        transcript= ""
        for i in transcript_text :
            transcript_text += i["text"]
        return transcript

    except Exception as e:
        raise e

##Getting the summary based on prompt from Gemini
def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(promopt+ transcript_text)
    return response.text


st.title("YT to transcript convertor")
yt_link = st.text_input("Enter YT link")

if yt_link:
    video_id = yt_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get detailed notes"):
    transcript_text = extract_transcript_details(yt_link)    

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("##Detailed Notes")
        st.write(summary)


