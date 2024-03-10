import os

import pygame
import speech_recognition as sr
import requests
import pyttsx3
from gtts import gTTS
from langdetect import detect

# Replace this with your actual API key
OPENAI_API_KEY = "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"


def recognize_speech():
    """
    Uses SpeechRecognition to record audio and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ar-EG")
        print("You said (Arabic): " + text)
        return text, "arabic"
    except sr.UnknownValueError:
        try:
            text = recognizer.recognize_google(audio)
            print("You said (English): " + text)
            return text, "english"
        except sr.UnknownValueError:
            print("Sorry, I could not understand audio")
            return None, None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None, None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None, None


def send_to_chatgpt(text, lang):
    """
    Sends the text to ChatGPT API (using v1/chat/completions) and returns the response.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to ChatGPT API: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing response from ChatGPT API: {e}")
        return None


def speak_text(text):
    """
    Uses pyttsx3 to convert text to speech and speak it.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()





def speak_text_arabic(text):
    """
    Uses gTTS to convert Arabic text to speech and play it using pygame.
    """
    output_dir = "C:/output"
    output_file = os.path.join(output_dir, "output.mp3")

    tts = gTTS(text=text, lang='ar')
    tts.save(output_file)

    pygame.mixer.init()  # Initialize Pygame's mixer module

    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Audio playback finished, remove the file
    pygame.mixer.quit()
    os.remove(output_file)

    print(f"Audio removed: {output_file}")


if __name__ == "__main__":
    while True:
        user_text, lang = recognize_speech()
        if user_text:
            if lang == "arabic":
                chatgpt_response = send_to_chatgpt(user_text, "arabic")
                if chatgpt_response:
                    speak_text_arabic(chatgpt_response)
                else:
                    print("ChatGPT failed to respond.")
            elif lang == "english":
                chatgpt_response = send_to_chatgpt(user_text, "english")
                if chatgpt_response:
                    speak_text(chatgpt_response)
                else:
                    print("ChatGPT failed to respond.")
        else:
            print("No speech recognized.")
