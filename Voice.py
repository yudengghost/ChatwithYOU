import torch
from TTS.api import TTS

class VoiceCreator:

    def __init__(self, speaker_wav, language="ja", file_path="output.wav"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        self.language = language
        self.speaker_wav = speaker_wav
        self.file_path = file_path


    def create_voice(self, text: str) -> None:
        self.tts.tts_to_file(text=text, speaker_wav=self.speaker_wav, language=self.language,
                        file_path=self.file_path)

if __name__ == '__main__':
    voice_creator = VoiceCreator(speaker_wav="E:\\Users\\downloads\\speaker.wav", language="ja", file_path="output.wav")
    voice_creator.create_voice("またお会いしましょう")

# # 本地下载模型运行
# # Get device
# device = "cuda" if torch.cuda.is_available() else "cpu"
#
# # List available 🐸TTS models
# print(TTS().list_models())
# # Init TTS
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
#
# tts.tts_to_file(text="またお会いしましょう", speaker_wav="E:\\Users\\downloads\\speaker.wav", language="ja", file_path="output.wav")