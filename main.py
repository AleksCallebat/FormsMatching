import os
from model import *

if __name__ == '__main__':
#    HOST = os.environ.get('192.168.4.4', 'localhost')
    HOST='192.168.4.4'
    try:
        PORT = int(os.environ.get('192.168.4.4', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,ssl_context="adhoc")