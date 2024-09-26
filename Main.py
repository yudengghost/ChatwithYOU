from Chat import Chat
from translation import Translation
from Voice import VoiceCreator
from playsound import playsound
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 创建聊天
chat_bot = Chat(config.get('API_KEY', 'openai_api_key'))
language: str = config.get('CONFIG', 'language')
print(language)
# 创建翻译
translator = Translation(language, config.get('API_KEY', 'openai_api_key'))
# 创建语音合成器
output_file = config.get('CONFIG',  'output')
voice_creator = VoiceCreator(speaker_wav=config.get('CONFIG', 'speaker_wav'), language=language, file_path=output_file)

# main
while True:
    input_text = input("& ")
    if input_text == "exit":
        break
    output = chat_bot.chat(input_text)
    output_translated = translator.translate(output)
    voice_creator.create_voice(output_translated)
    # 播放音频
    print(output)
    playsound(output_file)
