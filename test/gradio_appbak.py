import gradio as gr
import requests
import json
from difflib import SequenceMatcher
import brain_app
from zhipuai import ZhipuAI




client = ZhipuAI(api_key="50fd0042b4254f7b834487a7e6426276.5EeZ3qaC9sBN0w1o") # 请填写您自己的APIKey



# print(response)
# for chunk in response:
#     print(chunk.choices[0].delta)
class Chatbot:
    def __init__(self):
        self.url = "https://api.baichuan-ai.com/v1/chat/completions"
        self.api_key = "sk-86340cb476b9fbd5bf5406e72b202cd2"
        self.messages = []

    def do_request(self, messages):
        data = {
            "model": "Baichuan-NPC-Turbo",
            "character_profile": {
                "character_id": 31096
            },
            "messages": messages,
            "temperature": 0.8,
            "top_p": 0.98,
            "max_tokens": 512,
            "stream": False
        }

        json_data = json.dumps(data)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        response = requests.post(self.url, data=json_data, headers=headers, timeout=60)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def chat(self, input_text):
        while len(self.messages) > 40:
            self.messages.pop(0)  # 删除最早的一条消息

        self.messages.append({
            "role": "user",
            "content": input_text
        })

        assistant_reply = ""
        question, answer = brain_app.get_question_answer(input_text)
        if question and answer:
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            similarity = SequenceMatcher(None, question, input_text).ratio()
            print(similarity)
            if similarity > 0.7:
                assistant_reply = answer

        if assistant_reply == "":
            response = self.do_request(self.messages)
            if response is None:
                return "请求失败"
            assistant_reply = response["choices"][0]["message"]["content"]

        self.messages.append({
            "role": "assistant",
            "content": assistant_reply
        })
        print(assistant_reply)
        return assistant_reply


chatbot = Chatbot()


def chat(input_text):
    if input_text == "#reset":
        chatbot.messages.clear()
        return "重置成功"
    chatbot.chat(input_text)
    history = "\n\n".join([f"{m['role']}: {m['content']}" for m in chatbot.messages])
    return f"{history}"



iface = gr.Interface(fn=chat, inputs="text",outputs=gr.Textbox(lines=30,label="输出"), title="相亲对象", description="与相亲对象进行交流", show_progress="minimal")
iface.launch(server_name='10.234.129.125', server_port=7860)