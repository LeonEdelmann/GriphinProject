# Diese Datei ist eigentlich fertig.
# Wenn du testest musst die diese Datei starten

from server import server
from settings import settings

if __name__ == "__main__":
    server.run(host=settings['host'], port=settings['port'], debug=settings['debug'], threaded=True)