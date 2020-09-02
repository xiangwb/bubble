import requests
from bubble.config import USER_CENTER_URL


def get_user(user_id: str) -> dict:
    url = USER_CENTER_URL + 'api/v1/internal/users/' + user_id
    response = requests.get(url).json()
    code = response.get('code')
    if code != 200:
        raise Exception("Not Found")
    return response['data']
