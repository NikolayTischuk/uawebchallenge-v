# -*- coding: utf-8 -*-
# @author: ntischuk

import urllib2

from logg import Loggs
from urlparse import urlparse
from lxml import html


''' 
    @version: 1.1
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
            self.document = urllib2.urlopen(self.get_uri())
            self.html = self.document.read()
            self.visited = True
            return self.document
        except urllib2.HTTPError, e:
            self.error = str(e)
            return
    
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
    
    def get_html(self):
        return self.html
    
    def get_document(self):
        return self.document
    
    def search_page_links(self, absolut_links, _exclude = []):
        def is_site_hyperlink(link):
            # todo: http://example.com/index.php#about
            return urlparse(link).netloc == urlparse(absolut_links).netloc
        
        if self.hyperlink:
            return self.hyperlink
        else:
            _search = html.fromstring(self.get_html())
            if absolut_links:
                _search.make_links_absolute(absolut_links)
            self.hyperlink = []
            reference = _search.xpath('descendant-or-self::a[@href]')
            for link in reference:
                href = link.get('href')
                if is_site_hyperlink(href) and not href in _exclude:
                    self.hyperlink.append(href)
        return self.hyperlink
    
class Spider():
    __uri    = None
    __depth  = 0
    __stack  = {}
    __viewer = []
    
    def uri(self, uri):
        self.__uri = uri
    
    def depth(self, depth):
        self.__depth = depth
    
    def viewer(self):
        return self.__viewer
    
    def grabbing(self, uri, depth):
        self.uri(uri)
        self.depth(depth)
        return self.__mapping(uri, 0)
    
    def __mapping(self, reference, depth = 0):
        if depth > self.__depth:
            return 
        
        page = None
        if reference in self.__viewer:
            page = self.__stack.get(hash(reference), None)['page']
        else:
            page = Page(reference)
        
        if not page:
            return 
        
        if hasattr(page.get_document(), 'info'):
            header = page.get_document().info()
            if header.dict['content-type'].find('text/html') != -1:
                print depth, reference
                id = hash(reference)
                self.__stack[id] = {'page':page, 'depth':depth}
                self.__viewer.append(reference)

                links = page.search_page_links(self.__uri)
                grab = []
                for ref in links:
                    if ref not in self.__viewer: 
                        grab.append(ref)
                if grab:
                    return map(self.__mapping, grab, [depth+1]* len(grab))
        return

if __name__ == '__main__':
    w = Spider()
    w.grabbing('http://blog.ntischuk.com/', 80)
    print len(w.viewer())
#     for index, link in enumerate(w.viewer()):
#         print index, link
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            