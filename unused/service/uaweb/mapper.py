# -*- coding: utf-8 -*-
# @author: ntischuk

import urllib2

from logg import Loggs
from urlparse import urlparse
from lxml import html


''' Page '''
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

class Scheme:
    ''' Scheme '''
    
    uri = None
    # default depth 
    depth = 0
    links = {}
    
    def __init__(self, uri = None):
        if uri:
            self.set_site(uri)
    
    def get_site(self, _parse = False):
        if _parse:
            return self.uri
        return self.uri.geturl()
    
    def set_site(self, uri):
        if Page.is_uri(uri):
            self.uri = urlparse(uri)
#         raise Exception('assigned to incorrectly refers uri %s'%(uri))
    
    def has_link(self, link):
        return self.links.has_key(link)
    
    def __walk(self, _site, _depth = 0, visit = []):
        if _depth < 0:
            return
        grabb = None
        grabb = Page(uri = _site)
        
        if grabb.error:
            return
         
        header = grabb.get_document().info()
        if header.dict['content-type'].find('text/html') == -1:
            return
        
        if not self.has_link(_site):
            self.links[_site] = grabb
            yield grabb
        
        hyperlink = grabb.search_page_links(self.get_site(), self.links.keys())
        if hyperlink:
            _depth = _depth - 1
            for reference in hyperlink:
                for page in self.__walk(reference, _depth):
                    yield page
        return
    
    def building(self, depth = None):
        if not str(depth).isdigit():
            depth = 0
        self.depth = int(depth)
        self.links = {}
        return self.__walk(self.get_site(), int(depth))
    