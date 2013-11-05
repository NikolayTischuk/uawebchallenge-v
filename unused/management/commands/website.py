from optparse import make_option
from django.core.management.base import BaseCommand

import time

from unused.service.uaweb.parser import ParsingWebsite
from unused.service.uaweb.spider import Crawler, Page
from unused.service.uaweb.logg import Loggs

class Command(BaseCommand):
    help = '''
    Out unused css rules 
    Example: 0 http://example.com/
    '''
    args = 'num url'

    def handle(self, *args, **options):
        print '... {0}'.format('website '.ljust(73,'.'))
        
        reference = args[1]
        reference = 'http://uawebchallenge.com/'
        t = time.time()
        if not str(args[0]).isdigit():
            print self.help
        else:
            unused = []
            parser = ParsingWebsite()
            spider = Crawler()
            spider.grabbing(uri = reference, depth = 50)
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
            unused.append({'uri':reference, 'unused':website})
            parser.clear()
        print unused
        print "time: %f" % (time.time()-t)
