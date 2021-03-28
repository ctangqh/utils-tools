#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(acstime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class MysqlUtil(object):
    '''
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'charset': 'utf8',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    '''

    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.passwd = config['passwd']
        self.db = config['db']
        self.charset = config['charset']
        self.config = config
        self.conn = None
        self.cur = None

    def __del__(self):
        self.close()

    def open(self):
        try:
            self.conn = pymysql.connect(**self.config)
            self.conn.autocommit(1)
            self.cur = self.conn.cursor()
        except Exception as err:
            logging.error('database connect error,please check the config.\n%s' % err)

    def close(self):
        try:
            self.conn.close()
        except Exception as err:
            logging.error('database connect error,please check the config.\n%s' % err)

    def get_version(self):
        return self.get_one('SELECT VERSION()')

    def get_one(self, sql, params=None):
        res = None
        try:
            if params is not None:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            res = self.cur.fetchone()
            logging.debug('query sql [%s]' % sql)
        except Exception as err:
            logging.error('fetch one data error.\n%s' % err)

    def get_all(self, sql, params=None):
        res = None
        try:
            if params is not None:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            res = self.cur.fetchall()
            logging.debug('query sql [%s]' % sql)
        except Exception as err:
            logging.error('fetch one data error.\n%s' % err)

    def __execute(self, sql, params=None):
        count = 0
        try:
            if params is not None:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            count = self.db.commit()
            logging.debug('execute sql [%s]\nreturn [%s]' % (sql, count))
        except Exception as err:
            logging.error('execute sql[%s] error.\n%s' % (sql, err))

    def save(self, sql, params=None):
        return self.__execute(sql, params)

    def update(self, sql, params=None):
        return self.__execute(sql, params)

    def delete(self, sql, params=None):
        return self.__execute(sql, params)
