#!/usr/bin/python
# -*- coding:UTF-8 -*-
from happybase import ConnectionPool


def hbase_pool():
    pool = ConnectionPool(size=10, host='node01')

    # 创建表
    with pool.connection() as conn:
        conn.create_table('table_01', {'cf': dict()})

    #  # 插入数据
    with pool.connection() as connection:
        table = connection.table('table_01')

    with table.batch() as b:
        b.put('row1', {'cf:col1': 'value1'})

    # 更新数据
    with table.batch() as b:
        b.put('row1', {'cf:col2': 'value2'})

        # 删除数据
    with table.batch() as b:
        b.delete('row1')

    # 获取连接的上下文管理器
    with pool.connection() as connection:
        print(connection.tables())


if __name__ == '__main__':
    hbase_pool()
