from openai import OpenAI

class Translation:
    client = None

    def __init__(self, language: str, API_KEY: str):
        Translation.client = OpenAI(
            api_key=API_KEY,  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
            base_url="https://api.moonshot.cn/v1",
        )
        # 我们将 System Messages 单独放置在一个列表中，这是因为每次请求都应该携带 System Messages
        self.system_messages = [
            {"role": "system",
             "content": "你是一名翻译官，负责将中文翻译成地道的"+language+"，并且只翻译内容而不带有其它信息。"},
        ]

    def make_message(self, input):
        messages = []
        user_message = {"role": "user",
                        "content": input}
        messages.append(user_message)
        messages.extend(self.system_messages)
        return messages

    def translate(self, input):
        completion = Translation.client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.make_message(input),
            temperature=0.3,
        )
        assistant_message = completion.choices[0].message
        return assistant_message.content

if __name__ == "__main__":
    translator = Translation('ja')
    assistant = translator.translate("早上好")
    print(assistant)