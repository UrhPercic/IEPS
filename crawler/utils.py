import mimetypes
import requests
from io import BytesIO
from urllib.parse import urljoin

def get_content_type (image_url):
    content_type, _ = mimetypes.guess_type(image_url)
    if content_type:
        return content_type
    try:
        response = requests.head(image_url, timeout=10)
        if 'Content-Type' in response.headers:
            return response.headers['Content-Type']
    except requests.RequestException:
        pass

    return 'application/octet-stream'

def download_and_convert_image_to_binary(base_url, image_url):
    absolute_image_url = urljoin(base_url, image_url)
    try:
        response = requests.get(absolute_image_url)
        response.raise_for_status()
        return BytesIO(response.content).getvalue()
    except requests.RequestException as e:
        return None

def fetch_robots_content(domain):
    try:
        response = requests.get(f"http://{domain}/robots.txt", timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return None

def fetch_sitemap_content(domain):
    try:
        response = requests.get(f"http://{domain}/sitemap.xml", timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return None
