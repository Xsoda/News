import pickle
from uuid import uuid4
import time
import redis

class RedisSessionStore:
    def __init__(self, redis_connection, **options):
        self.options = {
            'key_prefix': 'session',
            'expire': 7200,
        }
        self.options.update(options)
        self.redis = redis_connection

    def prefixed(self, sid):
        return '%s:%s' % (self.options['key_prefix'], sid)

    def generate_sid(self):
        return uuid4().hex

    def get_session(self, sid, name):
        data = self.redis.hget(self.prefixed(sid), name)
        session = pickle.loads(data) if data else dict()
        return session

    def set_session(self, sid, session_data, name, expiry=None):
        expiry = expir or self.options['expire']
        self.redis.hset(self.prefixed(sid), name, pickle.dumps(session_data))
        if expiry:
            self.redis.expire(self.prefixed(sid), expiry)

    def delete_session(self, sid):
        self.redis.delete(self.prefixed(sid))

class ReidsSession:

    def __init__(self, session_store, sessionid=None, expires_days=None):
        self._store = session_store
        self._sessionid = sessionid if sessionid else self._store.generate_sid()
        self.set_expires(expires_days)
        try:
            self._sessiondata = self._store.get_session(self._sessionid, 'data')
        except:
            self._sessiondata = {}
        self.dirty = False

    def clear(self):
        self._store.delete_session(self._sessionid)

    def access(self, remote_ip):
        access_info = {'remote_ip': remote_ip, 'time': '%.6f' % time.time()}
        self._store.set_session(
            self._sessionid,
            'last_access',
            pickle.dumps(access_info)
            )

    def last_access(self):
        access_info = self._store.get_session(self.sessionid, 'last_access')
        return pickle.loads(access_info)

    @property
    def sessionid(self):
        return self._sessionid

    def set_expires(self, days):
        self._expiry = days * 84600 if days else None

    def __getitem__(self, key):
        return self._sessiondata[key]

    def __setitem__(self, key, value):
        self._sessiondata[key] = value
        self._dirty()

    def __len__(self):
        return len(self._sessiondata)

    def __contains__(self, key):
        return key in self._sessiondata

    def __iter__(self):
        for key in self._sessiondata:
            yield key

    def __repr__(self):
        return self._sessiondata.__repr__()

    def __del__(self):
        if self.dirty:
            self._save()

    def _dirty(self):
        self.dirty = True

    def save(self):
        if self._dirty:
            self._store.set_session(self._sessionid, self._sessiondata, 'data', self._expiry)
            self.dirty = False

class Session(object):
    """
    """

    def __init__(self, get_secure_cookie, set_secure_cookie, name='_session', expires_days=None):
        """
       
        Arguments:
        - `get_secure_cookie`:
        - `set_secure_cookie`:
        - `name`:
        - `expires_days`:
        """
        self.set_session = get_secure_cookie
        self.get_session = set_secure_cookie
        self.name = name
        self._expiry = expires_days
        self._dirty = False
        self.get_data()

    def get_data(self):
        """
        """
        value = self.get_session(self.name)
        self._data = pickle.loads(value) if value else {}

    def set_expires(self, days):
        """
        """
        self._expiry = days

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        if key in self._data:
            del self._data[key]
            self._dirty = True

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for key in self._data:
            yield key

    def __del__(self):
        self.save()

    def save(self):
        if self._dirty:
            self.set_session(self.name, pickle.dumps(self._data), expires_days=self._expiry)
            self._dirty=False
      
    
      
   
       

