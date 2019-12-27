import sqlite3

conn = sqlite3.connect('test.db')

print ("Opened database successfully")

cursor = conn.cursor()

conn.execute('DROP TABLE USERS;')

conn.execute('''CREATE TABLE USERS
         (ID INT PRIMARY KEY     NOT NULL,
         USERNAME           TEXT    NOT NULL,
         PASSWORD            INT     NOT NULL);''')

print ("Table created successfully")

insert_query = "INSERT INTO USERS VALUES(?, ?, ?)"

users = [
    (1, 'rolf', 'asdf'),
    (2, 'rolf1', 'asdf1'),
    (3, 'anne', 'xyz')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM USERS"

for row in cursor.execute(select_query):
    print(row)

conn.commit()
conn.close()


@jwt.authentication_handler
def authenticate(username, password):
    user = User.find_by_username(username)
    print(user)
    print(user.password)
    print(password)
    if user and safe_str_cmp(user.password, password):
        return user

@jwt.identity_handler
def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)