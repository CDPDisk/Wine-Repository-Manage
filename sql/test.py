import sqlite3
conn = sqlite3.connect('mytest.db')
cursor = conn.cursor()
try:
    cursor.execute('create table wine(\
        id1 int,\
        id2 int,\
        id3 int)')
except:
    pass
cursor.execute('insert into wine (id1,id2,id3) values(?,?,?)', (1, 2, 3))
cursor.execute('insert into wine (id1,id2,id3) values(?,?,?)', (5, 6, 7))
cursor.execute('update wine set id2=7,id3=5 where id1==5')
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
