import psycopg2
import csv

# Connect to an existing database
conn = psycopg2.connect(host="localhost",
                        database="postgres",
                        user="postgres",
                        password="postgres")

conn.autocommit = True
cursor = conn.cursor()
cursor.execute("CREATE DATABASE testdb;")
cursor.close()
conn.close()

conn = psycopg2.connect(host="localhost",
                        database="testdb",
                        user="postgres",
                        password="postgres")

cursor = conn.cursor()
cursor.execute("CREATE USER testuser WITH ENCRYPTED PASSWORD 'testpass';")
cursor.execute("GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;")

cursor.execute("CREATE TABLE userdata (id BIGSERIAL NOT NULL PRIMARY KEY, "
               "name VARCHAR(50) NOT NULL, "
               "birthyear SMALLINT NOT NULL, "
               "email VARCHAR(70) NOT NULL);")

with open("UserData.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(
            "INSERT INTO userdata VALUES (%s, %s, %s, %s)",
            (row[0], row[1], row[2], row[3])
        )
    cursor.close()

conn.commit()
conn.close()

