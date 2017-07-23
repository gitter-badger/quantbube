# encoding:utf-8
import logging

import msgpack
import redis

from .base import BaseConnection
from quantbube.timeseries import serializer

logger = logging.getLogger(__name__)


class RedisException(Exception):
    """
    redis Exception
    """
    pass


class RedisStore(BaseConnection):
    """
    Redis to save time-series data
    """
    serializer_class = serializer.BaseSerializer

    def __int__(self, structure, url=None, db=None, **kwargs):
        """
        :param url:
        :param db:
        :param kwargs:
        :return:
        """
        if url:
            pool = redis.ConnectionPool.from_url(url=url, db=db, **kwargs)
            self.conn = redis.StrictRedis(connection_pool=pool)
        else:
            self.conn = redis.StrictRedis(**kwargs)

    def _pipeline(self):
        """
        wrapper the pipeline execute
        :return:
        """
        pipe_needed = not isinstance(self.redis, BasePipeline)
        if pipe_needed:
            pipe = self.redis.pipeline(transaction=False)
            operation(pipe, *args, **kwargs)
            results = pipe.execute()
        else:
            results = operation(self.redis, *args, **kwargs)
        return results
        pass

    def set(self, name, timestamp, expired=None, **data):
        """

        :param name:
        :param timestamp:
        :param expired:
        :param data:
        :return:
        """

        pipe = self.conn.pipeline(transaction=True)
        pipe.zadd(name, timestamp, str(data))

        pipe.execute()

    def get(self, name, start_timestamp, end_timestamp):
        """
        :return:
        """
        pipe = self.conn.pipeline(transaction=True)
        pipe.zrange(name, start_timestamp, end_timestamp, withscores=True)

        result = pipe.execute()
        return result

    def contains(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def get_slice(self, key, start=None, end=None, ordering=None, *args, **kwargs):
        """
        :param key:
        :param start:
        :param end:
        :param ordering:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def remove_many(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def add_many(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def all(self, name):
        pipe = self.conn.pipeline(transaction=True)

        pipe.zrange(name, 0, -1, withscores=True)
        result = pipe.execute()
        return result

    def delete(self):
        """
        :return:
        """

    def iter(self):
        """
        :return:
        """
