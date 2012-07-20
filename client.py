# coding: UTF-8

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('localhost', 8087))
listener.listen(9999)
print 'client is listening...'

while True:
    try:
        socketToBrowser, addr = listener.accept()
        request = socketToBrowser.recv(1024)
        print request

        socketToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketToServer.connect(('localhost', 8088))
        socketToServer.send(request)
        response = socketToServer.recv(1024000)
        print response
        socketToServer.close()

        socketToBrowser.send(response)
        socketToBrowser.close()
    except Exception, e:
        print e
    