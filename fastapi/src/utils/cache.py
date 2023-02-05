import functools
import logging

import orjson


def cache(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):

        key = self._get_key(*args, **kwargs)

        if data := await self._cache.get(key=key):
            logging.info('[%s] get data from cache', type(self).__name__)
            return orjson.loads(data)

        if data := await func(self, *args, **kwargs):
            logging.info('[%s] get data from elastic', type(self).__name__)
            await self._cache.save(key=key, value=orjson.dumps(data))
            logging.info('[%s] put data to cache', type(self).__name__)
            return data

        logging.info("[%s] can't find item in elastic", type(self).__name__)
        return None

    return wrapper
