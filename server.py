# Datei um alle Routen zu definieren
# Mach nichts ohne mich hier, weil die Datei wird riesig werden

from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from libs.users import writeUser, isUsernameUsed, prooveEmail, allowedLogin, proofeBirthdate
from libs.bruteforce import noBruteForce, notimeout
from libs.user import getuserInfo, commitAllChanges, commitChanges, changePassword, allowed_file, writeProfile_pic, make_file_name
from libs.chats import make_chat, getchatJson
from datetime import datetime
import secrets
import os

folder = 'static/imgs/'

server = Flask(__name__)
Socketio = SocketIO(server)

@server.route('/', methods=['GET'])
def main():
    return 'Das ist Schisscord'

# Funktion zum Sign Up eines Users
@server.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        id = secrets.token_hex(8)
        username = request.json['username']
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        birthday = request.json['birthday']
        info = request.json['info']

        if isUsernameUsed(username) == True:
            return jsonify('Nutzername vergeben.')
        else:
            if prooveEmail(email) == True:
                if proofeBirthdate(birthday) == True:
                    data = [id, username, name, email, password, birthday, info]
                    return jsonify(writeUser(data))
                else:
                    return jsonify('Geburtsdatum ist falsch.')
            else:
                return jsonify('E-Mail nicht erlaubt.')

    
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        ip_addr = request.remote_addr
        now = datetime.now()
        string = username + "," + str(ip_addr) + "," + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "\n"
        
        f = open('database/login.txt', "a")
        f.write(string)
        f.close()

        noBruteForce(username)

        if notimeout(username) == True:
            if allowedLogin(username, password) == 'OK':
                session['username'] = username
                return jsonify('OK')
            elif allowedLogin(username, password) == 'Nutzername oder Passwort falsch.':
                return jsonify('Nutzername oder Passwort falsch.')
        else:
            return jsonify('Zu viele Fehlversuche')
        
@server.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('notLogin.html')
    
@server.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    if 'username' in session:
        if request.method == 'GET':
            return render_template('user.html')
        elif request.method == 'POST':
            target = request.json['target']
            currentUsername = request.json['currentUsername']
            if currentUsername == session['username']:
                if target == 'profile':
                    new_username = request.json['username']
                    new_description = request.json['description']
                    new_email = request.json['email']
                    id = request.json['id']
                    if new_username == session['username']:
                        return jsonify(commitChanges(new_description, new_email, id))
                    else:
                        answer = commitAllChanges(new_username, new_description, new_email, id)
                        session['username'] = new_username
                        return jsonify(answer)
                elif target == 'password':
                    password = request.json['currentpassword']
                    new_password = request.json['newpassword']
                    id = request.json['id']
                    return jsonify(changePassword(password, new_password, id))
            else:
                return jsonify('Nicht dein Profil.')
    else:
        return render_template('notLogin.html')
    
@server.route('/sendmessage', methods=['POST'])
def sendMessage():
    if 'username' in session:
        personA = session['username']
        personB = request.json['username']
        make_chat(personA, personB)
        return jsonify('OK')
    else:
        return render_template('notLogin.html')

@server.route('/uploadprofile-pic', methods=['POST'])
def uploadprofile_pic():
    if 'username' in session:
        username = request.form['currentUsername']
        id = request.form['id']
        img = request.files['file']
        if username == session['username']:
            if allowed_file(img.filename):
                filename = secure_filename(make_file_name() + '.png')
                img.save(os.path.join(folder, filename))
                writeProfile_pic(id, filename)
                return redirect(url_for('main'))
            else:
                return render_template('sthwentwrong.html')
        else: 
            return render_template('sthwentwrong.html')
    else:
        return redirect(url_for('main'))

@server.route('/getuser/<username>', methods=['GET'])
def getuser(username):
    if 'username' in session:
        rights = ''
        if username == session['username']:
            rights = 'Yes'
        else:
            rights = 'No'
        answer = getuserInfo(username, rights)
        if answer == 'Nutzer existiert nicht.':
            return jsonify(answer)
        else:
            return jsonify(answer)
    return render_template('notLogin.html')

@server.route('/wrongusername', methods=['GET'])
def wrongusername():
    return render_template('wrongusername.html')

@server.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('chats.html')
        else:
            pass
    else:
        return render_template('notLogin.html')
    
@server.route('/chatjson', methods=['GET'])
def chatjson():
    if 'username' in session:
        return jsonify(getchatJson(session['username']))
    else:
        return render_template('notLogin.html')

@server.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))