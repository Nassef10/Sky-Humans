from gtts import gTTS
import speech_recognition as sr
import pygame
import os  # Import for playing the audio file (requires mpg321)

# Function to recognize user's speech (Spanish)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla ahora (Speak now)...")  # Spanish prompt
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language='es-ES')  # Recognize Spanish (es-ES)
            return text
        except sr.UnknownValueError:
            print("Lo siento, no te entendí (Lo siento, no te entendí)")  # Spanish error message
            return None
        except sr.RequestError as e:
            print("No se pudieron solicitar resultados del servicio Google Speech Recognition; {0} (No se pudieron solicitar resultados del servicio Google Speech Recognition; {0})"
                  .format(e))  # Spanish error message
            return None

# Function to speak text (Spanish) using gTTS
def speak_text(text):
   output_dir = "G:\Work"
   output_file = os.path.join(output_dir, "output.mp3")

   tts = gTTS(text=text, lang='es-ES')
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
            print("Dijiste (Dijiste):", user_text)  # Spanish confirmation message
            speak_text(user_text)  # Speak the recognized text in Spanish using gTTS

if __name__ == "__main__":
    
    main()
