# import library dari mysql connector
import mysql.connector


# konfigurasi myDB
myDB = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
)

cursorObject = myDB.cursor()
cursorObject.execute("CREATE DATABASE IF NOT EXISTS belajarDjango")

print("Sukses!")