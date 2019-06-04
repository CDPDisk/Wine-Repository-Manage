import sqlite3
import os
os.remove('mytest.db')
conn = sqlite3.connect('mytest.db')
cursor = conn.cursor()
try:
    cursor.execute('create table wine(\
        id1 int not null primary key,\
        id2 int not null,\
        id3 int)')
except:
    print('errer create')

cursor.execute('insert into wine (id1,id2,id3) values(?,?,?)', (1, 2, 3))
cursor.execute('insert into wine (id1,id2,id3) values(?,?,?)', (None, 2, 3))
cursor.execute('update wine set id2=7,id3=5 where id1==1')
cursor.execute('select * from wine')
value = cursor.fetchall()
for i in value:
    print(i)
cursor.close()
conn.commit()
conn.close()

table = ''
a = {'a': 1, 'b': 2}
'update ' + table + ' set ' + ''
