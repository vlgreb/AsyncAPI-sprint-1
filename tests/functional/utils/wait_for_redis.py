import os
import time

from redis import Redis, exceptions

if __name__ == '__main__':

    redis_host = os.getenv('REDIS_HOST', default='localhost')

    redis = Redis(host=redis_host)

    while True:

        try:
            redis.ping()

        except exceptions.ConnectionError:
            time.sleep(1)

        else:
            break
