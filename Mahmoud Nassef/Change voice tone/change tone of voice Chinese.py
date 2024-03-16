from gtts import gTTS
import speech_recognition as sr
import os 
import pygame

# Function to recognize user's speech (Chinese)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now (in Chinese)...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language='zh-CN')  # Recognize Chinese (zh-CN)
            return text
        except sr.UnknownValueError:
            print("对不起，我听不懂 (Duìbù qǐng, wǒ tīng bù懂) [Sorry, I could not understand]")  # Chinese error message
            return None
        except sr.RequestError as e:
            print("无法从 Google 语音识别服务请求结果； {0} (Wúfǎ cóng Gǒogle yǔyīn shìbié fúwù qǐngqiú jiéguǒ; {0})"
                  .format(e))  # Chinese error message
            return None

# Function to speak text (Chinese) using gTTS
def speak_text(text):
   output_dir = "G:\Work"
   output_file = os.path.join(output_dir, "output.mp3")

   tts = gTTS(text=text, lang='zh-CN')
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
            print("您说 (Nín shuō) [You said]:", user_text)  # Chinese confirmation message
            speak_text(user_text)  # Speak the recognized text in Chinese using gTTS

if __name__ == "__main__":

    main()
