import argparse
import os
import random

from parrotSuite import *
import datetime
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

TODO:
    unit testing
    Flask UI
"""


def main():
    args = parseArgs()
    for bot in botList():
        fullPath = PARROTPATH + '/' + bot
        user = User(fullPath)

        # If flag is set, create & test an echo
        if args.createEchoes and 'bot1' in bot:
            testEchoCreation(user, args.createEchoes)

        # check to see if an echo needs to be posted
        echoPosted = checkForAutoPost(user)

        # If you didn't post an echo, check if it's time to squawk
        if not echoPosted:
            check(user)

        # No matter what, grab whatever metrics you can
        runsquawk(user)


def parseArgs():
    parser = argparse.ArgumentParser(description='Driver for parrotSuite.')
    parser.add_argument('-ce', type=int, default=0, dest='createEchoes',
                        help='-ce [num] to insert <num> echoes in bot1\'s CSV')
    args = parser.parse_args()
    return args


# Create an echo for sometime in the next 3 - 10 minutes.
# Then put it in the CSV
def createTestEcho():
    rand_int = str(random.randint(10000, 99999))
    time_addition = random.randint(200, 600)
    text = "testEcho" + rand_int
    location = str(rand_int)
    time = NOW + datetime.timedelta(0, time_addition)
    gHash = 'True'
    lHash = 'True'
    categories = 'soccer, football'
    time = datetime.datetime.strftime(time, '%a %b %d %H:%M:%S %Y')
    print("Creating echo (seed: %s, time_diff: %ds)"
          % (rand_int, time_addition))
    csvString = '||||'.join([text, location, gHash, lHash, categories, time])
    print("CSVstring: \n %s" % csvString)
    newEcho = Echo(csvString)
    return newEcho


def testEchoCreation(user, count):
    for _ in range(0, count):
        newEcho = createTestEcho()
        user.writeEchoCSV(newEcho)


def checkForAutoPost(user):
    echoList = readEchoes(user.path)
    for echo in echoList:
        if echo.timeToPost():
            print("POSTING")
            print(echo)
            user.postStatus(echo)
            return True
        print(echo)
    return False


def readEchoes(path):
    res = []
    lines = []
    for line in open(path + '/echo.csv'):
        if len(line.split('||||')) == 6:
            newEcho = Echo(line.strip())
            if NOW > newEcho.postTime:
                print("OLD ECHO: " + newEcho.text)
            else:
                lines.append(line)
                res.append(newEcho)

    # Write all non-posted lines
    with open(path + '/echo.csv', 'w') as myfile:
        for line in lines:
            myfile.write(line)

    print("Found %d non-old echoes" % len(res))
    return res


def runsquawk(user):
    newStatus = grabSquawk(user)
    user.postStatus(newStatus)


def check(user):
    print("Squawk Check")
    lastStatus = user.statuses[0]

    freqInMinutes = int(user.settings['frequency']) * 60
    if lastStatus.measureAge() < freqInMinutes:
        squawk.run(user)


def grabSquawk(user):

    res = []
    lines = []
    lineNo = 0
    for line in open(user.path + '/squawk.csv'):
        try:
            newEcho = Echo(line.strip())
            # Only keep an echo if it's not old
            if NOW < newEcho.time:
                lines.append(line)
                res.append(newEcho)
        except Exception as e:
            print("squawk failed on line %d" % lineNo)
            print(e)
        lineNo += 1

    # Write all non-posted lines
    with open(user.path + '/squawk.csv', 'w') as myfile:
        for line in lines:
            myfile.write(line)

    print("Found %d non-old echoes" % len(res))
    return res



if __name__ == '__main__':
    main()
