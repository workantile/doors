print("Using fake GPIO driver.")

BOARD = "board"
IN    = "input"
OUT   = "output"

def cleanup():
	print("> GPIO: cleaning up!")

def output(pin, voltage):
	state = "on" if (voltage == 1) else "off"
	print("> GPIO setting pin %s to %s." % (pin, state))

def setmode(mode):
	print("> GPIO setting mode: %s." % mode)

def setup(pin, iomode):
	print("> GPIO setting up pin: %s, %s." % (pin, iomode))
