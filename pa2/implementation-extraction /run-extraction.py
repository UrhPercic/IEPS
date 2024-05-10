import os
import argparse
from regex import regex_rtv_slo, regex_overstock, regex_pokedex
from xpath import xpath_rtv_slo, xpath_overstock, xpath_pokedex


def load_pages(path_to_dir, encoding="utf-8"):
    pages = []
    for file in os.listdir(path_to_dir):
        if file.endswith(".html"):
            with open(os.path.join(path_to_dir, file), "r", encoding=encoding) as f:
                html = f.read()
                pages.append(html)

    return pages


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("extraction_type", choices=["A", "B", "C"], type=str.upper, help="Type of extraction [A, B, C]")
    args = parser.parse_args()

    base_dir = os.path.join(os.getcwd(), '..','input-extraction')
    oversock_path = os.path.join(base_dir, 'overstock.com')
    rtv_path = os.path.join(base_dir, 'rtvslo.si')
    pokedex_path = os.path.join(base_dir, 'pokedex')

    oversock_pages = load_pages(oversock_path, encoding="windows-1252")
    rtv_pages = load_pages(rtv_path)
    pokedex_pages = load_pages(pokedex_path)

    if args.extraction_type == "A":
        for i, page in enumerate(rtv_pages):
            parsed_page_json = regex_rtv_slo(page)
            print(f"\n RTV page {i}: {parsed_page_json} \n")
        for i, page in enumerate(oversock_pages):
            parsed_page_json = regex_overstock(page)
            print(f"\n Overstock page {i}: {parsed_page_json} \n")
        for i, page in enumerate(pokedex_pages):
            parsed_page_json = regex_pokedex(page)
            print(f"\n Pokedex page {i}: {parsed_page_json} \n")
    elif args.extraction_type == "B":
        for i, page in enumerate(rtv_pages):
            parsed_page_json = xpath_rtv_slo(page)
            print(f"\n RTV page {i}: {parsed_page_json} \n")
        for i, page in enumerate(oversock_pages):
            parsed_page_json = xpath_overstock(page)
            print(f"\n Overstock page {i}: {parsed_page_json} \n")
        for i, page in enumerate(pokedex_pages):
            parsed_page_json = xpath_pokedex(page)
            print(f"\n Pokedex page {i}: {parsed_page_json} \n")
    elif args.extraction_type == "C":
        print("NOT IMPLEMENTED!")




