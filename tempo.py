import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="",
  database="clicker"
)

mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM go")
myresult = mycursor.fetchall()

print(myresult)