#!/usr/bin/python
# -*- coding:UTF-8 -*-

from pyhbase.connect import get_hbase_connect


def hbase_table_ddl(conn):
    """
    HBase数据库实例
    :param conn:
    :return:
    """
    # 创建表
    families = {
        'cf1': dict(max_versions=10),
        'cf2': dict(max_versions=1, block_cache_enabled=False),
        'cf3': dict(),  # use defaults
    }
    conn.create_table(name='test_01', families=families)
    # 启用指定的表
    conn.enable_table(name='test_01')
    # 禁用指定的表
    conn.disable_table(name='test_01')
    # 指定的表是否已启用
    conn.is_table_enabled(name='test_01')
    # 压缩指定的表(是否执行major压缩)
    conn.compact_table(name='test_01', major=False)
    # 从HBase数据库中删除一张表格, 删除表之前需要先禁用表
    conn.delete_table(name='test_01', disable=True)
    # 返回此HBase实例中可用的表名列表, 如果 Connection 对象设置了“table_prefix”：py:class:“Connection”，则仅将列出具有指定前缀的表。
    table_list = conn.tables()
    print(table_list)
    # 返回一个表对象(是否使用表前缀)，返回的是对象，那么就可以做相应的操作
    tb_obj = conn.table(name='test_01', use_prefix=True)


def hbase_data_ddl(conn):
    """
    HBase表格实例
    :param conn:
    :return:
    """
    # 创建表格
    conn.create_table(
        'student',
        {'info': dict()}  # 一个列族info
    )
    # 获取表格对象
    table_obj = conn.table('student')
    # 插入数据
    table_obj.put('row1', {'info:name': 'Tom', 'info:age': '18'})
    table_obj.put('row2', {'info:name': 'Jerry', 'info:age': '20'})

    # 获取数据
    print(table_obj.row('row1'))

    # 扫描表格
    for key, data in table_obj.scan():
        print(key, data)

    # 删除数据
    table_obj.delete('row1')


def hbase_data_batch(conn):
    """
    HBase 批量数据操作
    :param conn:
    :return:
    """
    table = conn.table('student')
    # TODO 批量插入
    with table.batch() as b:
        b.put('row1', {'info:col1': 'value1'})
        b.put('row2', {'info:col1': 'value2'})

    # TODO 批量查询
    # 返回list
    rows_list = table.rows(['row1', 'row2'])
    print(rows_list)
    # 返回dict
    rows_dict = dict(table.rows(['row1', 'row2']))
    print(rows_dict)

    # TODO 批量删除
    with table.batch() as b:
        b.delete('row1')
        b.delete('row2')


if __name__ == '__main__':
    connect = get_hbase_connect()
    # 打开HBase数据库实例
    connect.open()

    hbase_table_ddl(conn=connect)

    hbase_data_ddl(conn=connect)

    hbase_data_batch(conn=connect)

    # 关闭HBase数据库实例
    connect.close()
