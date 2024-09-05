import requests
import json


def get_question_answer(input_text):
    url = 'https://apiserverprod-nexuspy-ext-idc-ai.nie.netease.com/api/v1/docsets/@docset_1724830662327:chat'
    headers = {
        'X-Auth-User': '_dep375_bm_api_search',
        'X-Auth-Project': '_demo',
        'X-Access-Token': 'eyJhbGciOiJIUzI1NiIsImtpZCI6IjE3MjQ4MTkyMjEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3MjUwMDUzMzksImlzdCI6MTcyNDkxODkzOSwidXNlciI6Il9kZXAzNzVfYm1fYXBpX3NlYXJjaCJ9.KmONtzFy_z7SNmCsF3N4I9TALJOLtWC1owhQHaovMNs',
        # 替换为实际的Token
        'Content-Type': 'application/json'
    }
    data = {
        'input': input_text,
        'use_dataset_config': False
    }

    response = requests.post(url, headers=headers, json=data)

    # 解析响应内容
    response_json = response.json()
    print(response_json)
    # 提取 results 中的 Question 和 Answer
    for result in response_json.get('results', []):
        text = result.get('text', '')
        lines = text.split('\n')
        question = None
        answer = None
        for line in lines:
            if line.startswith('Question:'):
                question = line.replace('Question:', '').strip()
            elif line.startswith('Answer:'):
                answer = line.replace('Answer:', '').strip()
        if question and answer:
            return question, answer
    return None, None


# 示例调用
input_text = '不说算了'
question, answer = get_question_answer(input_text)
if question and answer:
    print(f"Question: {question}")
    print(f"Answer: {answer}")
else:
    print("No question and answer found.")