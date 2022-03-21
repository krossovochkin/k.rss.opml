from xml.etree import ElementTree as et
import sys
import itertools
import os
import urllib.parse

def deploy(input, output):
	rss_items = parseRssItems(input)
	
	printDisclaimer(input, output)
	
	for key, group in itertools.groupby(rss_items, lambda x : x.folder):
		printSection(key, list(group), output)
			
def parseRssItems(input):
	xmlp = et.XMLParser(encoding = "utf-8")
	tree = et.parse(input, parser=xmlp)
	root = tree.getroot()

	body = root.find("body")

	rss_items = []

	for folder in body.findall("outline"):
		for sub in folder.findall("outline"):
			rss_items.append(
				RssItem(
					folder.attrib["title"],
					sub.attrib["title"],
					sub.attrib["htmlUrl"]
				)
			)
			
	return rss_items
	
def printDisclaimer(input, output):
	print(
f"""# Krossovochkin RSS Subscriptions

This repository contains OPML file with subscriptions list of blogs in various areas (Android, Kotlin etc.) which I use to be up-to-date.  
RSS is still the best way to get new content as soon as possible.  
To use RSS and this list one should download [OPML file](https://raw.githubusercontent.com/krossovochkin/k.rss.opml/master/{urllib.parse.quote(input)}) and import with with [Inoreader](https://www.inoreader.com/blog/2014/04/opml-import-additions.html) or [Feedly](https://blog.feedly.com/opml/)

Optionally, one can take a look at the list of resources group by topic below.
""", file = output)
	
def printSection(caption, items, output):
	printCaption(caption, output)
	printTable(items, output)
	print("\n", file = output)
	
def printCaption(caption, output):
	print(caption.replace("|", "\|"), file = output)
	print("---", file = output)
		
def printTable(rss_items, output):
	print("|Title|URL|", file = output)
	print("|--|--|", file = output)
			
	for item in rss_items:
		title = item.title.replace("|", "\|")
		print(f"|{title}|[Link]({item.url})|", file = output)
	
class RssItem:
	def __init__(self, folder, title, url):
		self.folder = folder
		self.title = title
		self.url = url
		
	def isMedium(self):
		return "medium.com" in self.url
	
	def isReddit(self):
		return "reddit.com" in self.url
		
	def __str__(self):
		return f"{self.folder},{self.title},{self.url},{self.isMedium()},{self.isReddit()}"
	
def findOpmlFile():
	for file in os.listdir(os.getcwd()):
		if file.endswith(".xml"):
			return file
			
	return ""
	
if __name__ == "__main__":
	output = open("README.md", 'w', encoding="utf-8")
	
	deploy(findOpmlFile(), output)
