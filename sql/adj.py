# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:29:28 2019

@author: XIAOMI
"""
import sqlite3
import os

"""

"""


def make_wine_base_kw(wine_id='auto',
                      wine_type='NULL',
                      wine_num=0,
                      store_id='NULL'):
    return locals()


def make_wine_score_kw(wine_id='auto',
                       appear_clarity='NULL',
                       appear_tone='NULL',
                       appear_pureness='NULL',
                       aroma_pureness='NULL',
                       aroma_concentration='NULL',
                       aroma_quality='NULL',
                       taste_pureness='NULL',
                       taste_concentration='NULL',
                       taste_persistence='NULL',
                       taste_quality='NULL'):
    return locals()


def make_store_kw(store_id='NULL',
                  store_address='NULL',
                  store_temperature='NULL',
                  store_moisture='NULL'):
    return locals()


def make_command(operation, table, data):
    if operation == "insert":
        field = data.keys()
        block1 = ','.join(field)
        block2 = ','.join(list('?' * len(field)))
        command = 'insert into ' +\
            table +\
            ' (%s)' % (block1) +\
            ' values(%s)' % (block2)
    else:
        field = data.keys()
        value = data.values()
        block1 = ','.join(list(map(lambda a, b: str(a) + '=' + "'%s'" % str(b),
                                   field, value)))
        command = 'update ' +\
            table +\
            ' set ' +\
            block1 +\
            ' where wine_id==%s' % (data['wine_id'])
    return command


class wine():
    def __init__(self, file='test.db'):
        # 初始化创建表，如果表存在则跳过
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('create table store\
                                (\
                                    store_id varchar(20) primary key,\
                                    store_address varchar(20) not null,\
                                    store_temperature real,\
                                    store_moisture real\
                                )')
        except:
            pass
        try:
            self.cursor.execute('create table base\
                                (\
                                    wine_id varchar(20) primary key,\
                                    wine_type varchar(20) not null,\
                                    wine_num int not null,\
                                    store_id varchar(20) not null,\
                                    foreign key(store_id) references store(store_id)\
                                )')
        except:
            pass

        try:
            self.cursor.execute('create table score\
                                (\
                                    wine_id varchar(20) primary key,\
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
            pass

    def add_base(self, base):
        if base['wine_id'] == 'auto':
            # 自动增加id（建议）
            self.cursor.execute('select wine_id from base')
            value = self.cursor.fetchall()
            if value != []:
                base['wine_id'] = int(max(value)[0]) + 1
            else:
                base['wine_id'] = 0

        command = make_command('insert', 'base', base)
        self.cursor.execute(command, tuple(base.values()))

    def change_base(self, base):
        command = make_command('update', 'base', base)
        self.cursor.execute(command)

    def add_score(self, score):
        command = make_command('insert', 'score', score)
        self.cursor.execute(command, tuple(score.values()))

    def change_score(self, score):
        command = make_command('update', 'score', score)
        self.cursor.execute(command)

    def add_store():
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
        for i in value:
            print(i)

    def add(self, table, data):
        if table == 'base':
            if data['wine_id'] == 'auto':
                # 自动增加id（建议）
                self.cursor.execute('select wine_id from base')
                value = self.cursor.fetchall()
                if value != []:
                    data['wine_id'] = int(max(value)[0]) + 1
                else:
                    data['wine_id'] = 0

        if table == 'store':
            if data['store_id'] == 'auto':
                # 自动增加id（建议）
                self.cursor.execute('select store_id from store')
                value = self.cursor.fetchall()
                if value != []:
                    data['store_id'] = int(max(value)[0]) + 1
                else:
                    data['store_id'] = 0

        command = make_command('insert', table, data)
        self.cursor.execute(command, tuple(data.values()))

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


os.remove('test.db')
c = wine()
first = make_store_kw(store_address='place1')
c.add('store', first)
#first = make_wine_base_kw(wine_id=2, wine_type='yellow', wine_num=7)
#ans = c.change_base(first)
# if ans == 0:
c.select_all()
c.close()
