import argparse
from parrotSuite import *
import random

DEBUG_SETTINGS = False

"""
The driver is run every 3 minutes on a cronJob.
The driver iterates through all bots in PARROTDIR
  to execute its (3) main tasks:
	- Post echoes
		- Remove posted echoes
		- Remove old echoes
	- Post squawks
		- Count down squawk counter
		- Remove dead squawks
	- Update metrics
"""



def main():
    args = parseArgs()
    for bot in botList():
        fullPath = PARROTPATH + bot + '/'
        user = User(fullPath)

        # For adding echoes to test bot
        if 'bot1' in bot:
	        for _ in range(0, args.createEchoes):
	            newEcho = createTestEcho()            
	            user.writeEchoCSV(newEcho)

        echoPosted = echo.checkForAutoPost(user, fullPath)
        
        if not echoPosted:
            squawk.run(user)

        metrics.run(user)


def parseArgs():
    parser = argparse.ArgumentParser(description='Driver for parrotSuite.')
    parser.add_argument('-ce', type=int, default=0, dest='createEchoes',
                       help='-ce [num] to insert <num> echoes in bot1\'s CSV')
    args = parser.parse_args()
    return args

def createTestEcho():
    # For creating a test echo
    rand_int = str(random.randint(10000, 99999))
    time_addition = random.randint(200, 600)
    text = "testEcho" + rand_int
    location = rand_int
    time = NOW + datetime.timedelta(0,time_addition)
    gHash = True
    lHash = True
    categories = ['soccer', 'foosball', rand_int]

    print("Creating echo (seed %s: , time_diff: %ds)"  % (rand_int, time_addition))

    newEcho = echo.Echo()
    newEcho.initFromValues(text, time, location, gHash, lHash, categories)
    return newEcho


if __name__ == '__main__':
    main()