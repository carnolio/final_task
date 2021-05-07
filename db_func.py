import mysql.connector, os, hashlib
#pip install mysql-connector-python
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
    return link_type
    cursor.close()
    cnx.close()

def get_hash(password):
    #password = "!Example secure password!"
    password = password.encode()
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)
    return password_hash

def pass_is_correct(password_for_verify, mail):
    salt = os.urandom(16)
    #correct_password = "!Example secure password!"


    if True: #hmac.compare_digest(password_hash, encoded_incorrect_password):
        return True
    else:
        return False
    #return = hashlib.pbkdf2_hmac("sha256", password_hash.encode(), salt, 100000)

def get_user():
    pass

def add_user(mail, password):
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host,
                                  database=mysql_database)
    cursor = cnx.cursor()
    password_hash=get_hash(password)
    query = f"INSERT INTO `link_shortener`.`users` (`mail`, `password_hash`) VALUES ({mail},{password_hash})"
    cursor.execute(query)
    cursor.close()
    cnx.close()
    print(f"user: {mail} {password_hash} added")



get_link_type()