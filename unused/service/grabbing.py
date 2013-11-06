# -*- coding: utf-8 -*-
# @author: ntischuk

from uaweb.parser import ParsingWebsite
from uaweb.spider import Crawler, Page
from uaweb.logg import Loggs

class Pages:
    def grabbing(self, links):
        parser = ParsingWebsite()
        if isinstance(links, str):
            links = list(links)
        unused = []
        for reference in links:
            connect = Page(uri = reference)
            header = connect.get_document().info()
            if header.dict['content-type'].find('text/html') != -1:
                parser.set_uri(connect.get_uri())
                rules = parser.parsing_css(connect.get_html())
                website = []
                for rule_uri in rules:
                    website.append({'uri':rule_uri, 'unused':rules[rule_uri].get_rules()})
                unused.append({'uri':reference, 'unused':website})
                parser.clear()
        return unused

class Website:
    def grabbing(self, link, depth):
        unused = []
        parser = ParsingWebsite()
        spider = Crawler()
        spider.grabbing(uri = link, depth = depth)
        items = spider.stack()
        for stack in items.keys():
            page = items.get(stack)['page']
            if page.status() == 200 and page.get_html():
                parser.set_uri(page.get_uri())
                parser.parsing_css(content = page.get_html())

        website = []
        rules = parser.get_unused_rules()
        if rules:
            for rule_uri in rules:
                website.append({'uri':rule_uri, 'unused':rules[rule_uri].get_rules()})
        unused.append({'uri':link, 'unused':website})
        parser.clear()
        
        return unused
