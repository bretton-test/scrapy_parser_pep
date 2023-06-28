from pathlib import Path


BOT_NAME = 'pep_parse'
SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    'results/pep_%(time)s.csv': {
        # Формат файла.
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True,
    },
}
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PEP_DOC_URL = 'https://peps.python.org/'
PEP_DOC_DOMAIN = 'peps.python.org'
BASE_DIR = Path(__file__).parents[1]
