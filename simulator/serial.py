print("Using fake serial driver.")

import random
import string

class Serial:
	def __init__(self, path, baudrate, timeout):
		self.path     = path
		self.baudrate = baudrate
		self.timeout  = timeout

	def gen_key(self, count):
		lst = [random.choice(string.hexdigits) for n in range(count - 2)]
		return "A" + "".join(lst) + "D"

	def read(self, count):
		val = random.randint(0, 4)
		if val == 0 or val == 1:
			return "".encode()
		elif val == 2 or val == 3:
			ret = self.gen_key(count)
			print("> Serial generating key: %s" % ret)
			return ret.encode()
		raise Exception("Test Serial Exception")

	def flushInput(self):
		pass
