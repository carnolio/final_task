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
def generate_short_link (original):
#Ссылки должны сокращаться до длины от 8 до 12 символов не считая имени хоста:
    pass

def add_counter ():
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    cursor = cnx.cursor()
    query = f"INSERT INTO counters (count) VALUES ('0')"
    # print(query)
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()


    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    cursor = cnx.cursor()
    query = f"select MAX(ID) from counters"
    # print(query)
    cursor.execute(query)
    for res in cursor:
        result = res[0]
    print("res",result)
    cursor.close()
    cnx.close()
    return result


def add_link(original,short,user_id,type_id,friendly_link = "None"):
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    #приводим к нижнему

    cursor = cnx.cursor()

    #query = f"INSERT INTO users (mail, password_hash) VALUES ('{mail}','{password_hash}')"
    query = f"""INSERT INTO `link_shortener`.`shorted`
    (
    `original`,
    `short`,
    `friendly_link`,
    `user_id`,
    `type_id`,
    `counter_id`)
    VALUES
    ({original},
    {short},
    {friendly_link},
    {user_id},
    {type_id},
    {add_counter()});
    """
    print(query)
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()
    #print(f"query")




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
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash

def pass_is_correct(password_for_verify, mail):
    user = get_user(mail)
    #print("pass_foe ver",password_for_verify)
    #print("Hash: ", hash_verify)
    #print("user_hash: ", user["password_hash"])
    #print("sha", pbkdf2_sha256.identify(user["password_hash"]))
    #print("sha_mih",pbkdf2_sha256.verify(password_for_verify, user["password_hash"]))
    if pbkdf2_sha256.verify(password_for_verify, user["password_hash"]):
        return True
    else:
        return False

    # True
    # False

    #pbkdf2_sha256.identify(user["password_hash"])
    #pbkdf2_sha256.identify(hash)
    #pbkdf2_sha256.identify(other_hash)


def get_user(mail):
    user_data = {}
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    cursor = cnx.cursor()
    query = (f"SELECT * from users where mail = '{mail}'")
    #print(query)
    cursor.execute(query)
    for user in cursor:
        #user_data.append(user)
        print(user)
        user_data["mail"] = user[1]
        user_data["password_hash"] = user[2]
    cursor.close()
    cnx.close()
    return user_data

def add_user(mail, password):
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    #приводим к нижнему
    mail = mail.lower()
    cursor = cnx.cursor()
    password_hash = get_hash(password)
    print(password_hash)
    query = f"INSERT INTO users (mail, password_hash) VALUES ('{mail}','{password_hash}')"
    #print(query)
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()
    print(f"user: {mail} {password_hash} added")



get_link_type()
#add_user("carnolio@gmail.com","password")
print(get_user('carnolio@gmail.com'))
print(pass_is_correct("password","carnolio@gmail.com"))
print(add_counter())