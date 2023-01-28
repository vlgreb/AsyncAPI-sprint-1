import time

from elasticsearch import Elasticsearch

from tests.functional.settings import connection_settings

if __name__ == '__main__':

    es_client = Elasticsearch(hosts=[f'{connection_settings.es_host}:{connection_settings.es_port}'])

    while True:

        if es_client.ping():
            break
        time.sleep(1)
