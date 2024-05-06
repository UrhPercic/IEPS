from lxml import etree
import json


def xpath_overstock(target_html):
    root = etree.HTML(target_html)

    titles = root.xpath('//td[@valign="top"]/a/b/text()')
    list_prices = root.xpath('//td[@align="left" and @nowrap="nowrap"]/s/text()')
    prices = root.xpath('//td[@align="left" and @nowrap="nowrap"]/span[@class="bigred"]/b/text()')
    savings = root.xpath('//td[@align="left" and @nowrap="nowrap"]/span[@class="littleorange"]/text()')
    saving_percentage = [0 for _ in range(len(savings))]
    for i in range(len(savings)):
        saving_percentage[i] = savings[i].split()[1]
        savings[i] = savings[i].split()[0]
    contents = root.xpath('//span[@class="normal"]/text()')

    objects = [{"title": titles[i],
                "list_price": list_prices[i],
                "price": prices[i],
                "saving": savings[i],
                "saving_percentage": saving_percentage[i],
                "content": contents[i].replace('\n', ' ')} for i in range(len(titles))]

    return json.dumps(objects, indent=4, ensure_ascii=False)


def xpath_rtv_slo(target_html):
    root = etree.HTML(target_html)

    author = root.xpath('//div[@class="author-name"]/text()')[0]
    published_time = root.xpath('//div[@class="publish-meta"]/text()')[0].strip()
    title = root.xpath('//h1/text()')[0]
    subtitle = root.xpath('//div[@class="subtitle"]/text()')[0]
    lead = root.xpath('//p[@class="lead"]/text()')[0]
    content = root.xpath('//article[@class="article"]//p/text()')

    return json.dumps({
        'author': author,
        'published_time': published_time,
        'title': title,
        'subtitle': subtitle,
        'lead': lead,
        'content': content
    }, indent=4, ensure_ascii=False)


def xpath_pokedex(target_html):
    root = etree.HTML(target_html)

    name = root.xpath('//div[@class="pokedex-pokemon-pagination-title"]/div/text()')[0].strip()
    number = root.xpath('//div[@class="pokedex-pokemon-pagination-title"]/div/span/text()')[0]
    description = root.xpath('//div[@class="version-descriptions active"]/p/text()')[0].strip()
    height = root.xpath('//div/div/ul/li[span=\'Height\']/span/following-sibling::span[1]/text()')[0]
    weight = root.xpath('//div/div/ul/li[span=\'Weight\']/span/following-sibling::span[1]/text()')[0]
    category = root.xpath('//div/div/ul/li[span=\'Category\']/span/following-sibling::span[1]/text()')[0]
    type = root.xpath('//div/div/h3[contains(text(), "Type")]/following-sibling::ul/li/a/text()')
    weaknesses = root.xpath('//div/div/h3[contains(text(), "Weaknesses")]/following-sibling::ul/li/a/span/text()')

    type = list(set([type.strip() for type in type]))
    weaknesses = list(set([weakness.strip() for weakness in weaknesses]))

    return json.dumps({
        'name': name,
        'number': number,
        'description': description,
        'height': height,
        'weight': weight,
        'category': category,
        'type': type,
        'weaknesses': weaknesses
    }, indent=4, ensure_ascii=False)





