#!/usr/bin/env python

####################

import re

#####################

from mangaparsers.parser import Parser
from util import getSourceCode

#####################

class MangaReader(Parser):

	re_getSeries = re.compile('<li><a href="([^"]*)">([^<]*)</a>')
	re_getChapters = re.compile('<a href="([^"]*)">([^<]*)</a>([^<]*)</td>')
	re_getPage = re.compile("<option value=\"([^']*?)\"[^>]*>\s*(\d*)</option>")
	re_getImage = re.compile('img id="img" .* src="([^"]*)"')
	re_getMaxPages = re.compile('</select> of (\d*)(\s)*</div>')

	def parseSite(self):
		print('Beginning MangaReader check: %s' % self.manga)
		
		url = 'http://www.mangareader.net/alphabetical'

		source = getSourceCode(url)
		allSeries = MangaReader.re_getSeries.findall(source[source.find('series_col'):])

		keyword = self.selectFromResults(allSeries)

		url = 'http://www.mangareader.net%s' % keyword
		source = getSourceCode(url)

		self.chapters = MangaReader.re_getChapters.findall(source)
		
		lowerRange = 0
	
		for i in range(0, len(self.chapters)):
			self.chapters[i] = ('http://www.mangareader.net%s' % self.chapters[i][0], '%s%s' % (self.chapters[i][1], self.chapters[i][2]))
			print('(%i) %s' % (i + 1, self.chapters[i][1]))

		self.chapters_to_download = self.selectChapters(self.chapters)

	def downloadChapter(self, downloadThread, max_pages, url, manga_chapter_prefix, current_chapter):
		pageIndex = 0
		for page in MangaReader.re_getPage.findall(getSourceCode(url)):
			if (self.verbose_FLAG):
				print(self.chapters[current_chapter][1] + ' | ' + 'Page %s / %i' % (page[1], max_pages))

			pageUrl = 'http://www.mangareader.net' + page[0]
			self.downloadImage(downloadThread, page[1], pageUrl, manga_chapter_prefix)
			pageIndex = pageIndex + 1
