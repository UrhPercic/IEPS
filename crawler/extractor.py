from bs4 import BeautifulSoup
def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True)]

def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return [img['src'] for img in soup.find_all('img', src=True)]
