# Datei um alle Routen zu definieren
# Mach nichts ohne mich hier, weil die Datei wird riesig werden

from flask import Flask, render_template, session, redirect, url_for, request
from libs.users import writeUser

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
        id = request.json['id']
        username = request.json['username']
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        age = request.json['age']
        birthday = request.json['birthday']
        profile_pic = request.json['profile_pic']
        info = request.json['info']
        # ToDo:
        # 1. ID muss generiert werden
        # 2. Profilbild muss gespeichert werden un Path im array angeben
        # 3. Überprüfen das der Nutzername noch nicht vergeben ist
        
        data = [id, username, name, email, password, age, birthday, profile_pic, info]

        return writeUser(data)