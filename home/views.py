from .utils import get_gold_price
from django.shortcuts import render
from django.http import JsonResponse
from .models import Time
import jdatetime



def home(request):
    prices = get_gold_price()
    return render(request, 'home/home.html',{'prices':prices})

def reservation_api(request):
    reservations = Time.objects.all()
    events = [
        {
            'title': 'رزرو شده',
            'start': jdatetime.date.fromgregorian(date=res.shamsi_date).isoformat(),
            'color': 'red'
        }
        for res in reservations
    ]
    return JsonResponse(events, safe=False)



# def get_gold_price(request):
#
#     url = "https://BrsApi.ir/Api/Tsetmc/AllSymbols.php?key=FreeGKMTtKf3Z5xMtagk7SkrZXa5GUR5"
#
#
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
#         "Accept": "application/json, text/plain, */*"
#     }
#
#     try:
#         response = requests.get(url, headers=headers, timeout=5)
#         if response.status_code == 200:
#             return JsonResponse(response.json(), safe=False)
#         else:
#             return JsonResponse({
#                 "error": f"کد وضعیت: {response.status_code}",
#                 "detail": response.text
#             }, status=response.status_code)
#
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({
#             "error": "در دریافت اطلاعات مشکلی پیش آمده",
#             "detail": str(e)
#         }, status=500)

