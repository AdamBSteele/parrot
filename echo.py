"""
Echo contains the echo class and its functions

Example line of CSV

time in form: %a %b %d %H:%M:%S %Y
  text    ||||     Time               ||||Locat||||GHas||||lHas||||Categories
statusText||||Fri Jul 04 00:18:13 2014||||32304||||True||||True||||Soccer,Football
"""
import datetime

# Initialize time
NOW = datetime.datetime.now()

# Frequency of crontab runs.
FREQUENCY = 300


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
    lineNo = 0
    for line in open(path + 'echo.csv'):
        try:
            newEcho = Echo(line.strip())
            if NOW > newEcho.time:
                 print("OLD ECHO: " + newEcho.text)
            else:
                lines.append(line)
                res.append(newEcho)
        except Exception as e:
            print("readEchoes failed on line %d" % lineNo)
            print(e)
        lineNo += 1

    # Write all non-posted lines
    with open(path + 'echo.csv', 'w') as myfile:
        for line in lines:
            myfile.write(line)

    print("Found %d non-old echoes" % len(res))
    return res

def strToBool(string):
    if string == "True":
        return True
    return False




class Echo:
    def __init__(self, string=None):
        # String is pulled from echo.csv
        self.string = string

        # If string is not None, parse string
        if string is not None:
            self.initFromCSVLine(string)

    def initFromCSVLine(self, string):
        # CSV Line should come in form of 6 values delimeted by '||||'
        #     text, time, location, gHash, lHash, categories
        string = self.string
        values = string.split('||||')
        
        assert(len(values) == 6), 'Found %d fields in CSV line:\n %s' % (len(values), string)
        
        # text of status
        self.text = values[0]

        # time to post
        self.time = datetime.datetime.strptime(values[1], '%a %b %d %H:%M:%S %Y')

        # location to post from
        self.location = values[2]

        # append global or local hashes?
        self.gHash = strToBool(values[3])
        self.lHash = strToBool(values[4])

        # what categories should hashes be from?            
        self.categories = values[5].split(',')

    def initFromValues(self, text, time, location, gHash, lHash, categories):
        assert(type(text) == str)
        self.text = text
        assert(type(time) == datetime.datetime), "Time wasn't datetime"
        self.time = time
        strTime = time.strftime('%a %b %d %H:%M:%S %Y')
        self.location = location

        assert(type(gHash) == bool), "gHash came in as %s. Should be bool!" % (str(type(gHash)))
        self.gHash = gHash

        assert(type(lHash) == bool), "gHash came in as %s. Should be bool!" % (str(type(lHash)))
        self.lHash = lHash

        assert(type(categories) == list),\
            "Categories came in as %s. Should be list!" % (str(type(categories)))
        
        self.categories = categories
        self.string = ('||||').join([text, strTime, str(location),\
            str(gHash), str(lHash), ','.join(categories)])

    def timeToPost(self):
        age = self.time - NOW
        if age.seconds < FREQUENCY:
            return True
        return False

    def __repr__(self):
        res = "Echo:"
        res += "\n  Text: " + self.text
        res += "\n  Time: " + str(self.time) + "  |  Location: " + self.location
        res += '\n  '
        if self.gHash:
            res += "gHash "
        if self.lHash:
            res += "LHash "
        if self.gHash or self.lHash:
            res += ' -> Categories:  ' + ','.join(self.categories)
        return res