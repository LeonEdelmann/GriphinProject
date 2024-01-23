# Datei um alle Routen zu definieren
# Mach nichts ohne mich hier, weil die Datei wird riesig werden

from flask import Flask, render_template, session, redirect, url_for

server = Flask(__name__)

@server.route('/', methods=['GET'])
def main():
    return 'Das ist Schisscord'
