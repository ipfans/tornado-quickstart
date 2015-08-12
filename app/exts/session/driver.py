#!/usr/bin/env python
# coding=utf-8

# redis driver is not async redis client driver, if you want to imporve
# performace, you can change it to other async redis driver.

from __future__ import absolute_import

import redis
from copy import copy
from datetime import datetime
try:
    import cPickle as pickle    # py2
except:
    import pickle               # py3


class RedisSession(object):
    """
    Use Redis to save session object.
    """
    def __init__(self, **settings):
        self.settings = settings

    def get(self, session_id):
        self.__create_redis_client()
        session_data = self.client.get(session_id)
        if not session_data:
            return {}
        return pickle.loads(session_data)

    def save(self, session_id, session_data, expires=None):
        session_data = session_data if session_data else {}
        if expires:
            session_data.update(__expires__=expires)
        session_data = pickle.dumps(session_data)
        self.__create_redis_client()
        self.client.set(session_id, session_data)
        if expires:
            delta_seconds = int((expires - datetime.utcnow()).total_seconds())
            self.client.expire(session_id, delta_seconds)

    def clear(self, session_id):
        self.__create_redis_client()
        self.client.delete(session_id)

    def remove_expires(self):
        pass

    def __create_redis_client(self):
        if not hasattr(self, 'client'):
            if 'max_connections' in self.settings:
                connection_pool = redis.ConnectionPool(**self.settings)
                settings = copy(self.settings)
                del settings['max_connections']
                settings['connection_pool'] = connection_pool
            else:
                settings = self.settings
            self.client = redis.Redis(**settings)