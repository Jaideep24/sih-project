from django.http import JsonResponse
import requests
from .models import SiteSetting

def get_quote(request):
    # Get update interval from settings (not used here, but could be for caching)
    interval = SiteSetting.objects.first().quote_update_interval if SiteSetting.objects.exists() else 3600
    try:
        res = requests.get('https://zenquotes.io/api/random', timeout=5)
        data = res.json()
        quote = data[0]['q']
        author = data[0]['a']
        return JsonResponse({'quote': quote, 'author': author})
    except Exception:
        return JsonResponse({'quote': 'Unable to fetch quote.', 'author': ''})
