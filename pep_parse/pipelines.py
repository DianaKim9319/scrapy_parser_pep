import os
import csv
import datetime
from collections import Counter
from scrapy.spiders import Spider
from scrapy import Item

from .settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider: Spider) -> None:
        self.status_counter = Counter()

    def process_item(self, item: Item, spider: Spider) -> Item:
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider: Spider) -> None:
        current_datetime = datetime.datetime.now(
        ).strftime("%Y-%m-%dT%H-%M-%S")
        filename = os.path.join(
            BASE_DIR,
            'results',
            f'status_summary_{current_datetime}.csv'
        )

        with open(filename, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Статус', 'Количество'])
            for status, count in self.status_counter.items():
                writer.writerow([status, count])
            writer.writerow(['Total', sum(self.status_counter.values())])
