import os
import json
import datetime
import twitter
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
    - tStatus -> the status as pulled from Twitter
    - pStatus -> the common parts of Echoes and Squawks
    - Echo -> pStatus + postTime
    - Squawk -> pStatus + startTime + endTime
"""
# Initialize time
NOW = datetime.datetime.now()

# Frequency of crontab runs.
FREQUENCY = 300


DEBUG =  True

# Set path
PARROTPATH = os.getenv('PARROTPATH')
os.chdir(PARROTPATH)

# Grab settings from path
SETTINGS = {}
for line in open(PARROTPATH + '/config.txt'):
    if '//' not in line[0:1]:
        x,y = line.split('=')
        SETTINGS[x.strip()] = y.strip()


def botList():
    return [x for x in os.listdir(PARROTPATH) if os.path.isdir(x) and 'bot' in x]

class User:
    def __init__(self, path):
        self.path = path
        settings = {}
        
        for line in open(self.path + '/parrot.cfg'):
            x,y = line.split('=')
            settings[x.strip()] = y.strip()

            self.settings =  settings
        
        self.t = self.initializeTwitter()

        self.statuses = self.grabTStatuses()

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


    def grabTStatuses(self):
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
        with open(self.path + "/echo.csv", "a") as myfile:
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

"""
pStatus = parrotStatus

pStatus contains all the variables that are common between echo and squawk,
    which inherit pStatus
"""
class pStatus:
    def __init__(self, text, location, gHash, lHash, categories):
        self.text = text
        self.location = location
        self.gHash = gHash
        self.lHash = lHash
        self.categories = categories

    # The text of the status update (140 chars or less)
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        assert(type(value) == str),\
            "Tried to pass type \'%s\' into pStatus.text" % str(type(value))
        assert(len(value) < 140),\
            "Tried to pass %d char status into pStatus.text" % len(value)
        self._text = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        assert(type(value) == str or type(value) == int),\
            "Tried to pass type \'%s\' into pStatus.location" % str(type(value))
        self._location = str(value)

    @property
    def gHash(self):
        return self._gHash

    @gHash.setter
    def gHash(self, value):
        assert(type(value) == str or type(value) == bool),\
            "Tried to pass type \'%s\' into pStatus.gHash" % str(type(value))
        if type(value) == bool:
            self._gHash = value
        else:
            if 'True' in value:
                self._gHash = True
            elif 'False' in value:
                self._gHash = False
            else:
                self._gHash = False
    
    @property
    def lHash(self):
        return self._lHash

    @lHash.setter
    def lHash(self, value):
        assert(type(value) == str or type(value) == bool),\
            "Tried to pass type \'%s\' into pStatus.lHash" % str(type(value))
        if type(value) == bool:
                self._lHash = value
        else:
            if 'True' in value:
                self._lHash = True
            elif 'False' in value:
                self._lHash = False
            else:
                self._lHash = False

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        assert(type(value) == str or type(value) == list),\
            "Tried to pass type \'%s\' into pStatus.categories" % str(type(value))
        if type(value) == list:
            self._categories = value[:]
        if type(value) == str:
            self._categories = value.split(',')
    
    def __repr__(self):
        res = "pStatus:\n  " + self.text
        return res


"""
Example line of CSV

  text    ||||time%a %b %d %H:%M:%S %Y||||Locat||||GHas||||lHas||||Categories
statusText||||Fri Jul 04 00:18:13 2014||||32304||||True||||True||||Soccer,Football
testEcho84331||||Tue Jul 08 22:04:25 2014||||84331||||True||||True||||soccer, foosball, rand_int
"""

class Echo(pStatus):
    def __init__(self, csvLine):
        assert(type(csvLine) == str),\
            "Attempted to create Echo from type: %s" % str(type(csvLine))

        # CSV Line should come in form of 6 values delimeted by '||||'
        #     text, location, gHash, lHash, categories, postTime
        values = csvLine.split('||||')
        assert(len(values) == 6),\
            'Found %d fields in CSV line:\n %s' % (len(values), string)

        self.text = values[0]
        self.location = values[1]
        self.gHash = values[2]
        self.lHash = values[3]
        self.categories = values[4]
        self.postTime = values[5]


    @property
    def postTime(self):
        return self._postTime


    @postTime.setter
    def postTime(self, value):
        assert(type(value) == str or type(value) == datetime.datetime),\
            "Tried to pass type \'%s\' into pStatus.postTime" % str(type(value))
        if type(value) == str:
            # time to post
            self._postTime = datetime.datetime.strptime(value, '%a %b %d %H:%M:%S %Y')
        if type(value) == datetime.datetime:
            self._postTime = value

    @property
    def strTime(self):
        return datetime.datetime.strftime(self._postTime, '%a %b %d %H:%M:%S %Y')

    @property
    def string(self):
        return ('||||').join([self.text, self.location,\
            str(self.gHash), str(self.lHash), ','.join(self.categories), self.strTime])

    def timeToPost(self):
        age = self.postTime - NOW
        if age.seconds < FREQUENCY:
            return True
        return False

    def __repr__(self):
        res = "Echo:"
        res += "\n  Text: " + self.text
        res += "\n  Time: " + self.strTime + "  |  Location: " + self.location
        res += '\n  '
        if self.gHash:
            res += "gHash "
        if self.lHash:
            res += "LHash "
        if self.gHash or self.lHash:
            res += ' -> Categories:  ' + ','.join(self.categories)
        return res



# tStatus = twitter status
#   aka the json dict returned by Twitter
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
            if NOW > newEcho.time:
                 print("OLD ECHO: " + newEcho.text)
            else:
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

class Squawk:
    def __init__(self, string=None):
        # String is pulled from echo.csv
        self.string = string

        # If string is not None, parse string
        if string is not None:
            self.initFromCSVLine(string)

    def initFromCSVLine(self, string):
        # CSV Line should come in form of 6 values delimeted by '||||'
        #     text, prevTime, countDown, location, gHash, lHash, categories, startTime
        string = self.string
        values = string.split('||||')
        
        assert(len(values) == 6), 'Found %d fields in CSV line:\n %s' % (len(values), string)
        
        # text of status
        self.text = values[0]

        # time to post
        self.prevTime = datetime.datetime.strptime(values[1], '%a %b %d %H:%M:%S %Y')

        self.countDown = values[2]

        # location to post from
        self.location = values[3]

        # append global or local hashes?
        self.gHash = strToBool(values[4])
        self.lHash = strToBool(values[5])

        # what categories should hashes be from?            
        self.categories = values[6].split(',')

        # when squawk goes into effect
        #  For example, user may want to pre-set squawks for a
        #  an upcoming event / month / whatev
        self.prevTime = datetime.datetime.strptime(values[1], '%a %b %d %H:%M:%S %Y')