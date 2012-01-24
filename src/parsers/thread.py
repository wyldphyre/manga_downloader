#!/usr/bin/env python

#####################

import threading
import os
#####################

from parsers.base import SiteParserBase
from parsers.factory import SiteParserFactory

#####################

class SiteParserThread( threading.Thread ):

    def __init__ ( self, optDict, dom, node ):
        threading.Thread.__init__(self)

        for elem in vars(optDict):
            setattr(self, elem, getattr(optDict, elem))

        self.siteParser = SiteParserFactory.getInstance(self)
        self.siteParser.parseSite()

        # create download directory if not found
        try:
            if os.path.exists(self.downloadPath) is False:
                os.mkdir(self.downloadPath)
        except OSError:
            print("""Unable to create download directory. There may be a file
                with the same name, or you may not have permissions to write
                there.""")
            raise
        print('\n')

    def run (self):
        try:
            self.siteParser.download()

        except SiteParserBase.MangaNotFound as Instance:
            print("Error: Manga ("+self.manga+")")
            print(Instance)
            print("\n")
            return