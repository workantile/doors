print("Using fake serial driver.")

import random
import string

class Serial:
	def __init__(self, path, baudrate, timeout):
		self.path     = path
		self.baudrate = baudrate
		self.timeout  = timeout

	def read(self, count):
		lst = [random.choice(string.hexdigits) for n in range(count - 2)]
		ret = "A" + "".join(lst) + "D"
		return ret.encode()

	def flushInput(self):
		pass
