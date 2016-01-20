print("Using fake serial driver.")

import random
import string

class Serial:
	def __init__(self, path, baudrate, timeout):
		self.path       = path
		self.baudrate   = baudrate
		self.timeout    = timeout
		self.generated  = set()
		self.exceptions = True

	def gen_key(self, count):
		lst = [random.choice(string.hexdigits) for n in range(count - 2)]
		ret = "A" + "".join(lst) + "D"
		print("> Serial generated key: %s" % ret)
		self.generated.add(ret)
		return ret

	def old_key(self, count):
		if len(self.generated) == 0:
			return self.gen_key(count)
		index = random.randint(0, len(self.generated) - 1)
		ret = list(self.generated)[index]
		print("> Serial using old key: %s" % ret)
		return ret;

	def read(self, count):
		val = random.randint(0, 5)
		if val == 0:
			return self.gen_key(count).encode()
		elif val in {1, 2}:
			return self.old_key(count).encode()
		elif val in {3, 4} or self.exceptions == False:
			return "".encode()
		raise Exception("Test Serial Exception")

	def reset_input_buffer():
		pass
