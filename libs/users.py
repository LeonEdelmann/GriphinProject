import sqlite3

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