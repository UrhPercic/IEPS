import requests

def download_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text, response.status_code
    except requests.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return None, None
