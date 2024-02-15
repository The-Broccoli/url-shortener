from django.shortcuts import render, redirect
from .models import Urls
import base64
import hashlib
from urllib.parse import urlparse
from django.http import JsonResponse

DOMAIN = "https://www.istfy.de/"

def shortener(request):
    if request.method == 'POST':
        json = {}
        if is_valid_url(request.POST['url']):
            link = it_is_a_known_url(request.POST['url'])
            if not link:
                short_url = generate_short_url(request.POST['url'])
                Urls.objects.create(long_url = request.POST['url'], short_url = short_url)
                json['success_message'] = 'Link was copied to Clipboard'
                json['short_url'] = DOMAIN + short_url
                return JsonResponse(json)
            else:
                # print('known URL - Request data:', request.POST['url'])
                json['success_message'] = 'A known URL'
                json['short_url'] = DOMAIN + link
                return JsonResponse(json)
        else:
            # print('Invalid URL - Request data:', request.POST['url'])
            return JsonResponse({'error_message': 'Invalid URL'})
    return render(request, 'shortener.html')

def forward(request, exception):
    result = does_this_forwarding_exist(request.path[1:])
    if result:
        return redirect(result)
    else:
        return render(request, '404.html')

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
        if long_url == url.long_url:
            return url.short_url
    return False
    
def does_this_forwarding_exist(hex_code):
    all_urls = Urls.objects.all()
    for url in all_urls:
        if hex_code == url.short_url:
            return url.long_url
    return False