#!/usr/bin/env python

####################

import gzip
import io
import random
import re
import string
import time
###################

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

####################

# overwrite user agent for spoofing, enable GZIP
urlReqHeaders = {'User-agent': """Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.14 Safari/534.3""",
                 'Accept-encoding': 'gzip'}

####################

class FatalError(Exception):
    pass


def fixFormatting(s):
    """
    Special character fix for filesystem paths.
    """

    for i in string.punctuation:
        if(i != '-' and i != '.'):
            s = s.replace(i, '')
    return s.lower().lstrip('.').strip().replace(' ', '.')


def getSourceCode(url, maxRetries=5, waitRetryTime=5):
    """
    Retrieves the source code of a given URL.
    Accepts GZIP compression.
    Loops to get around server denies for info or minor disconnects.
    """

    ret = None
    request = urllib2.Request(url, headers=urlReqHeaders)
    numTries = 0

    while (ret == None):
        try:
            response = urllib2.urlopen(request)
            encoding = response.headers.get('Content-Encoding')

            if encoding == None:
                ret = response.read()
            else:
                if encoding.upper() == 'GZIP':
                    compressedstream = io.BytesIO(response.read())
                    gzipper = gzip.GzipFile(fileobj=compressedstream)
                    ret = gzipper.read()
                else:
                    raise FatalError('Unknown HTTP Encoding returned')
        except urllib2.URLError:
            if (numTries == maxRetries):
                break
            else:
                # random dist. for further protection against anti-leech
                # idea from wget
                time.sleep(random.uniform(0.5 * waitRetryTime, 1.5 * waitRetryTime))
                numTries += 1

    return ret