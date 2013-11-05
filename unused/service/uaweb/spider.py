# -*- coding: utf-8 -*-
# @author: ntischuk
# @version: 1.2.6

import urllib2

from logg import Loggs
from urlparse import urlparse
from lxml import html


''' 
    
    @note Object Page 
'''
class Page:
    uri       = None
    html      = None
    document  = None
    hyperlink = []
    error     = None
    visited   = False  
    
    def __init__(self, uri = None):
        if uri:
            self.set_uri(uri)
            self.connect()
    
    def connect(self):
        try:
            request = urllib2.Request(self.get_uri(), None, {'User-agent':'Robot-Grabber'})
            self.document = urllib2.urlopen(request)
            self.html = self.document.read()
            self.visited = True
            return self.document
        except urllib2.HTTPError, e:
            self.error = str(e)
            return
    
    def has_header(self, key, value):
        document = self.get_document()
        if not hasattr(document, 'info'):
            return False
        
        header = document.info()
        if header.get(key, None) and header.dict[key].find(value) != -1:
            return True
        return False
    
    @staticmethod
    def is_uri(uri):
        pieces = urlparse(uri)
        return all([pieces.scheme, pieces.netloc])
    
    def set_uri(self, link):
        if not self.is_uri(link):
            raise Exception('Not correct link: %s'%(link))
        self.uri = link
    
    def get_uri(self):
        return self.uri
    
    def status(self):
        return self.get_document().getcode()
    
    def get_html(self):
        return self.html
    
    def get_document(self):
        return self.document
    
    def hyperlinks(self):
        def is_hyperlink(link):
            # todo: http://example.com/index.php#about
            return urlparse(link).netloc == urlparse(self.get_uri()).netloc
        
        if self.hyperlink:
            return self.hyperlink
        else:
            if not self.get_html():
                return list()
            
            _search = html.fromstring(self.get_html())
            _search.make_links_absolute(self.get_uri())
            
            hyperlink = []
            reference = _search.xpath('descendant-or-self::a[@href] | descendant-or-self::form[@action] | descendant-or-self::iframe[@src]')
            for e in reference:
                if e.tag == 'a':
                    link = e.get('href', None)
                elif e.tag == 'form':
                    link = e.get('action', None)
                elif e.tag == 'iframe':
                    link = e.get('src', None)
                
                if link and is_hyperlink(link):
                    hyperlink.append(link)
            self.hyperlink = hyperlink
            return self.hyperlink

''' 
    
    @note Object Crawler 
'''
class Crawler():
    __uri    = None
    __depth  = 0
    __stack  = {}
    __viewer = []
    
    def uri(self, uri):
        self.__uri = uri
    
    def depth(self, depth):
        self.__depth = depth
    
    def stack(self):
        return self.__stack
    
    def viewer(self):
        return self.__viewer
    
    def grabbing(self, uri, depth):
        self.uri(uri)
        self.depth(depth)
        return self.__mapping(uri, 0)
    
    def __mapping(self, reference, depth = 0):
        if depth > self.__depth:
            return
        if reference in self.__viewer:
            return
        
        page = Page(reference)
        if page.has_header('content-type', 'text/html'):
            link = reference[0:75]
            print('{0}{1}'.format(link.ljust(77, '.'), depth))
            
            self.__stack[hash(reference)] = {'page':page, 'depth':depth}
            self.__viewer.append(reference)
            links = page.hyperlinks()
            return map(self.__mapping, links, [depth+1]*len(links))
        return

if __name__ == '__main__':
    import time
    t = time.time()
    
    crawler = Crawler()
    crawler.grabbing(uri = 'http://uawebchallenge.com/', depth = 50)
    print len(crawler.viewer())
    
    print "time: %f" % (time.time()-t)
    
    