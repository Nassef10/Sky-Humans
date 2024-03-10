import speech_recognition as sr
import os
import requests  # For making API requests
import pyttsx3  # For text-to-speech

# Replace these with your actual API keys
OPENAI_API_KEY = "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"
GOOGLE_CLOUD_SPEECH_API_KEY = "YOUR_GOOGLE_CLOUD_SPEECH_API_KEY"  # Optional for Google Speech-to-Text


def recognize_speech():
    """
    Uses SpeechRecognition to record audio and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)  # Use Google API key if available
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def send_to_chatgpt(text):
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
            {"role": "system", "content": "You are a professional salesperson named rabeh whose answer does not exceed one line of full english advice and avoid sentence cut at the end due to finish of tokens."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def speak_text(text):
    """
    Uses pyttsx3 to convert text to speech and speak it.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    while True:
        user_text = recognize_speech()
        if user_text:
            chatgpt_response = send_to_chatgpt(user_text)
            if chatgpt_response:
                speak_text(chatgpt_response)
            else:
                print("ChatGPT failed to respond.")
        else:
            print("No speech recognized.")
