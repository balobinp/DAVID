import os
from gtts import gTTS
language = 'ru'
file = "gas_danger.mp3"
text = 'Внимание! Повышенное содержание метана в воздухе.'
voice = gTTS(text=text, lang=language, slow=False) 
voice.save(file)
os.system("mpg123 " + file)
