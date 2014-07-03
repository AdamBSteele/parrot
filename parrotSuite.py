import os
import Twitter

# Set path
PARROTPATH = os.getenv('PARROTPATH')
os.chdir(PARROTPATH)

# Grab settings from path
SETTINGS = {}
for line in open(PARROTPATH + 'config.txt'):
    if '//' not in line[0:1]:
        x,y = line.split('=')
        SETTINGS[x.strip()] = y.strip()

class User:
    def __init__(self, path):
        self.path = path

        settings = {}
        for line in open(self.path + 'parrot.cfg'):
            x,y = line.split('=')
            settings[x.strip()] = y.strip()

            self.settings =  settings
        self.initializeTwitter()

    def initializeTwitter(self):
        OTOKEN = SETTINGS['OTOKEN']
        OSECRET = SETTINGS['OSECRET']
        CONSKEY = self.settings['CONSKEY']
        CONSSECRET = self.settings['CONSSECRET']
        # Initialize twitter
        try:
            t = Twitter(
                auth=OAuth(OTOKEN, OSECRET, CONSKEY, CONSSECRET)
            )
        except Exception as e:
            print "Twitter failed"
            print str(e)
            exit
        print "TWITTER SUCCESS"

    def __repr__(self):
        res = "PATH: " + self.path

        res += "\nSettings: "
        for x in self.settings.keys():
            res += '\n  ' + x + ": " + self.settings[x]

        return res




def getTimeline(settings):
    pass


class Status:
    def __init__(status):
        self.text = status.get('text')

class Timeline:
    def __init__(t):
        self.t = t
        self.statuses = []
        self.lastStatus = None
