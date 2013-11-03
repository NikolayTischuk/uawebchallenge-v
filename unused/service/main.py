#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ntischuk

import sys

from uaweb.parser import ParsingWebsite
from uaweb.mapper import Scheme
from uaweb.spider import Spider

if __name__ == '__main__':
    import time
    t = time.time()
    scheme = Scheme(uri = 'http://blog.ntischuk.com/')
    scheme.building(0)
    print "time: %f" % (time.time()-t)
    sys.exit(1)