# Diese Datei ist eigentlich fertig.
# Wenn du testest musst die diese Datei starten

from server import server
from settings import settings

if __name__ == "__main__":
    server.secret_key = settings['secret_key']
    server.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database/user.db'
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    server.run(host=settings['host'], port=settings['port'], debug=settings['debug'], threaded=True)