import requests
import json
from difflib import SequenceMatcher


def do_request(messages):
    url = "https://api.baichuan-ai.com/v1/chat/completions"
    api_key = "sk-86340cb476b9fbd5bf5406e72b202cd2"

    data = {
        "model": "Baichuan-NPC-Turbo",
        "character_profile": {
            "character_id": 31154
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
        "Authorization": "Bearer " + api_key
    }

    response = requests.post(url, data=json_data, headers=headers, timeout=60)

    if response.status_code == 200:
        # print("请求成功！")
        #print("响应body:", response.text)
        # print("请求成功，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
        return response.json()
    else:
        print("请求失败，状态码:", response.status_code)
        print("请求失败，body:", response.text)
        print("请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
        return None


if __name__ == "__main__":
    messages = [
        {
            "role": "user",
            "content": "你好，你是谁"
        }
    ]

    user_input=""
    while True:
        if len(messages) > 30:
            messages.pop(0)
            print("对话轮数超过30轮，删除最老的消息。")
        response = do_request(messages)
        if response is None:
            break

        assistant_reply = response["choices"][0]["message"]["content"]

        if "knowledge_base" in response:
            knowledge_base_reply = response["knowledge_base"]["cites"][0]["content"]
            # 将knowledge_base_reply按#分成两段
            kb_parts = knowledge_base_reply.split('？', 1)

            if len(kb_parts) > 1:
                first_part = kb_parts[0].strip()

                # 计算第一段与user_input的重复相似度
                similarity = SequenceMatcher(None, first_part, user_input).ratio()
                if similarity > 0.7:
                    print("匹配成功，将知识库中的答案作为回复")
                    print(f"相似度: {similarity:.2f}")
                    print("knowledge_base:", knowledge_base_reply)
                    print("user_input:", user_input)
                    assistant_reply = kb_parts[1].strip()
        print("assistant:", assistant_reply)

        print("----------------------------")
        messages.append({
            "role": "assistant",
            "content": assistant_reply
        })
        user_input = input("user:")
        messages.append({
            "role": "user",
            "content": user_input
        })
        # print(messages)