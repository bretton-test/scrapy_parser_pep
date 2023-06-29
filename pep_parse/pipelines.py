import csv
import datetime as dt
from dataclasses import dataclass
from collections import Counter

from pep_parse.settings import DATETIME_FORMAT, BASE_DIR


@dataclass()
class Pep:
    number: int
    name: str
    status: str


def save_to_csv(results):
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    file_path = results_dir / f'status_summary_{now_formatted}.csv'
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)


class PepParsePipeline:
    def __init__(self):
        self.peps = None

    def open_spider(self, spider):
        self.peps = {}

    def process_item(self, item, spider):
        self.peps[item['number']] = Pep(**item)
        return item

    def close_spider(self, spider):
        results = [('Статус', 'Количество')]
        statuses = sorted([item.status for item in self.peps.values()])
        for key, value in Counter(statuses).items():
            results.append((key, str(value)))

        results.append(('Total ', str(len(self.peps))))
        save_to_csv(results)
