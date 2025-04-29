from django.core.cache import cache
import requests
from environs import Env

env = Env()
env.read_env()

def send_reservation_sms(phone_number, name, date):
    api_key = env("API_KEY")
    url = f"https://api.kavenegar.com/v1/{api_key}/verify/lookup.json"

    params = {
        "receptor": phone_number,
        "template": "finalr",
        "token10": name,
        "token": date,
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to send reserve sms: {response.text}"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}


def send_reminder_sms(phone_number, date, time):
    print(f"📨 در حال ارسال پیامک به {phone_number} برای تاریخ {date} ساعت {time}")
    api_key = env("API_KEY")
    url = f"https://api.kavenegar.com/v1/{api_key}/verify/lookup.json"

    params = {
        "receptor": phone_number,
        "template": "reminder",
        "token": date,
        "token2": time,
    }
    try:
        response = requests.get(url, params=params)
        print(f"📩 وضعیت پاسخ API: {response.status_code}")
        if response.status_code == 200:
            print(f"📨 پاسخ: {response.json()}")
            return {"success": response.json()}
        else:
            return {"error": f"Failed to send reminder sms: {response.text}"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}


def get_gold_price():
    prices = cache.get('live_prices')
    if not prices:
        try:
            response = requests.get('https://api.navasan.tech/latest/?api_key=freeZ9rqreIdClKOXPcoStwUfngCSQrR')
            if response.status_code == 200:
                data = response.json()
                prices = {
                    '18ayar': {
                        'value': int(data.get('18ayar', {}).get('value', 0)) * 1000,
                        'change': int(data.get('18ayar', {}).get('change', 0)) * 1000,
                    },
                    'abshodeh': {
                        'value': int(data.get('abshodeh', {}).get('value', 0)) * 1000,
                        'change': int(data.get('abshodeh', {}).get('change', 0)) * 1000,
                    },
                    'sekkeh': {
                        'value': int(data.get('sekkeh', {}).get('value', 0)) * 1000,
                        'change': int(data.get('sekkeh', {}).get('change', 0)) * 1000,
                    },
                    'gerami': {
                        'value': int(data.get('gerami', {}).get('value', 0)) * 1000,
                        'change': int(data.get('gerami', {}).get('change', 0)) * 1000,
                    }
                }
                cache.set('live_prices', prices, timeout=120)
        except:
            prices = None
    return prices
