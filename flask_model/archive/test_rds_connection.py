import mysql.connector
import os
from werkzeug.utils import secure_filename

# Connect to MySQL database
db = mysql.connector.connect(
  host="rm-l4v31h2zpcuizey20.mysql.me-central-1.rds.aliyuncs.com",
  port=3306,
  user="mlproject",
  password="Mlproject@#1234",
  database="file_database"
)

print(db.is_connected())

cursor = db.cursor()

sql = '''select * from file;'''
#cursor.execute("SHOW TABLES")

#for table_name in cursor:
#   print(table_name)


# Execute the SQL statement
cursor.execute(sql)
print(cursor.fetchall())

# Close the cursor and connection
cursor.close()
db.close()
