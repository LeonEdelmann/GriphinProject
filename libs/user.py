import sqlite3
from libs.users import isUsernameUsed, prooveEmail
import hashlib
from settings import settings
import secrets
import os

def getuserInfo(username, rights):
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.commit()
    connection.close()

    if user == None:
        return 'Nutzer existiert nicht.'

    id = user[0]
    email = user[3]
    name = user[1]
    info = user[6]
    profile_pic = user[7]

    connection = sqlite3.connect('database/friends.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM friends WHERE persona = ? OR personb = ? AND status = ?', (id, id, 'OK'))
    friends = cursor.fetchall()
    connection.commit()
    connection.close() 
    
    friends_list = friends
    friends = len(friends)

    connection = sqlite3.connect('database/communities.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM communities WHERE founderid = ?', (id,))
    foundedcommunities = cursor.fetchall()
    connection.commit()
    connection.close() 

    founded_list = foundedcommunities
    foundedcommunities = len(foundedcommunities)

    connection = sqlite3.connect('database/communitymembers.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM members WHERE userid = ?', (id,))
    membernum = cursor.fetchall()
    connection.commit()
    connection.close()

    comlist = membernum
    membernum = len(membernum)

    if rights == 'Yes':
        return {'username': name, 'info': info, 'profile_pic': profile_pic, 'friends': 
                friends, 'friendslist': friends_list, 'foundedcoms': foundedcommunities, 
                'founded_list': founded_list, 'membernum': membernum, 'community_list': comlist, 
                'email': email, 'id': id, 'rights': 'Yes'}
    elif rights == 'No':
        return {'username': name, 'info': info, 'profile_pic': profile_pic, 'friends': 
                friends, 'friendslist': friends_list, 'foundedcoms': foundedcommunities, 
                'founded_list': founded_list, 'membernum': membernum, 'community_list': comlist, 
                'rights': 'No'}

def commitChanges(description, email, id) -> str:
    if prooveEmail(email) == True:
        connection = sqlite3.connect('database/user.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET email = ?,info = ? WHERE id = ?', (email, description, id,))
        connection.commit()
        connection.close()
        print('ok')
        return 'OK'
    else:
        return 'E-Mail nicht erlaubt.'

def commitAllChanges(username, description, email, id) -> str:
    if isUsernameUsed(username) == False:
        if prooveEmail(email) == True:
            connection = sqlite3.connect('database/user.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE users SET username = ?, email = ?, info = ? WHERE id = ?', (username, email, description, id,))
            connection.commit()
            connection.close()
            return 'OK'
        else: 
            return 'E-Mail nicht erlaubt.'
    else:
        return 'Nutzername bereits vergeben.'

def changePassword(password, new_password, id):
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    user = cursor.fetchone()
    connection.commit()
    connection.close()
    if hashlib.sha512(password.encode('utf-8')).hexdigest() == user[4]:
        connection = sqlite3.connect('database/user.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashlib.sha512(new_password.encode('utf-8')).hexdigest(), id,))
        user = cursor.fetchone()
        connection.commit()
        connection.close()
        return 'OK'
    else:
        return 'Aktuelles Passwort falsch eingegeben!'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings['extensions']

def make_file_name() -> str:
    return secrets.token_hex(4)

def writeProfile_pic(id, path):
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()
    cursor.execute('SELECT profile_pic FROM users WHERE id = ?', (id,))
    old_path = cursor.fetchone()
    cursor.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (path, id,))
    delete_old_profile_pic(old_path)
    connection.commit()
    connection.close()

def delete_old_profile_pic(filename):
    if filename[0] == 'user.png':
        return
    else:
        os.remove(str('static/imgs/' + filename[0]))