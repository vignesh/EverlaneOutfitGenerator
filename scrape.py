from bs4 import BeautifulSoup
import urllib2
import platform, sys
from selenium import webdriver
import random

class Everlane:

	def __init__(self): 
		self.womensUrl = "https://www.everlane.com/collections/womens-all"
		self.mensUrl = "https://www.everlane.com/collections/mens-all"
		self.productMapping = {}

	def getProducts(self, url):
		try:
		 	browser = webdriver.PhantomJS(executable_path = 'phantomjs-2.1.1-macosx/bin/phantomjs')
			browser.get(url)
		except Exception as e:
		 	print "Page could not be found: %s" % url
		 	return 

		soup = BeautifulSoup(browser.page_source, "html.parser")
		products = soup.find_all("div", {"class": "product-details"})
		for product in products:
			try:
				productName = product.find_all("h3", {"class": "product__name"})[0].get_text()
				productPrice = product.find_all("span", {"class": "product__price"})[0].get_text()
				productColor = product.find_all("span", {"class": "product__color"})[0].get_text()
				productCategory = self.categorizeMapping(productName)
				self.addProductToMap(productCategory, productName, productPrice, productColor)
			except Exception as e:
				print "Unable to add product to mapping"
				continue 

	def getWomensProducts(self):
		self.getProducts(self.womensUrl)

	def getMensProducts(self):
		self.getProducts(self.mensUrl)

	def getAllProducts(self):
		self.getProducts(self.womensUrl)
		self.getProducts(self.mensUrl)

	def addProductToMap(self, category, name, price, color):
		if category not in self.productMapping:
			self.productMapping[category] = {}
		if name not in self.productMapping[category]:
			self.productMapping[category][name] = set()
			self.productMapping[category][name].add((price, color))
		#add new version of product
		else:
			self.productMapping[category][name].add((price, color))

	def categorizeMapping(self, productName):
		productName = str(productName).lower().split()
		tops = ["crew", "v-neck","hoodie", "jacket", "tee", "polo", "tank", "anorak", "shirt", "long-sleeve"]
		bottoms = ["chino", "jean", "pant", "short", "sweatpant", "oxford", "sweatshort"]
		if any(top in productName for top in tops):
			return "top"
		elif any(bottom in productName for bottom in bottoms):
			return "bottom"
		else:
			return "accessory"

	def prettyPrintMapping(self):
		for category, names in self.productMapping.items():
			print category
			print "***********"
			for name, details in names.items():
				print name
				for price, color in details:
					print "- %s:%s" % (color, price)
				print "___________"

	def randomOutfit(self):
		randomTop = random.choice(self.productMapping["top"].items())
		randomTopName = randomTop[0]
		randomTopDetails = random.sample(randomTop[1], 1)
		randomTopPrice = randomTopDetails[0][0]
		randomTopColor = randomTopDetails[0][1]
		randomBottom = random.choice(self.productMapping["bottom"].items())
		randomBottomName = randomBottom[0]
		randomBottomDetails = random.sample(randomBottom[1], 1)
		randomBottomPrice = randomBottomDetails[0][0]
		randomBottomColor = randomBottomDetails[0][1]
		randomAccessory = random.choice(self.productMapping["accessory"].items())
		randomAccessoryName = randomAccessory[0]
		randomAccessoryDetails = random.sample(randomAccessory[1], 1)
		randomAccessoryPrice = randomAccessoryDetails[0][0]
		randomAccessoryColor = randomAccessoryDetails[0][1]
		totalPrice = self.calculateTotalPrice(randomTopPrice, randomBottomPrice, randomAccessoryPrice)
		print "Top: %s color %s - %s" % (randomTopColor, randomTopName, randomTopPrice)
		print "Bottom: %s color %s - %s" % (randomBottomColor, randomBottomName, randomBottomPrice)
		print "Accessory: %s color %s - %s" % (randomAccessoryColor, randomAccessoryName, randomAccessoryPrice)
		print "Complete Everlane Outfit for only $%s!" % (totalPrice)

	def calculateTotalPrice(self, top, bottom, accessory):
		topPrice = int(top.replace("$", ""))
		bottomPrice = int(bottom.replace("$", ""))
		accessoryPrice = int(accessory.replace("$", ""))
		return topPrice + bottomPrice + accessoryPrice

def main():
	everlaneStore = Everlane()
	everlaneStore.getMensProducts()
	#print everlaneStore.productMapping
	#everlaneStore.getAllProducts()
	#everlaneStore.prettyPrintMapping()
	everlaneStore.randomOutfit()

if __name__ == "__main__":
	main()
