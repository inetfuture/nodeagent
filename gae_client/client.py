# coding: utf-8

import sys
import socket
import thread
import re
import urllib
import urllib2

def async_handle_request(socketToBrowser):
    try:
        request = socketToBrowser.recv(1024000)               
        m = re.match('(?s).*GET\s(?P<url>.*?)\sHTTP/1\.1(.*Cookie:\s(?P<cookie>.*?)\s.*|.*)',  request)
        
        if m:            
            reqUrl = m.group('url')
            reqCookie = m.group('cookie')
            
            data = urllib.urlencode({ 'url':  reqUrl, 'cookie': reqCookie })
            req = urllib2.Request('http://localhost:8080',  data)
            response = urllib2.urlopen(req).read()            

            socketToBrowser.send(response)
            socketToBrowser.close()
            
            print '\r\n[[\r\n', request,  'url:',  reqUrl,  '\r\ncookie:',  reqCookie, '\r\nresponse data size:', len(response), '\r\n]]'
        else:
            print '\r\n[[\r\ncannot analyze request:\r\n',  request,  ']]'
    except Exception,  e:
        print e

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('localhost', 8087))
listener.listen(9999)
print 'client is listening...'

while True:
    try:
        socketToBrowser, addr = listener.accept()        
        thread.start_new_thread(async_handle_request, (socketToBrowser,))
    except Exception, e:
        print e
    
