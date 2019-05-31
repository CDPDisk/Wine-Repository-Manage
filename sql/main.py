# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:29:36 2019

@author: XIAOMI
"""

import sqlite3

conn=sqlite3.connect('test.db')
cursor=conn.cursor()
try:
    cursor.execute('create table wine\
                    (id varchar(20) primary key,\
                    origin varchar(20))')
except:
    pass
origin_place=['ab','b','c','d','e','a']
cursor.execute("delete from wine")
for index,origin in enumerate(origin_place):
    cursor.execute("insert into wine (id,origin) values(?,?)" ,(index,origin))
#cursor.execute("insert into wine (id,origin) values('%s','%s')" % (123,'ab'))

cursor.execute("select * from wine")
value=cursor.fetchall()
value
cursor.close()
conn.commit()
conn.close()