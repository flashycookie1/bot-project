import os

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from summarizer import Summarizer
import json

import google.generativeai as genai
from google.generativeai import caching
import datetime
import time

genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def handle_response(message,username) -> str:
    p_message = message.lower()

    if 'hello' in p_message:
        return f'hello, {username}!'
    
    if 'https://www.youtube.com/watch?v=' in p_message:
        video_link = message
        video_id = (video_link.replace('https://www.youtube.com/watch?v=', ''))

        raw_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        #  json_formatted = JSONFormatter().format_transcript(raw_transcript)
        #  json_formatted = json_formatted[1:-1]
        #  jsonobj = json.loads(json_formatted)

        transcript = ''

        print(type(raw_transcript), f': {raw_transcript}')

        for x in raw_transcript:
            transcript += (x['text']+' ')
        transcript = transcript.replace("\n", " ")

        response = model.generate_content("summarize the following video based on its transcript in under 100 words:" + transcript)

        # bert_model = Summarizer()
        # bert_summary = str(''.join(bert_model(transcript, min_length=60)))
        return(response.text)

    else:
        return None