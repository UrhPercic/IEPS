import json
import re


def regex_overstock(target_html):
    titles = re.findall(r'<td valign="top">[\s\n]*.+?\s*<b>(.*?)\s*</b></a>', target_html)
    list_prices = re.findall(r'<b>\s*List Price:\s*</b>\s*.+?\s*<s>\s*(.*?)\s*</s>', target_html)
    prices = re.findall(r'<b>\s*Price:\s*</b>\s*.+?\s*<b>\s*(.*?)\s*</b>', target_html)
    savings = re.findall(r'<b>\s*You Save:\s*</b>\s*.+?\s*<span class="littleorange">\s*(.*?)\s\s*.+?\s*</span>', target_html)
    savings_percentage = re.findall(r'<b>\s*You Save:\s*</b>\s*.+?\s*<span class="littleorange">\s*.+?\s*\s(.+?)\s*</span>', target_html)
    contents = re.findall(r'<span class="normal">\s*([\S\s]*?)\s*(?=<br>)', target_html)

    objects = [{"title": titles[i],
                "list_price": list_prices[i],
                "price": prices[i],
                "saving": savings[i],
                "saving_percentage": savings_percentage[i],
                "content": contents[i].replace('\n', ' ')} for i in range(len(titles))]

    return json.dumps(objects, indent=4, ensure_ascii=False)


def regex_rtv_slo(target_html):
    author_search = re.search(r'<div class="author-name">\s*(.*?)\s*</div>', target_html)
    published_time_search = re.search(r'<div class="publish-meta">\s*(.*?)\s*<br>', target_html)
    title_search = re.search(r'<title>\s*(.*?)\s*</title>', target_html)
    subtitle_search = re.search(r'<div class="subtitle">\s*(.*?)\s*</div>', target_html)
    lead_search = re.search(r'<p class="lead">\s*(.*?)\s*</p>', target_html)
    content_search = re.search(
        r'<article class="article">[\S\s]*?<p[^>]*>(.*?)</p>[\s\n\t]*(?:\t|<figure class="mceNonEditable c-figure-full">)',
        target_html)

    author = author_search.group(1) if author_search else None
    published_time = published_time_search.group(1) if published_time_search else None
    title = title_search.group(1) if title_search else None
    subtitle = subtitle_search.group(1) if subtitle_search else None
    lead = lead_search.group(1) if lead_search else None

    # Da se znebimo vseh dodatnih znakov v matchu, ker je ceu content samo ena vrsta
    content = re.sub(r'<.*?>|[\n\t]*', '', content_search.group(1))

    return json.dumps({
        'author': author,
        'published_time': published_time,
        'title': title,
        'subtitle': subtitle,
        'lead': lead,
        'content': content
    }, indent=4, ensure_ascii=False)


def regex_pokedex(target_html):
    name = re.search(r'<div>[\s\n]*(.*?)[\s\n]*<span class="pokemon-number">', target_html)
    number = re.search(r'<span class="pokemon-number">\s*(.*?)\s*</span>', target_html)
    description = re.search(r'<p class="version-y[\s\n]*">\s*(.*?)[\s\n]*</p>', target_html)
    height = re.search(r'<span class="attribute-title">\s*Height\s*</span>[\s\n]*<span class="attribute-value">\s*(.*?)\s*</span>', target_html)
    weight = re.search(r'<span class="attribute-title">\s*Weight\s*</span>[\s\n]*<span class="attribute-value">\s*(.*?)\s*</span>', target_html)
    category = re.search(r'<span class="attribute-title">\s*Category\s*</span>[\s\n]*<span class="attribute-value">\s*(.*?)\s*</span>', target_html)
    type = re.findall(r'<h3\s*.*?>Type</h3>[\s\n\t]*<ul>[\s\n\t]*<li class="background-color-.*?">[\s\n\t]*<a href="https://www.pokemon.com/us/pokedex/\?type=.*?">\s*(.*?)\s*</a>', target_html)
    weaknesses = re.findall(r'<h3\s*.*?>Weaknesses</h3>[\s\n\t]*<ul>[\s\n\t]*<li class="background-color-.*?">[\s\n\t]*<a href="https://www.pokemon.com/us/pokedex/\?weakness=.*?">[\s\n\t]*<span>\s*(.*?)[\s\n\t]*</span>', target_html)

    # r'<h3\s*.*?>Type</h3>[\s\n\t]*<ul>[\s\n\t]*<li class="background-color-.*?">[\s\n\t]*<a href="https://www.pokemon.com/us/pokedex/\?type=.*?">\s*(*.?)\s*</a>'
    # r'<h3\s*.*?>Weaknesses</h3>[\s\n\t]*<ul>[\s\n\t]*<li class="background-color-.*?">[\s\n\t]*<a href="https://www.pokemon.com/us/pokedex/\?weakness=.*?">[\s\n\t]*<span>\s*(.*?)[\s\n\t]*</span>'

    name = name.group(1) if name else None
    number = number.group(1) if number else None
    description = description.group(1) if description else None
    height = height.group(1) if height else None
    weight = weight.group(1) if weight else None
    category = category.group(1) if category else None

    return json.dumps({
        "name": name,
        "number": number,
        "description": description,
        "height": height,
        "weight": weight,
        "category": category,
        "type": type,
        "weaknesses": weaknesses
    }, indent=4, ensure_ascii=False)
