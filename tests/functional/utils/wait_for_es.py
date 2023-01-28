import time

from tests.functional.settings import connection_settings


from elasticsearch import Elasticsearch

if __name__ == '__main__':

    es_client = Elasticsearch(hosts=connection_settings.es_host, validate_cert=False, use_ssl=False)

    while True:

        if es_client.ping():
            break
        time.sleep(1)
