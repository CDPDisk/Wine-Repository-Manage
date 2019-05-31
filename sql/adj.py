# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:29:28 2019

@author: XIAOMI
"""
import sqlite3

"""

"""
def make_wine_base_kw(wine_id = 'auto',
                      wine_type = None,
                      wine_num = 0):
    return locals()
def make_wine_score_kw(wine_id = 'auto',
                       appear_clarity = None,
                       appear_tone = None,
                       appear_pureness = None,
                       aroma_pureness = None,
                       aroma_concentration = None,
                       aroma_quality = None,
                       taste_pureness = None,
                       taste_concentration = None,
                       taste_persistence = None,
                       taste_quality = None):
    return locals()
def make_command(operation,table,field):
    block1 = ','.join(field)
    block2 = ','.join(list('?'*len(field)))
    command = operation+\
              ' into ' +\
              table +\
              ' (%s)'%(block1) +\
              ' values(%s)'%(block2)
    return command

class wine():
    def __init__(self,file='test.db'):
        self.conn=sqlite3.connect('test.db')
        self.cursor=self.conn.cursor()
    def add_wine(self,**kwargs):
        if kwargs['wine_id']=='auto':
            #自动增加id（建议）
            self.cursor.execute('select wine_id from wine')
            value = self.cursor.fetchall()
            kwargs['wine_id'] = max(value)+1
        else:
            self.cursor.execute('select wine_id from wine')
            value = self.cursor.fetchall()
            if kwargs['wine_id'] in values:
                #增加数量
                pass
        
        command = make_command('insert','wine',kwargs.keys())
        self.cursor.execute(command)
    def add_warehouse():
        pass