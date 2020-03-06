# -*- coding: UTF-8 -*-
from daily_commute import dbha


class ModelDatabaseRouter(object):

    def db_for_read(self, model, **hints):
        """Point all read operations to our available dbms server"""
        return dbha.available_db()

    def db_for_write(self, model, **hints):
        """Point all write operations to our available dbms server"""
        return dbha.available_db()
