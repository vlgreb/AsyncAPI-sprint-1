import logging
import os

import backoff
from redis import Redis, exceptions


def redis_conn_backoff_hdlr(details):
    logging.info(
     "\t\n ==> Redis connection Error. "
     "Backing off {wait:0.1f} seconds after {tries} tries "
     "Details: {args}".format(**details))


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=exceptions.ConnectionError,
    on_backoff=redis_conn_backoff_hdlr,
    max_tries=10
)
def check_redis_connection():
    redis_host = os.getenv('REDIS_HOST', default='localhost')
    redis = Redis(host=redis_host)
    redis.ping()


if __name__ == '__main__':
    check_redis_connection()
