import sqlite3
from settings import settings
import hashlib
from datetime import datetime, timedelta

# Tabelle generieren
connection = sqlite3.connect('database/user.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (id TEXT, username TEXT, name TEXT, email TEXT, password TEXT, birthday TEXT, info TEXT, profile_pic TEXT)''')
connection.commit()
connection.close()

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
                   (id, username, name, email, safe_password, birthday, info, ''))

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

def noBruteForce(username):
    now = datetime.now()
    login_attempts = []
    with open('database/login.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                file_username, _, timestamp_str = parts
                if file_username == username:
                    timestamp = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M:%S')
                    login_attempts.append((file_username, timestamp_str, timestamp))
    
    if len(login_attempts) < 3:
        return True
    
    for i in range(len(login_attempts) - 2):
        time_diff1 = login_attempts[i + 2][2] - login_attempts[i][2]
        time_diff2 = login_attempts[i + 1][2] - login_attempts[i][2]
        if time_diff1.total_seconds() <= 60 and time_diff2.total_seconds() <= 60:
            with open('database/timeout.txt', 'a') as output_file:
                output_file.write(f"{username}, {(now + timedelta(minutes=5)).strftime('%d/%m/%Y %H:%M:%S')}\n")
            with open('database/login.txt', 'r') as input_file:
                lines = input_file.readlines()
            with open('database/login.txt', 'w') as output_file:
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 3 and parts[0] != username:
                        output_file.write(line)
            return False
    return True

def notimeout(username) -> bool:
    now = datetime.now()
    now.strftime("%d/%m/%Y %H:%M:%S")

    with open('database/timeout.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(',')
            if username == parts[0]:
                a = now
                b = datetime.strptime(parts[1][1:-1], "%d/%m/%Y %H:%M:%S")
                if a < b:
                    return False
    return True