# Datei um alle Routen zu definieren
# Mach nichts ohne mich hier, weil die Datei wird riesig werden

from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from libs.users import writeUser, isUsernameUsed, prooveEmail, allowedLogin, proofeBirthdate
from libs.bruteforce import noBruteForce, notimeout
from libs.user import getuserInfo
from datetime import datetime
import secrets

extensions = set(['jpg', 'jpeg', 'png'])
folder = 'database/img/'

server = Flask(__name__)

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
    else:
        return render_template('notLogin.html')
    
@server.route('/getuser/<username>', methods=['GET'])
def getuser(username):
    if 'username' in session:
        answer = getuserInfo(username)
        if username == session['username']:
            answer['rights'] = 'Yes'
            return jsonify(answer)
        else:
            answer['rights'] = 'No'
            return jsonify(answer)
    return render_template('notLogin.html')

@server.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))