import logging
import os

import backoff
from elasticsearch import Elasticsearch, ElasticsearchException


def elastic_conn_backoff_hdlr(details):
    logging.warning(
        "\t\n ==> Elastic connection Error. "
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "Details: {args}".format(**details))


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=ElasticsearchException,
    on_backoff=elastic_conn_backoff_hdlr,
    max_tries=10
)
def check_elastic_connection():

    es_host = os.getenv('ELASTIC_HOST', default='localhost')
    es_port = os.getenv('ELASTIC_PORT', default=6379)
    es_total_count = int(os.getenv('TOTAL_ITEMS_COUNT', 5191))

    es_client = Elasticsearch(
        hosts=[f'{es_host}:{es_port}'])

    if es_client.ping():

        if int(es_client.cat.count(format="json")[0]['count']) < es_total_count:
            raise ElasticsearchException("Not enough data for testing. Wait for ETL finish loading...")

    else:
        raise ElasticsearchException("Elastic server is not available")


if __name__ == '__main__':
    check_elastic_connection()
