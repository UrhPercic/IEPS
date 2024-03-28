import mimetypes
import requests
from io import BytesIO
from urllib.parse import urljoin
import hashlib
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree

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

def fetch_robots_rules(domain):
    robots_url = f"http://{domain}/robots.txt"
    parser = RobotFileParser(robots_url)
    try:
        parser.read()
        delay = parser.crawl_delay("*")
        return parser, delay
    except Exception as e:
        print(f"Error fetching or parsing robots.txt for {domain}: {e}")
        return None, None


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
    elif 'application/pdf' in mime_type:
        return 'PDF'
    elif 'application/msword' in mime_type or 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in mime_type:
        return 'DOC'
    elif 'application/vnd.ms-powerpoint' in mime_type or 'application/vnd.openxmlformats-officedocument.presentationml.presentation' in mime_type:
        return 'PPT'
    else:
        return 'UNKNOWN'

def get_page_type(url):
    mime_type, _ = mimetypes.guess_type(url)
    if mime_type:
        return get_mime_type_category(mime_type)
    try:
        response = requests.head(url, timeout=10)
        if 'Content-Type' in response.headers:
            content_type = response.headers['Content-Type'].split(';')[0]
            return get_mime_type_category(content_type)
    except requests.RequestException:
        pass

    return 'UNKNOWN'

def hash_html_content(html_content):
    return hashlib.md5(html_content.encode('utf-8')).hexdigest()