import speech_recognition as sr
import pyttsx3
import time

# Function to recognize user's speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None

# Function to speak text with adjustable tone
def speak_text(text, rate=175, volume=0.8):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Choose a voice with a different tone if available
    for voice in voices:
        if 'english+m2' in voice.id:  # Example: Male voice (adjust ID for different tones)
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', rate)  # Adjust speaking rate (words per minute)
    engine.setProperty('volume', volume)  # Adjust volume (0-1)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def main():
    while True:
        user_text = recognize_speech()
        if user_text:
            speak_text(user_text)
        else:
            print("No speech recognized.")
        time.sleep(1)  # Short pause between loops

if __name__ == "__main__":
    main()
