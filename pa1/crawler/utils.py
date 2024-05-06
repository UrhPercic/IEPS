import mimetypes
import requests
from io import BytesIO
from urllib.parse import urljoin
import hashlib
from urllib.robotparser import RobotFileParser

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


def fetch_robots_rules(datastore, domain):
    robots_content = datastore.get_robots_content(domain)
    parser = RobotFileParser()

    if robots_content is not None:
        parser.parse(robots_content.splitlines())
    else:
        parser.allow_all = True

    delay = parser.crawl_delay("*") or 1
    return parser, delay


def download_binary_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error downloading binary content from {url}: {e}")
        return None

def get_mime_type_category(mime_type):
    if 'text/html' in mime_type:
        return 'HTML'
    elif any(sub_type in mime_type for sub_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                                    'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']):
        return 'BINARY'
    else:
        return 'UNKNOWN'

def get_page_type(url):
    try:
        response = requests.get(url)
        content_type = response.headers['Content-Type']
        page_type = get_mime_type_category(content_type)
        return page_type
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def hash_html_content(html_content):
    return hashlib.md5(html_content.encode('utf-8')).hexdigest()