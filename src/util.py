#!/usr/bin/env python

####################

import gzip
import re
import string
import StringIO
import time
import urllib2

####################

# something seriously wrong happened
class FatalError(Exception):
	pass

def fixFormatting(s):
	"""
	Special character fix for filesystem paths.
	"""
	
	for i in string.punctuation:
		if(i != '-' and i != '.'):
			s = s.replace(i, '')
	return s.lower().lstrip('.').strip().replace(' ', '_')

# overwrite default user-agent so we can download
#class AppURLopener(urllib.FancyURLopener):
#	version = 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.14 Safari/534.3'


def getSourceCode(url, maxRetries=5, waitRetryTime=5):
	# overwrite default user-agent so we can download
	UserAgent = 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.14 Safari/534.3'
	
	"""
	While loop to get around server denies for info or minor disconnects.
	"""
	while True:
		ret = None
		try:
			# Modifies the user agent and notifies the server we accept gzip encoding
			request = urllib2.Request(url) 
			request.add_header('User-Agent', UserAgent)
			request.add_header('Accept-encoding', 'gzip')
			opener = urllib2.build_opener()
			f = opener.open(request)
			
			encoding = f.headers.get('Content-Encoding')
					
			if encoding == None:
				ret = f.read()
			else:
				encoding = encoding.upper()
				if encoding == 'GZIP': 
					compressedstream = StringIO.StringIO(f.read()) 
					gzipper = gzip.GzipFile(fileobj=compressedstream)
					ret = gzipper.read()
				else:
					raise FatalError('Uknown HTTP Encoding returned')
		except urllib2.URLError, e:
			if e.code == 404:
				ret = ""
				break
			else:
				# Check maxrRetries. If we should try again, wait waitRetryTime seconds
				if (maxRetries > 0):
					time.sleep(waitRetryTime)
					maxRetries = maxRetries - 1
				else:
					# We have already tries maxRetries times. Just break to avoid an infinite loop
					break
		else:
			break

	return ret

def isImageLibAvailable():
	try:
		from ConvertPackage.ConvertFile import convertFile
	except ImportError:
		return False
	else:
		return True
	
def zeroFillStr(inputString, numOfZeros):
	startIndex = []
	endIndex = []
	
	outputString = inputString
	
	for m in re.finditer('\d+', outputString):
		startIndex.append(m.start())
		endIndex.append(m.end())
	
	# Starting from the end converts the found substrings to their zero filled counterparts
	# 
	# Converting from the end of the string will not move the locations of
	# any of the prior substrings (Thoses in the string before the one 
	# currently being converted. 
	while ((len(startIndex) > 0) and (len(endIndex))):
		startIdx = startIndex.pop()
		endIdx = endIndex.pop()
		outputString = outputString[:startIdx] + outputString[startIdx:endIdx].zfill(numOfZeros) + outputString[endIdx:]	
	
	return outputString	

#=========================
#
# XML Helper Functions
#
#=========================

def getText(node):
	rc = []
	for node in node.childNodes:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)		
			
		return ''.join(rc)
#		return ''.join([node.data for node in nodelist if node.nodeType == node.TEXT_NODE])			

def setText(dom, node, text):
	for currNode in node.childNodes:
		if currNode.nodeType == currNode.TEXT_NODE:
			currNode.data = text
			return

	# If this code is executed, it means that the loop failed to find a text node
	# A new text needs to be created and appended to this node
	textNode = dom.createTextNode(text) 	
	node.appendChild(textNode)

def updateNode(dom, node, tagName, text):
	if (len(node.getElementsByTagName(tagName)) > 0):
		updateNode = node.getElementsByTagName(tagName)[0]
	else:
		# Node Currently Does have a timeStamp Node Must add one
		updateNode = dom.createElement(tagName)
		node.appendChild(updateNode)
		
	setText(dom, updateNode, text) 	
	