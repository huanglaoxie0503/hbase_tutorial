## happybase简介
 对happybase库的简单介绍如下:

HappyBase是一个Python库,提供了在HBase上进行操作的API。HBase是一个开源的、分布式的、面向列的NoSQL数据库,建立在Hadoop和Zookeeper之上。

HappyBase的主要功能包括:

- 连接和管理HBase数据库中的表
- 在表中进行增删改查操作,如创建、删除、获取和设置单元格的数据
- 支持对表进行扫描,通过过滤器来选择数据
- 支持表的批量put和get操作
- 支持在HBase表上进行MapReduce操作

HappyBase隐藏了HBase的复杂性,给用户提供了简单易用的Python API来操作HBase数据库。它的代码结构清晰简单,文档齐全,是在Python程序中访问HBase数据库的不错选择。

主要优点:

- API简单易用
- 良好的代码结构和文档
- 支持连接池提高性能
- 支持数据过滤和批处理

总体来说,HappyBase是一个轻量级但功能齐全的HBase Python客户端库,可以很好地帮助Python开发者访问和利用HBase数据库。
## happybase安装

1. 确保系统中已经安装了Python和pip
2. 使用pip安装happybase
```
pip install happybase
```
3. 如果系统中已经安装了HBase,则可以直接使用happybase连接，没安装的可以查看：[HBase集群安装教程](https://mp.weixin.qq.com/s?__biz=MzI0NjYzMDI0OA==&mid=2247485641&idx=1&sn=33746a5efb8c19cb0c580e60966ca358&chksm=e9bd1acedeca93d8f8fd9b6b822dba6a8b4f7ba43ba5c0dba89b77f04522de71abef08337819#rd)。
4. 启动/停止HBase数据库,常用的命令为:
```
# 启动HBase集群
$HBASE_HOME/bin/start-hbase.sh
# 停止HBase集群
$HBASE_HOME/bin/stop-hbase.sh
# 启动thrift
$HBASE_HOME/bin/hbase-daemon.sh start thrift
```
happybase的安装很简单,主要就是pip安装库,然后启动HBase数据库,之后就可以通过happybase提供的API来进行数据库操作了。
## API 
### happybase库的连接

`Connection`类用于连接HBase Thrift服务器。

#### 构造函数

```python
happybase.Connection(host=None, port=9090, timeout=None, autoconnect=True, 
                     table_prefix=None, table_prefix_separator='_', 
                     compat='0.96', transport='buffered', protocol='binary')
```

- `host` - HBase Thrift服务器主机名,默认为`localhost`
- `port` - HBase Thrift服务器端口,默认为`9090`
- `timeout` - 套接字超时时间(毫秒)
- `autoconnect` - 是否自动连接,默认为`True`  
- `table_prefix` - 表名前缀
- `table_prefix_separator` - 表名前缀分隔符,默认为`_`
- `compat` - 兼容模式,可选`'0.90'`, `'0.92'`, `'0.94'`, `'0.96'`(默认)
- `transport` - Thrift传输模式,可选`'buffered'`(默认), `'framed'`
- `protocol` - Thrift协议,可选`'binary'`(默认), `'compact'`

#### 主要方法

- `open()/close()` - 打开/关闭连接
- `tables()` - 获取所有表名
- `create_table()/delete_table()` - 创建/删除表
- `table()` - 返回一个Table对象用于操作表
- `is_table_enabled()` - 检查表是否存在

源码：
![](https://files.mdnice.com/user/3948/0ff5adf4-9fa7-4851-ad88-538190902f11.png)


### HBase 表操作

```python
def hbase_table_ddl(conn):
    """
    HBase数据库实例
    :param conn: Connection 对象
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
```
所以happybase通过简单的API就可以连接HBase并进行操作。
### HBase 数据操作
这里是一个使用HappyBase在HBase创建表格和进行数据操作的代码示例:

```python
def hbase_data_ddl(conn):
    """
    HBase表格实例
    :param conn: Connection 对象
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
```
这个示例演示了以下操作:

- 创建一个列族为"info"的HBase表格"student"
- 插入两行数据
- 获取一行数据
- 扫描全表并打印
- 删除一行数据

源码：

![](https://files.mdnice.com/user/3948/5612e439-dd87-4f20-ac28-ad4f73ddf0ac.png)

HappyBase让HBase的表格操作变得简单明了。我们只需要简单的API就可以进行构建表格、增删改查等操作。
### HBase 批量数据操作
```python
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
```
### send()方法什么时候用？
在HappyBase中,Batch对象的send()方法可以用来手动触发批处理操作的执行。

通常情况下,我们会使用"with"语句的上下文管理器来自动提交批处理:

```python
with table.batch() as b:
  b.put(...) 

# 退出上下文时会自动发送
```

但是有时我们需要手动控制批处理的发送,这时可以使用send()方法:

```python
b = table.batch()
b.put(...) 

# 手动发送
b.send() 

# 继续添加操作
b.put(...)
b.send()
```

send()方法会立即发送之前添加到批处理中的所有变更操作。

这样我们可以分多次调用发送批处理,手动控制发送的时机。

另外,发送完批处理后,可以继续往同一个批处理对象中添加新操作,之后再次发送。批处理对象可以重用。

需要注意的是,批处理对象必须在使用完后关闭:

```python
b.close() # 关闭批处理对象
```

总之,send()给了我们手动控制批处理发送的能力。结合上下文管理器,可以实现灵活的批量写入。
### ConnectionPool 
```python
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
```
### Major压缩
major压缩是一种列式存储数据库常用的压缩算法。

Major压缩的主要思想是:

1. 对值相同的连续列进行行合并,只存储一个值和这个值的重复次数。

2. 不存储重复值,对每个不同的值只存储一次,用长度字典来记录每种值的第一个位置。

3. 对长度字典使用位图索引进行编码,只存储开始位置的偏移量。

4. 使用通用压缩算法(如gzip)进一步压缩位图索引得到的字节流。

Major压缩的优点是:

- 对连续重复数据具有很高的压缩率
- 通过字典编码减少冗余
- 支持快速 locating,无需完全解压缩就能读取某列的数据

Major压缩的缺点是:

- 压缩和解压缩需要额外计算开销
- 对随机变化的数据压缩率不高

HBase、Cassandra等列式数据库广泛采用Major压缩来减少存储空间需求并提高查询性能。需要根据数据特征选择合适的压缩算法。