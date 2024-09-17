

import speech_recognition as sr
from openai import OpenAI
import pyttsx3
engine = pyttsx3.init()
recognizer = sr.Recognizer()
def speak(text):  # This function takes a string text as input and
    engine.say(text)
    engine.runAndWait()
def talk():# talk and print out what you said
    with sr.Microphone() as source:
        print("Talk to me...")
        # Adjust the pause threshold to make the recognizer wait longer before considering silence
        #recognizer.pause_threshold = 5.0  # Default is 0.8 seconds, increase if you want longer pauses allowed
        #recognizer.non_speaking_duration = 5 # Adjusts the duration of silence before ending a phrase
        #recognizer.energy_threshold = 300  # Adjusts the sensitivity to ambient noise
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)

            ai_response=generate_response(text)
            print("Response: "+ai_response)
            speak(ai_response)
        except sr.UnknownValueError:
            speak("Sorry, Could you please repeat")
            print("Sorry, Could you please repeat")
        except sr.RequestError:
            speak("your network is weak ")
            print("your network is weak ")
        return text

key="Private"
client=OpenAI(
    api_key=key,
)

def generate_response(message):
    response= client.chat.completions.create(
        model="gpt-3.5-turbo",#model
        messages=[{"role":"user","content":message}]
        #max_tokens=150
    )
    return response.choices[0].message.content.strip()

speak("Hi, I'm Enyce How can i assist you")
word=talk()
