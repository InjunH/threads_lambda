import requests
import json

url = "https://vasaqzveo8.execute-api.ap-northeast-2.amazonaws.com/dev"
payload = {
    "post_content": "오늘 사업자 모임 후기\n1. 스레드 이야기가 진짜 많이 나옴.."
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)