from django import forms
import requests
from environs import Env

# This is for loading environment variables from a .env file
env = Env()
env.read_env()


def send_code(phone_number, token):
    api_key = env("API_KEY")
    url = f"https://api.kavenegar.com/v1/{api_key}/verify/lookup.json"

    params = {
        "receptor": phone_number,
        "token": token,
        "template": "verify"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to send verification code: {response.text}"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}


class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(max_length=4, required=True)
