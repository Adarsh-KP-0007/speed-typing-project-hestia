import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="speedtype")
print(mydb)
mycursor=mydb.cursor()
mycursor.execute("delete from leaderboard where wpm<40")
mydb.commit()