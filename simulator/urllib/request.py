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
		val = random.randint(0, 2)
		if val == 0:
			return "OK".encode()
		elif val == 1:
			return "ERROR".encode()
		raise Exception('Test Exception')


def urlopen(url):
	print("> URLLIB: opening url %s" % url)
	return Request(url)
