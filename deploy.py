from xml.etree import ElementTree as et
import sys
import itertools
import os

def deploy(input, output):
	rss_items = parseRssItems(input)
	
	printDisclaimer(output)
	
	for key, group in itertools.groupby(rss_items, lambda x : x.folder):
		printSection(key, list(group), output)
		
	printSection("Medium", filter(lambda x : x.isMedium(), rss_items), output)
	printSection("Reddit", filter(lambda x : x.isReddit(), rss_items), output)
			
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
					sub.attrib["xmlUrl"]
				)
			)
			
	return rss_items
	
def printDisclaimer(output):
	print(
"""# Krossovochkin RSS Subscriptions

This repository contains OPML file with subscriptions list of blogs in various areas (Android, Kotlin etc.) which I use to be up-to-date.  
RSS is still the best way to get new content as soon as possible.  
To use RSS and this list one should download [OPML file]() and import with with [Inoreader](https://www.inoreader.com/blog/2014/04/opml-import-additions.html) or [Feedly](https://blog.feedly.com/opml/)

Optionally, one can take a look at the list of resources below.  
They are grouped by topic. Additionally at the bottom there are resources hosted on Medium.com and on Reddit.com.
""", file = output)
	
def printSection(caption, items, output):
	printCaption(caption, output)
	printTable(items, output)
	print("\n", file = output)
	
def printCaption(caption, output):
	print(caption, file = output)
	print("---", file = output)
		
def printTable(rss_items, output):
	print("|Title|URL|", file = output)
	print("|--|--|", file = output)
			
	for item in rss_items:
		print(f"|{item.title}|[Link]({item.url})|", file = output)
	
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