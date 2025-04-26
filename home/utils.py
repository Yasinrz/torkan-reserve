import requests
from environs import Env

env = Env()
env.read_env()


def send_reservation_sms(phone_number, name, date):
    api_key = env('API_KEY')
    url = f"https://api.kavenegar.com/v1/{api_key}/verify/lookup.json"

    params = {
        "receptor": phone_number,
        "template": "finalr",  # اسم قالب
        "token": name,  # نام کاربر
        "token2": date,  # تاریخ رزرو
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to send reserve sms: {response.text}"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}
