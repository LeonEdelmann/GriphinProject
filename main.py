# Diese Datei ist eigentlich fertig.
# Wenn du testest musst die diese Datei starten

from server import server, folder, Socketio
from settings import settings
import sqlite3

def generateTables():
    # Nutzer Datenbank
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id TEXT, username TEXT, name TEXT, email TEXT, password TEXT, birthday TEXT, info TEXT, profile_pic TEXT)''')
    connection.commit()
    connection.close()
    # Freunde Datenbank
    connection = sqlite3.connect('database/friends.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS friends
            (persona TEXT, personb TEXT, status TEXT)''')
    connection.commit()
    connection.close()
    # Chats Datenbank
    connection = sqlite3.connect('database/chats.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chats
            (persona TEXT, personb TEXT)''')
    connection.commit()
    connection.close()
    # Messages Datenbank
    connection = sqlite3.connect('database/messages.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
            (datetime TEXT, isread TEXT, message TEXT, writer TEXT, reader TEXT)''')
    connection.commit()
    connection.close()
    # Communities Datenbank
    connection = sqlite3.connect('database/communities.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS communities
            (foundingdate TEXT, founderid TEXT, name TEXT, adminoneid TEXT, admintwoid TEXT, adminthreeid TEXT, maxpeoplenum TEXT, banner TEXT, profilepic TEXT, discussionroomnum TEXT, allowedmedia TEXT)''')
    connection.commit()
    connection.close()
    # Community Mitglieder Datenbank
    connection = sqlite3.connect('database/communitymembers.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS members
            (communityname TEXT, userid TEXT)''')
    connection.commit()
    connection.close()

if __name__ == "__main__":
    server.secret_key = settings['secret_key']
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    server.config['UPLOAD_FOLDER'] = folder
    generateTables()
    Socketio.run(server, host=settings['host'], port=settings['port'], debug=settings['debug'])