from bs4 import BeautifulSoup
from urllib.parse import urljoin
def extract_links(html_content, current_page_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        link_url = a['href']
        full_link_url = urljoin(current_page_url, link_url)
        links.append((current_page_url, full_link_url))
    return links

def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return [img['src'] for img in soup.find_all('img', src=True)]
