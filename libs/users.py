import sqlite3
from settings import settings

# Tabelle generieren
connection = sqlite3.connect('database/user.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (id TEXT, username TEXT, name TEXT, email TEXT, password TEXT, age TEXT, birthday TEXT, profile_pic TEXT, info TEXT)''')
connection.commit()
connection.close()

# Funktion um Nutzer in die Datenbank einzutragen
def writeUser(data) -> str:
    id = data[0]
    username = data[1]
    name = data[2]
    email = data[3]
    password = data[4]
    age = data[5]
    birthday = data[6]
    profile_pic = data[7]
    info = data[8]

    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                   (id, username, name, email, password, age, birthday, profile_pic, info))

    connection.commit()
    connection.close()

    return 'Account written'

def isUsernameUsed(username) -> bool:
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username))
    user = cursor.fetchone()

    connection.commit()
    connection.close()

    if user is None:
        return False
    else:
        return True
    
def prooveEmail(email) -> bool:
    allowed = settings['allowedEMAILS']

    for mail in allowed:
        if mail in email:
            return True

    return False
