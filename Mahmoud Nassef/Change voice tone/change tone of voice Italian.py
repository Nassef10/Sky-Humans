from gtts import gTTS
import speech_recognition as sr
import pygame
import os  # Import for playing the audio file (requires mpg321)

# Function to recognize user's speech (Italian)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parla ora (Speak now)...")  # Italian prompt
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language='it-IT')  # Recognize Italian (it-IT)
            return text
        except sr.UnknownValueError:
            print("Mi dispiace, non ho capito (Mi dispiace, non ho capito)")  # Italian error message
            return None
        except sr.RequestError as e:
            print("Impossibile ottenere risultati dal servizio Google Speech Recognition; {0} (Impossibile ottenere risultati dal servizio Google Speech Recognition; {0})"
                  .format(e))  # Italian error message
            return None

# Function to speak text (Italian) using gTTS
def speak_text(text):
    output_dir = "G:\Work"  # Modify this path if needed
    output_file = os.path.join(output_dir, "output.mp3")

    tts = gTTS(text=text, lang='it')  # Set language to Italian (it)
    tts.save(output_file)

    pygame.mixer.init()  # Initialize Pygame's mixer module

    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Audio playback finished, remove the file
    pygame.mixer.quit()
    os.remove(output_file)


def main():
    while True:
        user_text = recognize_speech()
        if user_text:
            print("Hai detto (Hai detto):", user_text)  # Italian confirmation message
            speak_text(user_text)  # Speak the recognized text in Italian using gTTS


if __name__ == "__main__":
    main()
