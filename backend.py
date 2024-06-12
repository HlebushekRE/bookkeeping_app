import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1qazxsw23edcG308:',
    database='bookkeeping'
)

print('\n\n')

mycursor = mydb.cursor()
'''mycursor.execute('SHOW TABLES')

for tb in mycursor:
    print(tb)
'''
#Функция ручного ввода данных

#Функция парсера

#Функция расчётов?

#Функция загрузки файлов на сервер?