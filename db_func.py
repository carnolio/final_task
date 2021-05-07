import mysql.connector
import os
#import hashlib
from passlib.hash import pbkdf2_sha256, md5_crypt
import getpass

#pip install mysql-connector-python

# sha1(sha1(getpass.getpass("New MySQL Password:")).digest()).hexdigest()'
#

mysql_host = '127.0.0.1'
mysql_database = 'link_shortener'
mysql_user = 'root'
mysql_password = 'P@ssw0rd'

def get_link_type():
    link_type = list()
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    cursor = cnx.cursor()
    query = ("SELECT * from link_type")
    cursor.execute(query)
    for type in cursor:
        link_type.append(type[1])
        print (type[1])
    cursor.close()
    cnx.close()
    return link_type

def get_hash(password):
    #password = "!Example secure password!"
    password = password.encode()
    salt = os.urandom(16)
    #password_hash = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash

def pass_is_correct(password_for_verify, mail):
    pass
    #pbkdf2_sha256.identify(hash)
    #True
    #pbkdf2_sha256.identify(other_hash)
    #False
    #    return True
    #    return False


def get_user(mail):
    user_data = list()
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    cursor = cnx.cursor()
    query = (f"SELECT * from users where users.mail = {mail}")
    cursor.execute(query)
    for user in cursor:
        user_data.append(user)
        print (user)
    cursor.close()
    cnx.close()
    return user_data

def add_user(mail, password):
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    cursor = cnx.cursor()
    password_hash=get_hash(password)
    print(password_hash)
    #password_hash = password
    #query = f"INSERT INTO users (mail, password_hash) VALUES ('{mail}',{password_hash})"
    query = f"INSERT INTO users (mail, password_hash) VALUES ('{mail}','{password_hash}')"
    print(query)
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()
    print(f"user: {mail} {password_hash} added")



get_link_type()
print(get_hash("password"))
add_user("carnolio@gmail.com","password")
