import requests
import lxml.html
from lxml import etree
from io import StringIO, BytesIO
import os
import logging
import random
import time


if __name__ == '__main__':

    baseurl = 'https://wikipedia.org'
    random_wiki = 'wiki/Special:Random'
    parser = etree.HTMLParser()
    logging.basicConfig(level=logging.INFO)
    while True:
        logging.debug('starting while loop')

        url = os.path.join(baseurl, *random_wiki.split('/'))
        logging.debug(f"joined url {url}")

        html = requests.get(url)
        logging.debug('sent request')

        tree = etree.parse(StringIO(html.text),parser)
        logging.debug('parsing string')


        title = tree.xpath('//h1[@id="firstHeading"]')[0].text
        logging.info(f"{title =}")

        paragraphs = tree.xpath('//div[@class="mw-parser-output"]/p')
        for index, paragraph in enumerate(paragraphs):
            # makes less text show up
            if index > 10:
                continue

            text = ''.join(paragraph.itertext())

            # makes less text show up
            if len(text) > 20:
                text = text[:20] + '...'

            print(text)
        print()


        links = tree.xpath('//div[@class="mw-parser-output"]/p/*/@href')
        random_wiki = random.choice(links)
        logging.debug(links)

        time.sleep(5)
