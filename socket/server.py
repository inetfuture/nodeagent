# coding: utf-8
import socket,struct,sys,time,re,thread

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

def async_handle_request(socketToClient):
    request = socketToClient.recv(1024)        
        
    m = re.match('.*GET\shttp://(.*?)/.*\sHTTP/1.1.*', request)
    webHost = m.group(1)

    socketToWeb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketToWeb.connect((webHost, 80))
    socketToWeb.send(request)
    response = recv_timeout(socketToWeb)        
    socketToWeb.close()
    
    print '\r\n[[', request, 'response data size:', len(response), ']]'

    socketToClient.send(response)
    socketToClient.close()

port = 8082
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('localhost', port))
listener.listen(9999)
print 'server is listening at port', port, '...'

while True:
    try:
        socketToClient, addr = listener.accept()
        thread.start_new_thread(async_handle_request, (socketToClient,))
    except Exception, e:
        print e