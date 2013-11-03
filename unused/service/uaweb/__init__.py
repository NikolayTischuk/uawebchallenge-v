import sys
import httplib
import urlparse
from BeautifulSoup import BeautifulSoup

class Crawler:
    def __init__(self, host, root, depth, handler):
        self._host = host
        self._root = root
        self._depth = depth
        self._handler = handler
        self._visited = []
        self._connection = httplib.HTTPConnection(host)

    def run(self):
        self._run(self._root, '', 0)

    def _run(self, url, parentUrl, currentDepth):
        # is some clown is using absolute URLs for internal links?
        url = url.replace('http://' + self._host, '')
        # bail if we're running too deep
        if self._depth >= 0 and currentDepth > self._depth:
#             print 'WOWWW...'
            return
        # bail if it's a manky URL
        if ':' in url or url[0].startswith('#'):
            return

        # normalise relative urls
        if url[0] != '/':
            index = parentUrl.rfind('/')
            if index > -1:
                url = parentUrl[:index] + '/' + url
            else:
                url = '/' + url

        # bail if we've already visited this page
        if url in self._visited:
            return

        page = Page(self._connection, url)
        self._handler(page)
        self._visited.append(url)

        print self._depth, currentDepth 
        print page.urls, [url] * len(page.urls), [currentDepth + 1] * len(page.urls)
        map(self._run, page.urls, [url] * len(page.urls), [currentDepth+1] * len(page.urls))

class Page:
    def __init__(self, connection, url):
        self.url = url
        self.urls = []
        self.inputs = []

        # get a list of querystring key
        querystring = urlparse.urlparse(url).query
        self.querystring_params = [part.split('=')[0] for part in querystring.split('&')]

        connection.connect()
        connection.request('GET', url, headers = {'User-Agent': 'Colourblind Crawler 0.1'})
        response = connection.getresponse()

        self.statusCode = response.status
        if self.statusCode != 200:
            # handle redirects (location probably isn't relevant to all of them)
            if self.statusCode >= 300 and self.statusCode < 400:
                self.urls.append(response.getheader('Location'))

        # if it's HTML, parse the sucker
        if 'text/html' in response.getheader('Content-Type'):
            soup = BeautifulSoup(response.read(), fromEncoding='utf-8')
            links = soup('a')
            # grab all the hrefs and remove any blanks
            self.urls.extend(filter(lambda x: x != None, map(lambda x: x.get('href'), links)))
            self.inputs.extend(soup('input'))
            self.inputs.extend(soup('select'))
            self.inputs.extend(soup('textarea'))

        connection.close()

def print_page(page):
    pass
#     print('{0} {1}'.format(page.url.ljust(75, '.'), page.statusCode))

if __name__ == '__main__':
    startPage = '/'
    depth = 1

    crawler = Crawler('blog.ntischuk.com', startPage, depth, print_page)
    crawler.run()
    print crawler._visited