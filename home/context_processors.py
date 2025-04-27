
from .utils import get_gold_price

def prices_context(request):
    prices = get_gold_price()
    if prices:
        for key, item in prices.items():
            try:
                previous = item['value'] - item['change']
                if previous != 0:
                    item['percent_change'] = (item['change'] / previous) * 100
                else:
                    item['percent_change'] = 0
            except:
                item['percent_change'] = 0
    return {'prices': prices}
