print("Using fake urllib module.")

import random

class Request:
	def __init__(self, url):
		self.url = url

	def __enter__(self):
		return self

	def __exit__(self, type, value, tb):
		pass

	def read(self):
		if random.randint(0, 1) == 0:
			return "OK".encode()
		return "ERROR".encode()



def urlopen(url):
	print("> URLLIB: opening url %s" % url)
	return Request(url)
