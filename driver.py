from parrotSuite import *
import echo
import squawk
import metrics

def main():
    if SETTINGS.get('DEBUG') == "TRUE":
        for x in SETTINGS.keys():
            print (x + ": " + SETTINGS[x])

    for bot in botList():
        fullPath = PARROTPATH + bot + '/'
        user = User(fullPath)
        if SETTINGS.get('DEBUG') == "TRUE":
            print user
        # user = User(userSettings, bot)
        # getTimeline(userSettings)
        # echo.run(userSettings)
        # squawk.run(userSettings)
        # metrics.run(userSettings)

def botList():
    return [x for x in os.listdir(PARROTPATH) if os.path.isdir(x) and 'git' not in x]

if __name__ == '__main__':
    print "START"
    main()