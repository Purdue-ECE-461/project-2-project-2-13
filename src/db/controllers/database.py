import mysql.connector

mydb = mysql.connector.connect(
  name="test",
  version="1.2.3",
  id = id
)
print(mydb)

db_cursor = mydb.cursor()

db_cursor.execute("CREATE DATABASE newDataBase")
db_cursor.execute("CREATE TABLE Databases (id STRING, name VARCHAR(255))")
db_cursor.execute("CREATE TABLE Version (id INT, name VARCHAR(255))")
db_cursor.execute("CREATE TABLE ID (id INT, name VARCHAR(255))")

Database_sql_query = "INSERT INTO Databases(id,name) VALUES(01, 'Database 1')"
Version_sql_query = "INSERT INTO Version(id,name) VALUES(01, '1.0.0')"
ID_sql_query = "INSERT INTO ID(id,name) VALUES(01, 'DB1')"

db_cursor.execute(Database_sql_query)
db_cursor.execute(Version_sql_query)
db_cursor.execute(ID_sql_query)
db_cursor.execute("SHOW DATABASES")

mydb.commit()

for db in db_cursor:
	print(db)

print(db_cursor.rowcount, "total rows")