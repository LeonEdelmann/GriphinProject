# Datei um alle Routen zu definieren
# Mach nichts ohne mich hier, weil die Datei wird riesig werden

from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from libs.users import writeUser, isUsernameUsed, prooveEmail, allowedLogin, proofeBirthdate
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
        # ToDo:
        # 2. Profilbild muss gespeichert werden un Path im array angeben

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

        if allowedLogin(username, password) == 'OK':
            session['username'] = username
            return jsonify('OK')
        elif allowedLogin(username, password) == 'Nutzername oder Passwort falsch.':
            return jsonify('Nutzername oder Passwort falsch.')
        
@server.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('notLogin.html')
    
@server.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))