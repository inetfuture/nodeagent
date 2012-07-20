# coding: UTF-8

import socket,struct,sys,time

def recv_timeout(the_socket,timeout=2):
    the_socket.setblocking(0)
    total_data=[];data='';begin=time.time()
    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break
        try:
            data=the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join(total_data)

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('localhost', 8088))
listener.listen(9999)
print 'server is listening...'

while True:
    try:
        socketToClient, addr = listener.accept()
        request = socketToClient.recv(1024)
        print request

        socketToWeb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketToWeb.connect(('www.baidu.com', 80))
        socketToWeb.send(request)
        response = recv_timeout(socketToWeb, 3)
        print response
        socketToWeb.close()

        socketToClient.send(response)
        socketToClient.close()
    except Exception, e:
        print e