import os
PARROTPATH = os.getenv('PARROTPATH')
os.chdir(PARROTPATH)
import echo
import squawk
import metrics
from parrotSuite import *

def main():
	#settings = getSettings()
	for bot in [x for x in os.listdir(PARROTPATH) if os.path.isdir(x)]:
		echo.run(bot)
		squawk.run(bot)
		metrics.run(bot)

if __name__ == '__main__':
	print "START"
	main()