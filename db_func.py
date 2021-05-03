import mysql.connector
#pip install mysql-connector-python

cnx = mysql.connector.connect(user='root', password='P@ssw0rd',
                              host='127.0.0.1',
                              database='link_shortener')
cursor = cnx.cursor()
query = ("SELECT * from link_type")
cursor.execute(query)
for type in cursor:
    print (type[1])
cursor.close()
cnx.close()