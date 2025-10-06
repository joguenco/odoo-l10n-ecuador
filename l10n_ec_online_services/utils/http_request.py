import requests


def make_api_request(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Odoo/18.0",
    }
    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code == 200:
        return response.json()
    else:
        return False
