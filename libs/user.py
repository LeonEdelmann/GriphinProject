import sqlite3

def getuserInfo(username):
    connection = sqlite3.connect('database/user.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.commit()
    connection.close()

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

    return {'username': name, 'info': info, 'profile_pic': profile_pic, 'friends': 
            friends, 'friendslist': friends_list, 'foundedcoms': foundedcommunities, 
            'founded_list': founded_list, 'membernum': membernum, 'community_list': comlist, 'email': email}