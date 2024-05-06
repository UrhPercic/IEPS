import time
from threading import Thread
from downloader import download_page
from extractor import extract_links, extract_images
from datastore import DataStore
from duplicate_detector import DuplicateDetector
from urllib.parse import urlparse
from utils import get_content_type, download_and_convert_image_to_binary, get_page_type, download_binary_content, hash_html_content, fetch_robots_rules

datastore = DataStore()
duplicate_detector = DuplicateDetector(datastore)

seed_urls = ["http://gov.si", "http://evem.gov.si", "http://e-uprava.gov.si", "http://e-prostor.gov.si"]
for url in seed_urls:
    domain = urlparse(url).netloc
    site_id = datastore.get_or_create_site_id(domain)
    if not datastore.check_page_exists(url):
        datastore.store_page(site_id, 'FRONTIER', url, None, None, None, None)

num_worker_threads = 6

robot_rules = {}
robot_delays = {}


def crawl():
    while True:
        frontier_pages = datastore.fetch_frontier_pages()
        frontier_pages_to_insert = []
        links_to_insert = []
        images_to_insert = []

        if not frontier_pages:
            time.sleep(5)
            continue

        for page_id, url in frontier_pages:
            domain = urlparse(url).netloc
            site_id = datastore.get_or_create_site_id(domain)

            if domain not in robot_rules or domain not in robot_delays:
                robot_rules[domain], robot_delays[domain] = fetch_robots_rules(datastore, domain)

            if not robot_rules[domain] or robot_rules[domain].can_fetch("*", url):
                time.sleep(robot_delays[domain])

            content, status_code = download_page(url)

            if content is not None and status_code == 200:
                page_type = get_page_type(url)

                if page_type == 'HTML' or page_type == 'UNKNOWN':
                    if not duplicate_detector.is_duplicate(content):
                        html_hash = hash_html_content(content)
                        datastore.update_page_status(page_id, 'HTML', content, status_code, time.strftime('%Y-%m-%d %H:%M:%S'), html_hash)

                        images = extract_images(content)
                        for image_url in images:
                            content_type = get_content_type(image_url)
                            image_data = download_and_convert_image_to_binary(url, image_url)
                            truncated_image_url = image_url[:255]
                            images_to_insert.append((page_id, truncated_image_url, content_type, image_data, time.strftime('%Y-%m-%d %H:%M:%S')))

                        link_tuples = extract_links(content, url)
                        for _, link_url in link_tuples:
                            canonicalized_link_url = duplicate_detector.canonicalize(link_url)
                            frontier_pages_to_insert.append((site_id, 'FRONTIER', canonicalized_link_url, None, None, None, None))
                            links_to_insert.append((page_id, canonicalized_link_url))
                    else:
                        datastore.update_page_status(page_id, 'DUPLICATE', None, status_code, time.strftime('%Y-%m-%d %H:%M:%S'), None)
                else:
                    datastore.update_page_status(page_id, 'BINARY', None, status_code, time.strftime('%Y-%m-%d %H:%M:%S'), None)


        inserted_frontier_pages = datastore.store_pages_bulk(frontier_pages_to_insert)
        if inserted_frontier_pages:
            url_to_page_id = {url: page_id for page_id, url in inserted_frontier_pages}
        else:
            url_to_page_id = {}
        links_to_insert_final = [(from_page_id, url_to_page_id[url]) for from_page_id, url in links_to_insert if url in url_to_page_id]
        datastore.store_links_bulk(links_to_insert_final)

        if images_to_insert:
            datastore.store_images_bulk(images_to_insert)


def start_crawling():
    threads = []
    for i in range(num_worker_threads):
        thread = Thread(target=crawl)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    start_crawling()