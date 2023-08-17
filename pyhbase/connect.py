#!/usr/bin/python
# -*- coding:UTF-8 -*-
from happybase import Connection


def get_hbase_connect():
    try:
        connection = Connection(host='node01', port=9090, timeout=3000000, table_prefix='pyhbase')
        return connection
    except Exception as exp:
        print(exp)
