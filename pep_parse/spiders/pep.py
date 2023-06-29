import re
import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import PEP_DOC_DOMAIN, PEP_DOC_URL


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = (PEP_DOC_DOMAIN,)
    start_urls = [PEP_DOC_URL]

    # кортеж использовать нельзя. pytest невелит
    # В классе PepSpider для атрибута start_urls
    # установите список со значением https://peps.python.org/
    def parse(self, response):
        links = [
            info.css('a::attr(href)').get()
            for info in response.xpath('//*[@id="index-by-category"]').css(
                'tr'
            )
            if info.css('a::attr(href)').get() is not None
        ]

        for pep_link in links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        content = response.xpath('//*[@id="pep-content"]')
        pattern = r'PEP (?P<number>\d+) – (?P<name>.*)'
        pep_match = re.search(pattern, content.css('h1::text').get())

        data = {
            'number': int(pep_match.group('number')),
            'name': pep_match.group('name'),
            'status': content.css('dl').css('dd').css('abbr::text').get(),
        }
        yield PepParseItem(data)
