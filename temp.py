import requests
import tornado.web
import tornado.ioloop
from bs4 import BeautifulSoup as bs

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        url = "http://quotes.toscrape.com"
        content = requests.get(url+self.request.uri)
        content = find(content.text)
        self.write(content)

def find(content):
    soup = bs(content, 'lxml')
    link = soup.find_all('link',attrs={'rel':'stylesheet'})
    for i in link:
        href = i.attrs.get('href')
        css=get_file(href)
        content = content+"<style>"+css+"</style>"
    return content

def get_file(file):
    if file == "/static/bootstrap.min.css":
        with open('bootstrap.min.css','r') as f:
            return f.read()
    elif file == "/static/main.css":
        with open('main.css','r') as f:
           return f.read()


def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()



if __name__=="__main__":
    main()