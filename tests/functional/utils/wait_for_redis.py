from redis import Redis, exceptions
from tests.functional.settings import connection_settings

import time

if __name__ == '__main__':

    redis = Redis(host=connection_settings.redis_host)

    while True:

        try:
            redis.ping()

        except exceptions.ConnectionError:
            time.sleep(1)

        else:
            break
