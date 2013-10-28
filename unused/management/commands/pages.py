from optparse import make_option
from django.core.management.base import BaseCommand

import time

from unused.service.uaweb.parser import ParsingWebsite
from unused.service.uaweb.mapper import Page

class Command(BaseCommand):
    help = '''
    Out unused css rules 
    Example url: http://example.com/
    Example url: http://example1.com/ http://example2.com/
    '''
    args = '<url url ... url>'

    def handle(self, *args, **options):
        print 'pages'
        t = time.time()
        parser = ParsingWebsite()
        for reference in args:
            print "Parsion page: %s "%(reference)
            page = Page(uri = reference)
            header = page.get_document().info()
            if header.dict['content-type'].find('text/html') != -1:
                parser.set_uri(page.get_uri())
                parser.parsing_css(page.get_html())
                unused = parser.get_unused_rules()
                for link in unused:
                    rule = unused[link]
                    print "\t%s"%(', '.join(rule.get_rules()))
                parser.clear()
        print "time: %f" % (time.time()-t)
