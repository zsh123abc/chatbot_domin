import requests
import json

# API服务的URL
API_URL = 'http://localhost:8080/chat/'
# 要发送给API的文本消息


user_text = "我是谁"

data = {
    "text": user_text,
}

# 发送POST请求到API
response = requests.post(API_URL, json=data)

# 检查响应状态码，如果是200则表示成功
if response.status_code == 200:
    # 解析JSON响应
    response_data = response.json()
    print("API响应:", response_data['response'][-1][-1][1])
else:
    print("请求失败，状态码:", response.status_code)
    print("响应内容:", response.text)
