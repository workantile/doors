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
		val = random.randint(0, 5)
		if val == 0:
			return "ERROR".encode()
		elif val < 4:
			return "OK".encode()
		raise Exception("Test Network Exception")


def urlopen(url):
	print("> URLLIB: opening url %s" % url)
	return Request(url)
