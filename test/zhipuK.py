from zhipuai import ZhipuAI




client = ZhipuAI(api_key="50fd0042b4254f7b834487a7e6426276.5EeZ3qaC9sBN0w1o") # 请填写您自己的APIKey

result = client.knowledge.query(
    page=1,
    size=10,
)
print(result)
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你好"},
    ],
    tools=[
            {
                "type": "retrieval",
                "retrieval": {
                    "knowledge_id": "1828039211614420992",
                    "prompt_template": "从文档\n\"\"\"\n{{knowledge}}\n\"\"\"\n中找问题\n\"\"\"\n{{question}}\n\"\"\"\n的一个答案，把你找到的问题和答案给出来，问题和答案用#做分割开，没有找到会回复没有"
                }
            }
            ],
    stream=False,
)
content = response.choices[0].message.content
print(content)# for chunk in response:
#     print(chunk.choices[0].delta)