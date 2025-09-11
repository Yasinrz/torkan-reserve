import requests
from environs import Env

# This is for loading environment variables from a .env file
env = Env()
env.read_env()


def send_location(name, messege, created_at ,phone):
    api_key = env("API_KEY")
    url = f"https://api.kavenegar.com/v1/{api_key}/verify/lookup.json"

    params = {
        "receptor":phone,
        "template": "locatin",
        "token10": name,
        "token": created_at,
        "token20": messege,
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to send request reserve sms: {response.text}"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}