#!/usr/bin/env python

# Copyright (C) 2010-2012
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

##########

import optparse
import os
import sys

##########
from parsers.thread import SiteParserThread
from util import fixFormatting
##########

VERSION = 'v0.8.8'

siteDict = {
    '': '[mf]',
    '1': '[mf]',
    '2': '[ow]',
    '3': '[mr]'
}

##########

class InvalidSite(Exception):
    pass


def printLicenseInfo():
    print("\nProgram: Copyright (c) 2010-2012. GPL v3 (http://www.gnu.org/licenses/gpl.html).")
    print("Icon:      Copyright (c) 2006. GNU Free Document License v1.2 (Author:Kasuga).")
    print("           http://ja.wikipedia.org/wiki/%E5%88%A9%E7%94%A8%E8%80%85:Kasuga\n")

##########

def isValidNumThreads(number):
    return number.isdigit() and number > 0


def lookUpSiteCode(site):
    try:
        return siteDict[site]
    except KeyError:
        raise InvalidSite('Site selection invalid.')


def main():
    printLicenseInfo()

    # for easier parsing, adds free --help and --version
    # optparse (v2.3-v2.7) was chosen over argparse (v2.7+) for compatibility (and relative similarity) reasons
    # and over getopt(v?) for additional functionality
    parser = optparse.OptionParser(usage='usage: %prog [options] <manga name>',
        version=('Manga Downloader %s' % VERSION))

    parser.set_defaults(
        all_chapters_FLAG=False,
        downloadFormat='.cbz',
        downloadPath='DEFAULT_VALUE',
        overwrite_FLAG=False,
        verbose_FLAG=False,
        maxChapterThreads=3)

    parser.add_option('--all',
        action='store_true',
        dest='all_chapters_FLAG',
        help='Download all available chapters.')

    parser.add_option('-d', '--directory',
        dest='downloadPath',
        help='The destination download directory.  Defaults to the directory of the script.')

    parser.add_option('--overwrite',
        action='store_true',
        dest='overwrite_FLAG',
        help='Overwrites previous copies of downloaded chapters.')

    parser.add_option('-t', '--threads',
        dest='maxChapterThreads',
        help='Limits the number of chapter threads to the value specified.')

    parser.add_option('--verbose',
        action='store_true',
        dest='verbose_FLAG',
        help='Verbose Output.')

    parser.add_option('-z', '--zip',
        action='store_const',
        dest='downloadFormat',
        const='.zip',
        help='Downloads using .zip compression.  Omitting this option defaults to %default.')

    (options, args) = parser.parse_args()

    if not isValidNumThreads(options.maxChapterThreads):
        options.maxChapterThreads = parser.defaults[maxChapterThreads]

    if len(args) == 0:
        parser.error('Manga not specified.')

    SetDownloadPathToName_Flag = False
    if len(args) > 0:
        # Default Directory is the ./MangaName
        if options.downloadPath == 'DEFAULT_VALUE':
            SetDownloadPathToName_Flag = True

    # Changes the working directory to the script location
    os.chdir(os.path.dirname(sys.argv[0]))

    threadPool = []
    for manga in args:
        print( manga )
        options.manga = manga

        if SetDownloadPathToName_Flag:
            options.downloadPath = ('./' + fixFormatting(options.manga))

        options.downloadPath = os.path.realpath(options.downloadPath) + os.sep

        # site selection
        print('\nWhich site?\n(1) MangaFox\n(2) OtakuWorks\n(3) MangaReader\n')

        site = raw_input()

        options.site = lookUpSiteCode(site)

        threadPool.append(SiteParserThread(options, None, None))

    for thread in threadPool:
        thread.start()
        thread.join()

if __name__ == '__main__':
    main()