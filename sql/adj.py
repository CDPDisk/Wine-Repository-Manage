# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:29:28 2019

@author: XIAOMI
"""
import sqlite3
import os

"""

"""


class make_record():
    def __init__(self, table, **kw):
        self.data = None
        self.primary = None
        self.table = table
        if table == 'base':
            self.data = self.make_wine_kw(**kw)
            self.primary = 'wine_id'
        elif table == 'score':
            self.data = self.make_score_kw(**kw)
            self.primary = 'wine_id'
        elif table == 'store':
            self.data = self.make_store_kw(**kw)
            self.primary = 'store_id'

        self.data.pop('self')

    def make_wine_kw(self, wine_id='auto',
                     wine_type=None,
                     wine_num=0,
                     store_id=None):
        return locals()

    def make_score_kw(self, wine_id=None,
                      appear_clarity=None,
                      appear_tone=None,
                      appear_pureness=None,
                      aroma_pureness=None,
                      aroma_concentration=None,
                      aroma_quality=None,
                      taste_pureness=None,
                      taste_concentration=None,
                      taste_persistence=None,
                      taste_quality=None):
        return locals()

    def make_store_kw(self, store_id='auto',
                      store_address=None,
                      store_temperature=None,
                      store_moisture=None):
        return locals()


def make_command(operation, table, record):
    data = record.data
    if operation == "insert":
        field = data.keys()
        block1 = ','.join(field)
        block2 = ','.join(list('?' * len(field)))
        command = 'insert into ' +\
            table +\
            ' (%s)' % (block1) +\
            ' values(%s)' % (block2)
    elif operation == 'update':
        field = data.keys()
        value = data.values()
        block1 = str(','.join(list(map(lambda a, b: str(a) + '=' + "'%s'" % str(b),
                                       field, value))))
        block1 = block1.replace("'None'", 'null')
        command = 'update ' +\
            table +\
            ' set ' +\
            block1 +\
            ' where %s==%s' % (record.primary, data[record.primary])
    elif operation == 'delete':
        command = 'delete from ' +\
            table + ' where ' + \
            '%s==%s' % (record.primary, data[record.primary])

    return command


class wine():
    def __init__(self, file='test.db'):
        # 初始化创建表，如果表存在则跳过
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()
        base_keys = ['wine_id', 'wine_type', 'wine_num', 'store_id']
        base_keys_CH = ['酒编号', '酒类型', '数量', '存储仓库编号']
        score_keys = ['wine_id', 'appear_clarity', 'appear_tone', 'appear_pureness',
                      'aroma_pureness', 'aroma_concentration', 'aroma_quality',
                      'taste_pureness', 'taste_concentration', 'taste_persistence', 'taste_quality']
        score_keys_CH = ['酒编号', '外观澄清度', '外观色调', '外观纯正度',
                         '香气纯正度', '香气浓度', '香气质量',
                         '口感纯正度', '口感浓度', '口感持久性', '口感质量']
        store_keys = ['store_id', 'store_address',
                      'store_temperature', 'store_moisture']
        store_keys_CH = ['仓库编号', '地址',
                         '温度', '湿度']
        self.keys = {'score': score_keys,
                     'base': base_keys,
                     'store': store_keys}
        self.keys_CH = {'score': score_keys_CH,
                        'base': base_keys_CH,
                        'store': store_keys_CH}
        try:
            self.cursor.execute('create table store\
                                (\
                                    store_id varchar(20) not null primary key,\
                                    store_address varchar(20) not null,\
                                    store_temperature real,\
                                    store_moisture real\
                                )')
        except:
            print("Error create store")
            pass
        try:
            self.cursor.execute('create table base\
                                (\
                                    wine_id varchar(20) not null primary key,\
                                    wine_type varchar(20) not null,\
                                    wine_num int not null,\
                                    store_id varchar(20) not null,\
                                    foreign key(store_id) references store(store_id)\
                                )')
        except:
            print("Error create base")
            pass

        try:
            self.cursor.execute('create table score\
                                (\
                                    wine_id varchar(20) not null primary key,\
                                    appear_clarity int,\
                                    appear_tone int,\
                                    appear_pureness int,\
                                    aroma_pureness int,\
                                    aroma_concentration int,\
                                    aroma_quality int,\
                                    taste_pureness int,\
                                    taste_concentration int,\
                                    taste_persistence int,\
                                    taste_quality int,\
                                    foreign key(wine_id) references base(wine_id)\
                                )')
        except:
            print("Error create score")
            pass

    def select_all(self):
        print("Base:")
        self.cursor.execute('select * from base')
        value = self.cursor.fetchall()
        for i in value:
            print(i)
        print("########################")
        print("Score:")
        self.cursor.execute('select * from score')
        value = self.cursor.fetchall()
        for i in value:
            print(i)
        print("########################")
        print("Store:")
        self.cursor.execute('select * from store')
        value = self.cursor.fetchall()
        # print(value)
        for i in value:
            print(i)

    def add(self, record):
        table = record.table
        data = record.data
        if table == 'base':
            if data['wine_id'] == 'auto':
                # 自动增加id（建议）
                self.cursor.execute('select wine_id from base')
                value = self.cursor.fetchall()
                if value != []:
                    data['wine_id'] = int(max(value)[0]) + 1
                else:
                    data['wine_id'] = 10000

        if table == 'store':
            if data['store_id'] == 'auto':
                # 自动增加id（建议）
                self.cursor.execute('select store_id from store')
                value = self.cursor.fetchall()
                if value != []:
                    data['store_id'] = int(max(value)[0]) + 1
                else:
                    data['store_id'] = 100
        # print(data)
        self.__insert(record)

    def __insert(self, record):
        table = record.table
        command = make_command('insert', table, record)
        self.cursor.execute(command, tuple(record.data.values()))

    def delete(self, record):
        table = record.table
        command = make_command('delete', table, record)
        self.cursor.execute(command)

    def update(self, record):
        table = record.table
        command = make_command('update', table, record)
        print(command)
        self.cursor.execute(command)

    def select(self, table):
        self.cursor.execute("select * from " + table)
        return self.cursor.fetchall()

    def select_com(self, command):
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def close(self):
        print("Save done")
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


# os.remove('test.db')
# c = wine()
# r1 = make_record('store', store_address='place1')
# r2 = make_record('store', store_address='place2')
# c.add(r1)
# c.add(r2)

# r1 = make_record('base', wine_type='type1', wine_num=1, store_id='100')
# r2 = make_record('base', wine_type='type1', wine_num=2, store_id='101')
# c.add(r1)
# c.add(r2)
# c.select_all()
# c.close()
# c = wine()
# temp = c.select_com("select store_id from store")
# strlist = []
# for i in temp:
#     strlist.append(i[0])
# print(strlist)
# c.close()
