import os
from gtts import gTTS
language = 'ru'
file = "naughty_children.mp3"
text = 'Дети, не шумите, вы мне уже надоели.'
voice = gTTS(text=text, lang=language, slow=False) 
voice.save(file)
os.system("mpg123 " + file)
