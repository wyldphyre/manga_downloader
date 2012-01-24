#!/usr/bin/env python

####################

import gzip
import io
import random
import string
import time
###################

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

####################

# overwrite user agent for spoofing, enable GZIP
urlReqHeaders = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7'
    ,
    'Accept-encoding': 'gzip'}

####################

class FatalError(Exception):
    pass


def fixFormatting(s):
    """
    Special character fix for filesystem paths.
    """

    for i in string.punctuation:
        if i != '-' and i != '.':
            s = s.replace(i, '')
    return s.lower().lstrip('.').strip().replace(' ', '.')


def getSourceCode(url, maxRetries=5, waitRetryTime=5):
    """
    Retrieves the source code of a given URL.
    Accepts GZIP compression.
    Loops to get around server denies for info or minor disconnects.
    """

    sourceCode = None
    request = urllib2.Request(url, headers=urlReqHeaders)
    numTries = 0

    while sourceCode is None:
        try:
            response = urllib2.urlopen(request)
            encoding = response.headers.get('Content-Encoding')

            if encoding is None:
                sourceCode = response.read()
            else:
                if encoding.upper() == 'GZIP':
                    compressedStream = io.BytesIO(response.read())
                    gzipper = gzip.GzipFile(fileobj=compressedStream)
                    sourceCode = gzipper.read()
                else:
                    raise FatalError('Unknown HTTP Encoding returned')
        except urllib2.URLError:
            if numTries == maxRetries:
                break
            else:
                # random dist. for further protection against anti-leech
                # idea from wget
                time.sleep(random.uniform(0.5 * waitRetryTime, 1.5 * waitRetryTime))
                numTries += 1

    return sourceCode