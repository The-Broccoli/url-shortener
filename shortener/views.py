from django.shortcuts import render
from .models import Urls
import base64
import hashlib
from urllib.parse import urlparse
from django.http import JsonResponse

# Create your views here.
def shortener(request):
    if request.method == 'POST':
        # Request data auf vollständigkeit prüfen
        if is_valid_url(request.POST['url']):
            # Ist diese URL dem System schon bekannt?
            if it_is_a_known_url(request.POST['url']):
                short_url = generate_short_url(request.POST['url'])
                Urls.objects.create(long_url = request.POST['url'], short_url = short_url)
            else:
                print('known URL - Request data:', request.POST['url'])
                return JsonResponse({'error_message': 'A known URL'})
        else:
            print('Invalid URL - Request data:', request.POST['url'])
            return JsonResponse({'error_message': 'Invalid URL'})
    return render(request, 'shortener.html')

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def generate_short_url(long_url):
    hash_object = hashlib.sha1(long_url.encode())
    hex_dig = hash_object.hexdigest()
    decimal_hash = int(hex_dig, 16)
    short_url = base64.b64encode(str(decimal_hash).encode()).decode()
    return f'{short_url[:8]}'
    
def it_is_a_known_url(long_url):
    all_urls = Urls.objects.all()
    for url in all_urls:
        if long_url == url:
            return True
    return False