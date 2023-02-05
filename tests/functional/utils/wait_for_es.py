import logging
import os
import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':

    es_host = os.getenv('ELASTIC_HOST', default='localhost')
    es_port = os.getenv('ELASTIC_PORT', default=6379)
    es_total_count = int(os.getenv('TOTAL_ITEMS_COUNT', 5191))

    es_client = Elasticsearch(
        hosts=[f'{es_host}:{es_port}'])

    while True:
        try:
            if es_client.ping():
                es_client.indices.refresh()
                if int(es_client.cat.count(format="json")[0]['count']) >= es_total_count:
                    break
            time.sleep(1)
        except Exception as exc:
            logging.error('elastic is not ready\n\t%s', exc)
