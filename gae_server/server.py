import webapp2
from google.appengine.api import urlfetch

class MainPage(webapp2.RequestHandler):
    def post(self):        
        url = self.request.get('url')
        cookie = self.request.get('cookie')
        
        result = urlfetch.fetch(
            url = url,            
            method = urlfetch.GET, 
            headers = { 'Cookie':  cookie })
        self.response.out.write(result.content)        

app = webapp2.WSGIApplication(
    [('/', MainPage)],
    debug=True)
