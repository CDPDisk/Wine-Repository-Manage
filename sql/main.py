# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:29:36 2019

@author: XIAOMI
"""

import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
try:
    cursor.execute('create table wine(\
                    wine_id varchar(20) primary key,\
                    wine_type varchar(20),\
                    wine_num int)')
except:
    pass

cursor.execute('select * from wine where wine_id==2')
value = cursor.fetchall()
print(value)

cursor.execute("select * from wine")
value = cursor.fetchall()
value
cursor.close()
conn.commit()
conn.close()
