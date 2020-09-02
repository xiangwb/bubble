import requests
from bubble.config import USER_CENTER_URL


def get_user(user_id: str) -> dict:
    url = USER_CENTER_URL + '/api/v1/internal/users/' + user_id
    headers = {"Content-Type": "application/json"}
    timeout = 60
    response = requests.get(url,headers=headers,timeout=timeout).json()
    code = response.get('code')
    if code != 200:
        raise Exception("Not Found")
    return response['data']
