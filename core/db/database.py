#*-*coding: utf-8*-*
#!/usr/bin/env python

__author__ = 'Xsoda'
import copy
import psycopg2
import itertools
import logging
import time

class Connection(object):
    """
    """

    def __init__(self, host, database, user=None, password=None, max_idle_time=7*3600):
        """
        """
        self.host = host
        self.database = database
        self.max_idle_time = max_idle_time

        args = dict(database=database)

        if user is not None:
            args['user'] = user
        if password is not None:
            args['password'] = password

        self.socket = None
        pair = host.split(':')
        if len(pair) == 2:
            args['host'], args['port'] = pair[0], int(pair[1])
        else:
            args['host'], args['port'] = host, 5432

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to Postgresql on %s", self.host, exc_info=True)

    def __del__(self):
        """ Closes this database connection.            
        """
        if getattr(self, '_db', None) is not None:
            self._db.close()
            self._db = None

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """ Closes the existing database connection and re-opens is.                  """
        self.close()
        self._db = psycopg2.connect(**self._db_args)
        self._db.set_session(autocommit=True)        

    def query(self, query, *parameters):
        """ Returns a row list for the given query and parameters.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.zip_longest(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters):
        """ Returns the first row returned for the given query.
        """
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    # revcount is a more reasonable default return value than lastrwid,
    # bu for historical compatibility execute() must return lastrowid.
    def execute(self, query, *parameters):
        """ Execute the given query, returning the lastrowid from the query.
        """
        return self.execute_lastrowid(query, *parameters)

    def execute_lastrowid(self, query, *parameters):
        """ Execute the given query, returning the lastrowid form the query.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters):
        """ Execute the given query, returning the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """ Execute the given query against all the given param sequences.
        We teturn the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)
    
    def executemany_lastrowid(self, query, parameters):
        """ Execute the given query against all the given param sequences.
        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """ Execute the given query against all the given param sequences.
        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return corsor.rowcount
        finally:
            cursor.close()

    def _ensure_connected(self):
        if (self._db is not None or
            (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters):
        try:
            print(query, parameters)
            return cursor.execute(query, parameters)
        except OperationalError:
            logging.error("Error connection to Postgresql on %s", self.host)
            self.close()
            raise

class Row(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
    
OperationalError = psycopg2.OperationalError
IntegrityError = psycopg2.IntegrityError
