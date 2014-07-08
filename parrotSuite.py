import os
import json
import datetime
import twitter
import echo
import squawk
import metrics

"""
ParrotSuite initializes settings for the driver including:
    - application settings from config.txt
    - path
    - debug settings

ParrotSuite grabs the bots from PARROTDIR

ParrotSuite contains classes:
    - User
    - Status
"""


DEBUG =  True

# Set path
PARROTPATH = os.getenv('PARROTPATH')
os.chdir(PARROTPATH)

# Grab settings from path
SETTINGS = {}
for line in open(PARROTPATH + 'config.txt'):
    if '//' not in line[0:1]:
        x,y = line.split('=')
        SETTINGS[x.strip()] = y.strip()

# Initialize time
NOW = datetime.datetime.now()

def botList():
    return [x for x in os.listdir(PARROTPATH) if os.path.isdir(x) and 'bot' in x]

class User:
    def __init__(self, path):
        self.path = path
        settings = {}
        
        for line in open(self.path + 'parrot.cfg'):
            x,y = line.split('=')
            settings[x.strip()] = y.strip()

            self.settings =  settings
        
        self.t = self.initializeTwitter()

        self.statuses = self.grabStatuses()

    def initializeTwitter(self):
        OTOKEN = SETTINGS['OTOKEN']
        OSECRET = SETTINGS['OSECRET']
        CONSKEY = self.settings['CONSKEY']
        CONSSECRET = self.settings['CONSSECRET']
        # Initialize twitter
        try:
            t = twitter.Twitter(
                auth=twitter.OAuth(OTOKEN, OSECRET, CONSKEY, CONSSECRET)
            )
        except Exception as e:
            print("Twitter failed")
            print(str(e))
            exit
        return t


    def grabStatuses(self):
        # Grab statuses
        try:
            statuses = self.t.statuses.home_timeline()
        except Exception as e:
            print('ERR: ' + str(e))
            exit(0)

        statusList = []
        for x in statuses:
            statusList.append(tStatus(x))
        return statusList

    def writeEchoCSV(self, echo):
        # Convert values to string then add them to CSV file
        with open(self.path + "echo.csv", "a") as myfile:
            myfile.write('\n' + echo.string)
        myfile.close


    def postStatus(self, status):
        try:
            if DEBUG:
                print("ECHO POST HAS BEEN DISABLED DUE TO DEBUG")
            else:
                self.t.statuses.update(status=status.text)
        except Exception as e:
            print("Failed to post this echo:")
            print(echo)
            print(e)

    def __repr__(self):
        res = "PATH: " + self.path

        res += "\nSettings: "
        for x in self.settings.keys():
            res += '\n  ' + x + ": " + self.settings[x]

        res += "\nLast post:"
        res += str(self.statuses[0].text)
        res += "\n (" + str(self.statuses[0].age) + "s old)"
        return res

# tStatus = twitter status
class tStatus:
    def __init__(self, status):
        self.text = status.get('text')
        self.created_at = status.get('created_at')
        self.age = self.measureAge()

        self.id_str = status.get('id_str')
        self.in_reply_to_user_id_str = status.get('in_reply_to_user_id_str')
        self.in_reply_to_status_id = status.get('in_reply_to_status_id')
        self.in_reply_to_status_id_str = status.get('in_reply_to_status_id_str')
        self.contributors = status.get('contributors')
        self.retweeted = status.get('retweeted')
        self.lang = status.get('lang')
        self.geo = status.get('geo')
        self.status = status.get('status')
        self.favorite_count = status.get('favorite_count')
        self.id = status.get('id')
        self.truncated = status.get('truncated')
        self.coordinates = status.get('coordinates')
        self.in_reply_to_user_id = status.get('in_reply_to_user_id')
        self.in_reply_to_screen_name = status.get('in_reply_to_screen_name')
        self.retweet_count = status.get('retweet_count')
        self.favorited = status.get('favorited')

        self.source = status.get('source')
        self.place = status.get('place')
        self.entities = status.get('entities')
        self.user = status.get('user')

    def measureAge(self):
        """ Returns the age of a status (in seconds)"""
        strTime = ' '.join(
            self.created_at.split(' ')[:4]) + ' ' + str(NOW.year)
        statusTime = datetime.datetime.strptime(strTime, '%a %b %d %H:%M:%S %Y')
        age =  NOW - statusTime
        return age.seconds

class Timeline:
    def __init__(t):
        self.t = t
        self.statuses = []
        self.lastStatus = None