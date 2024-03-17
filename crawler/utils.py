import mimetypes
import requests

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
