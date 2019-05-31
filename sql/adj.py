# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:29:28 2019

@author: XIAOMI
"""
import sqlite3

"""

"""


def make_wine_base_kw(wine_id='auto',
                      wine_type=None,
                      wine_num=0):
    return locals()


def make_wine_score_kw(wine_id='auto',
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


def make_insert_command(operation, table, field):
    block1 = ','.join(field)
    block2 = ','.join(list('?' * len(field)))
    command = operation +\
        ' into ' +\
        table +\
        ' (%s)' % (block1) +\
        ' values(%s)' % (block2)
    return command


class wine():
    def __init__(self, file='test.db'):
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('create table wine_base\
                                (\
                                    wine_id varchar(20) primary key,\
                                    wine_type varchar(20),\
                                    wine_num int\
                                )')
        except:
            pass

        try:
            self.cursor.execute('create table wine\
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
                                    taste_quality int\
                                    foreign key(wine_id) references wine(wine_id)\
                                )')
        except:
            pass

    def add_wine_base(self, wine_base):
        if wine_base['wine_id'] == 'auto':
            # 自动增加id（建议）
            self.cursor.execute('select wine_id from wine_base')
            value = self.cursor.fetchall()

            if value != []:
                wine_base['wine_id'] = int(max(value)[0]) + 1
            else:
                wine_base['wine_id'] = 0
        else:
            self.cursor.execute('select wine_id from wine_base')
            value = self.cursor.fetchall()

            if tuple(wine_base['wine_id']) in value:
                self.cursor.execute('update wine_base set wine_num=wine_num+%s \
                                        where wine_id==%s'
                                    % (wine_base['wine_num'], wine_base['wine_id']))
                return 0

        command = make_insert_command('insert', 'wine_base', wine_base.keys())
        self.cursor.execute(command, tuple(wine_base.values()))
        return 0

    def add_wine_score(self, wine_score):
        if wine_score['wine_id'] == 'auto':
            # 自动增加id（建议）
            self.cursor.execute('select wine_id from wine_score')
            value = self.cursor.fetchall()

            if value != []:
                wine_score['wine_id'] = int(max(value)[0]) + 1
            else:
                wine_score['wine_id'] = 0
        else:
            self.cursor.execute('select wine_id from wine_score')
            value = self.cursor.fetchall()

            if tuple(wine_score['wine_id']) in value:
                self.cursor.execute('update wine_score set wine_num=wine_num+%s \
                                        where wine_id==%s'
                                    % (wine_score['wine_num'], wine_score['wine_id']))
                return

        command = make_insert_command(
            'insert', 'wine_score', wine_score.keys())
        self.cursor.execute(command, tuple(wine_score.values()))

    def add_winehouse():
        pass

    def select_all(self):
        self.cursor.execute('select * from wine_base')
        value = self.cursor.fetchall()
        for i in value:
            print(i)

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


c = wine()
first = make_wine_base_kw(wine_id='3', wine_type='white', wine_num=2)
ans = c.add_wine(first)
if ans == 0:
    c.select_all()
c.close()
