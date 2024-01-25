import os

BOT_NAME = 'pep_parse'
NEWSPIDER_MODULE = f'{BOT_NAME}.spiders'
SPIDER_MODULES = [NEWSPIDER_MODULE]

DOMAIN = 'peps.python.org'

ROBOTSTXT_OBEY = True

FEED_EXPORT_ENCODING = 'utf-8'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILE_FORMAT = 'csv'

FEEDS = {
    f'results/pep_%(time)s.{FILE_FORMAT}': {
        'format': FILE_FORMAT,
        'fields': ['number', 'name', 'status'],
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
