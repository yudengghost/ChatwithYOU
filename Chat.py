from openai import OpenAI

class Chat:

    client = None

    def __init__(self, API_KEY: str):
        Chat.client = OpenAI(
            api_key=API_KEY,  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
            base_url="https://api.moonshot.cn/v1",
        )

        # 我们将 System Messages 单独放置在一个列表中，这是因为每次请求都应该携带 System Messages
        self.system_messages = [
            {"role": "system",
             "content": "你将扮演动漫《文豪野犬》里的太宰治，接下来请你用太宰治的身份和我说话"},
        ]

        self.messages = []
        # 我们定义一个全局变量 messages，用于记录我们和 Kimi 大模型产生的历史对话消息
        # 在 messages 中，既包含我们向 Kimi 大模型提出的问题（role=user），也包括 Kimi 大模型给我们的回复（role=assistant）
        # messages 中的消息按时间顺序从小到大排列

    def make_messages(self, input: str, n: int = 20) -> list[dict]:
        """
        使用 make_messaegs 控制每次请求的消息数量，使其保持在一个合理的范围内，例如默认值是 20。在构建消息列表
        的过程中，我们会先添加 System Prompt，这是因为无论如何对消息进行截断，System Prompt 都是必不可少
        的内容，再获取 messages —— 即历史记录中，最新的 n 条消息作为请求使用的消息，在大部分场景中，这样
        能保证请求的消息所占用的 Tokens 数量不超过模型上下文窗口。
        """
        # 首先，我们将用户最新的问题构造成一个 message（role=user），并添加到 messages 的尾部
        self.messages.append({
            "role": "user",
            "content": input,
        })

        # new_messages 是我们下一次请求使用的消息列表，现在让我们来构建它
        new_messages = []

        # 每次请求都需要携带 System Messages，因此我们需要先把 system_messages 添加到消息列表中；
        # 注意，即使对消息进行截断，也应该注意保证 System Messages 仍然在 messages 列表中。
        new_messages.extend(self.system_messages)

        # 在这里，当历史消息超过 n 条时，我们仅保留最新的 n 条消息
        if len(self.messages) > n:
            self.messages = self.messages[-n:]

        new_messages.extend(self.messages)

        return new_messages


    def chat(self, input: str) -> str:
        """
        chat 函数支持多轮对话，每次调用 chat 函数与 Kimi 大模型对话时，Kimi 大模型都会”看到“此前已经
        产生的历史对话消息，换句话说，Kimi 大模型拥有了记忆。
        """

        # 携带 messages 与 Kimi 大模型对话
        completion = Chat.client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.make_messages(input),
            temperature=0.5,
        )

        # 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
        assistant_message = completion.choices[0].message

    # 为了让 Kimi 大模型拥有完整的记忆，我们必须将 Kimi 大模型返回给我们的消息也添加到 messages 中
        self.messages.append(assistant_message)

        return assistant_message.content

if __name__ == '__main__':
    chat_client = Chat()
    while True:
        input_text = input("& ")
        if input_text == "exit":
            break
        output = chat_client.chat(input_text)
        print(output)