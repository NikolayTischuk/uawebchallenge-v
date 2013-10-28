#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ntischuk

# import modules
import urllib2
import re
import cssutils


# import from modules
from lxml import html
from lxml.etree import XPathEvalError
from cssselect.xpath import ExpressionError
from cssselect import GenericTranslator, SelectorError
from urlparse import urlparse
from logg import Loggs
from mapper import Page

class Rules():
    uri   = None
    rules = []
    
    def __init__(self, uri, rules):
        self.uri   = uri
        rules.sort()
        self.rules = rules
    def get_rules(self):
        return filter(None, self.rules)
    def unuset_rule(self, used):
        if used in self.rules:
            index = self.rules.index(used)
            self.rules[index] = None

class ParsingWebsite:
    __html  = ''
    __uri   = ''
    __rules = {}
    loggs   = None

    def __init__(self):
        logging = __import__('logging')
        cssutils.log.setLevel(logging.FATAL)
        self.loggs = Loggs()
        self.clear()

    def clear(self):
        self.loggs.logger.info('clear property')
        
        self.__html   = None
        self.__uri    = None
        self.__rules  = {}
        
    
    def set_html(self, content):
        self.loggs.logger.info('set content html')
        self.__html = content
    
    def set_uri(self, hyperlink):
        self.loggs.logger.info('set uri %s'%(hyperlink))
        self.__uri = hyperlink
    
    def get_uri(self):
        return self.__uri
    
    # --- get all link and style HTML Page
    def get_css_content(self):
        self.loggs.logger.info('parsing css content')
        
        if not self.__html:
            msg = 'Does not have content in %s'%(self.get_uri())
            self.loggs.logger.info(msg)
            raise Exception(msg)
        
        # --- check dom elemnt
        def is_css_link(element):
            if element.tag != 'link':
                return False
            if element.get('type') == 'text/css' or element.get('rel') == 'stylesheet':
                href = element.get('href')
                if href:
                    return True
            return False
        
        # --- work with css content
        def get_rules(content):
            def pseudo_classes(string):
                if not string:
                    return False
                pattern = re.compile('\:{1,2}.+')
                return bool(re.search(pattern, string))
            # --- Parsion css content
            sheet  = cssutils.parseString(content)
            result = []
            for rule in sheet.cssRules:
                if hasattr(rule, 'selectorText'):
                    selector = rule.selectorText
                    if selector.find(',') != -1:
                        split = selector.split(',')
                        for item in split:
                            if not pseudo_classes(item):
                                result.append(item.strip())
                    elif not pseudo_classes(selector):
                        result.append(selector.strip(' '))
            return list(set(result))
        
        # --- get all styles
        document = html.fromstring(self.__html)
        document.make_links_absolute(self.get_uri())
        styles = document.xpath('descendant-or-self::style')
        if styles:
            for item in styles:
                rules = get_rules(item.text)
                self.__rules[self.get_uri()] = Rules(self.get_uri(), rules)
        
        # --- get all links and his css content
        links = document.xpath('descendant-or-self::link')
        if links:
            for item in links:
                if is_css_link(item):
                    href = item.get('href')
                    if Page.is_uri(href) and not self.__rules.has_key(href):
                        try:
                            uri_content = urllib2.urlopen(href).read()
                            rules = get_rules(uri_content)
                            self.__rules[href] = Rules(href, rules)
                        except:
                            pass
    
    # mark rule as used
    def rule_used(self, used):
        references = self.__rules.keys()
        for link in references:
            items = self.__rules[link]
            items.unuset_rule(used)
    
    # search and mark as used rule
    def unused_selectors(self):
        self.loggs.logger.info('Parsing page %s'%(self.get_uri()))
        document = html.fromstring(self.__html)
        document.make_links_absolute(self.get_uri())
        
        # Check if need parsing many page on website, verify using links style
        def has_style_in_page(link):
            if link != self.get_uri():
                expression = GenericTranslator().css_to_xpath('link[href="%s"]'%(link))
                return bool(document.xpath(expression))
            return True
        
        references = [item for item in self.__rules.keys() if has_style_in_page(item)]
        for link in references:
            rules = list(self.__rules[link].get_rules())
            for item in rules:
                if item:
                    try:
                        expression = GenericTranslator().css_to_xpath(item)
                        result = document.xpath(expression)
                        if len(result)>0:
                            self.rule_used(item)
                    except (ExpressionError, SelectorError, XPathEvalError), e:
                        self.loggs.logger.error('Invalid selector: %s : %s'%(item, str(e)))
    
    # return clear unused rules
    def get_unused_rules(self):
        self.__rules
        result = {}
        for item in self.__rules:
            rules = self.__rules[item].get_rules()
            result[item] = Rules(item, rules) 
        return result
    
    # main method
    def parsing_css(self, content):
        if self.get_uri():
            self.set_html(content)
            self.get_css_content()
            self.unused_selectors()

            return self.get_unused_rules()
        return dict()
