from optparse import make_option
from django.core.management.base import BaseCommand

import time

from unused.service.uaweb.parser import ParsingWebsite
from unused.service.uaweb.mapper import Scheme, Page
from unused.service.uaweb.logg import Loggs

class Command(BaseCommand):
    help = '''
    Out unused css rules 
    Example: 0 http://example.com/
    '''
    args = 'num url'

    def handle(self, *args, **options):
        print 'website'
        t = time.time()
        if not str(args[0]).isdigit():
            print self.help
        else:
            parser = ParsingWebsite()
            scheme = Scheme(uri = args[1])
            for page in scheme.building(args[0]):
                Loggs().logger.info("Parsing: %s "%(page.get_uri()))
                parser.set_uri(page.get_uri())
                parser.parsing_css(content = page.get_html())
            website = []
            rules = parser.get_unused_rules()
            print args[1]
            if rules:
                for rule_uri in rules:
                    print "\t%s"%(', '.join(rules[rule_uri].get_rules()))
            else:
                print None
            parser.clear()
        print "time: %f" % (time.time()-t)
