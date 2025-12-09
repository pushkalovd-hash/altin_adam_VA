from gtts import gTTS
import os, playsound

tts = gTTS("ЗДРАСТВУЙТЕ", lang='ru')
tts.save("speek.mp3")
playsound('speek.mp3')