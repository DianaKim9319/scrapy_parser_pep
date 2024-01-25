import re
from urllib.parse import urljoin

import scrapy
from scrapy.http import Response

from pep_parse.items import PepParseItem
from pep_parse.settings import DOMAIN


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = [DOMAIN]
    start_urls = [f'https://{DOMAIN}/']

    def parse(self, response: Response) -> None:
        """
        Парсит URL всех PEP и переходит по ним.

        """
        all_peps = response.css('section[id="numerical-index"]')
        all_peps_links = all_peps.css(
            'a.pep.reference.internal::attr(href)'
        ).getall()
        for pep_link in all_peps_links:
            link = urljoin(response.url, pep_link)
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response: Response) -> PepParseItem:
        """
        Парсит такие данные, как "Номер", "Название" и "Статус"
        по каждиму PEP.

        """
        text = response.css('h1.page-title::text').get().strip()
        number = re.search(r'\d+', text).group()
        name = text.replace(f'PEP {number} – ', '')
        status = response.css('abbr::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
