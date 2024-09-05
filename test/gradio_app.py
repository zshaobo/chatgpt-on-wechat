import gradio as gr
import requests
import json
from difflib import SequenceMatcher


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
        self.messages.append({
            "role": "user",
            "content": input_text
        })

        response = self.do_request(self.messages)
        if response is None:
            return "请求失败"
        assistant_reply = response["choices"][0]["message"]["content"]
        print(response)
        if "knowledge_base" in response:
            knowledge_base_reply = response["knowledge_base"]["cites"][0]["content"]
            kb_parts = knowledge_base_reply.split('??', 1)

            if len(kb_parts) > 1:
                first_part = kb_parts[0].strip()

                similarity = SequenceMatcher(None, first_part, input_text).ratio()
                print(similarity)
                if similarity > 0.7:
                    assistant_reply = kb_parts[1].strip()

        self.messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

        return assistant_reply


chatbot = Chatbot()


def chat(input_text):
    if input_text == "#reset":
        chatbot.messages.clear()
        return "重置成功"
    chatbot.chat(input_text)
    history = "\n".join([f"{m['role']}: {m['content']}" for m in chatbot.messages])
    return f"{history}"



iface = gr.Interface(fn=chat, inputs="text",outputs=gr.Textbox(lines=30,label="输出"), title="相亲对象", description="与相亲对象进行交流", show_progress="minimal")
iface.launch(server_name='10.234.129.125', server_port=7860)