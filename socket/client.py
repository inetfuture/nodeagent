# coding: utf-8

import socket, thread

def async_handle_request(socketToBrowser):
    request = socketToBrowser.recv(1024)        

    socketToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketToServer.connect(('localhost', 8088))
    socketToServer.send(request)
    response = socketToServer.recv(1024000)        
    socketToServer.close()
    
    print '\r\n[[', request, 'response data size:', len(response), ']]'

    socketToBrowser.send(response)
    socketToBrowser.close()

port = 8081
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('localhost', port))
listener.listen(9999)
print 'client is listening at port', port, '...'

while True:
    try:
        socketToBrowser, addr = listener.accept()
        thread.start_new_thread(async_handle_request, (socketToBrowser,))
    except Exception, e:
        print e
    
