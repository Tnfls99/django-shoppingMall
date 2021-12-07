from shop.models import Good
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib

def get_detail(url):
        req = urlopen(url)
        soup = BeautifulSoup(req, 'html.parser')
        meta = soup.find('meta', {'property':'og:description'})
        if meta:
                detail = meta.get('content')
                return detail
        else:
                return False

def get_detail_img(url):
        req = urlopen(url)
        soup = BeautifulSoup(req, 'html.parser')
        meta = soup.find('meta', {'property':'og:image'})
        image = meta.get('content')
        return image
