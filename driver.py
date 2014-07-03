import os
PARROTPATH = os.getenv('PARROTPATH')
os.chdir(PARROTPATH)
import echo
import squawk
import metrics
from parrotSuite import *

SETTINGS = getSettings(PARROTPATH + 'config.txt')

def main():
	for bot in [x for x in os.listdir(PARROTPATH) if os.path.isdir(x) and 'git' not in x]:
		userSettings = getUserSettings(PARROTPATH + bot + '/parrot.cfg')
		getTimeline(userSettings)
		echo.run(userSettings)
		squawk.run(userSettings)
		metrics.run(userSettings)


if __name__ == '__main__':
	print "START"
	main()