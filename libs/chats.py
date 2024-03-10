import sqlite3

def make_chat(personA, personB):
    connection = sqlite3.connect('database/chats.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM chats WHERE personA = ? OR personB = ?', (personA, personA))
    existence = cursor.fetchone()
    if existence == None:
        cursor.execute('INSERT INTO chats VALUES (?, ?)', (personA, personB,))
    else:
        connection.commit()
        connection.close()

def getchatJson(username):
    names = []
    contacts = []
    unreadeded = []
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.commit()
    connection.close()

    connection = sqlite3.connect('database/chats.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM chats WHERE personA = ? OR personB = ?', (username, username))
    chats = cursor.fetchall()
    connection.commit()
    connection.close()

    for element in chats:
        if element[0] == username:
            name = element[1]
            names.append(name)
        else:
            name = element[0]
            names.append(name)

    for name in names:
        connection = sqlite3.connect('database/user.db')
        cursor = connection.cursor()
        cursor.execute('SELECT profile_pic FROM users WHERE username = ?', (name,))
        profile_pic = cursor.fetchone()
        connection.commit()
        connection.close()
        contacts.append([profile_pic[0], name])

    connection = sqlite3.connect('database/messages.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM messages WHERE reader = ? AND isread = ?', (username, 'No',))
    unreaded = cursor.fetchall()
    connection.commit()
    connection.close()

    for elem in unreaded:
        unreadeded.append(elem[3])
    print(contacts)
    return {
        'own_account': {
            'own_profile_pic': user[7],
            'own_name': username
        },
        'chats': contacts,
        'unreadedcontacts': unreadeded
    }