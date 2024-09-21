import streamlit as st 
import google.generativeai as genai
import os 
from dotenv import load_dotenv
from PIL import Image 
load_dotenv()
from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
Prompt= """You are an expert YouTube video summarizer. 
Your task is to analyze the provided transcript of the video 
and deliver a clear, concise summary highlighting the most important points. 
The summary should be structured in bullet points, capturing the key information 
and main takeaways in no more than 200 words. Ensure the summary is comprehensive, 
easy to understand, and avoids unnecessary details."""

def get_gemini_response(transcript,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript)
    return response.text

def youtube_transcriber(video_url):
    try:
        video_id=video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text']
    except Exception as e:
        raise e
    return transcript

st.set_page_config(page_title="Youtube Summarizer App")
st.header("Youtube Summarizer App!")
file = st.text_input("Your Youtube link here...")

if st.button("Summarize"):
    transcript = youtube_transcriber(file)
    if transcript:
       response = get_gemini_response(transcript,Prompt)
       st.markdown("## Summary")
       st.write(transcript)
