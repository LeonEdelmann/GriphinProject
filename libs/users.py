import sqlite3
from settings import settings
import hashlib
from datetime import datetime


# Funktion um Nutzer in die Datenbank einzutragen
def writeUser(data) -> str:
    id = data[0]
    username = data[1]
    name = data[2]
    email = data[3]
    password = data[4]
    birthday = data[5]
    info = data[6]

    safe_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                   (id, username, name, email, safe_password, birthday, info, 'user.png'))

    connection.commit()
    connection.close()

    return 'Account written'

def isUsernameUsed(username) -> bool:
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
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

def allowedLogin(username, password) -> str:
    safe_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, safe_password,))
    user = cursor.fetchone()

    connection.commit()
    connection.close()

    if user is None:
        return 'Nutzername oder Passwort falsch.'
    else:
        return 'OK'

def proofeBirthdate(date) -> bool:
    try:
        birthdate = datetime.strptime(date, '%Y-%m-%d')

        today = datetime.now()
        if birthdate < today:
            return True
        else:
            return False
    except ValueError:
        return False
