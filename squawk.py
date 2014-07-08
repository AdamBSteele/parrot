def run(user):
    newStatus = grabSquawk(user)
    user.post(newStatus)
    decrementSquawkCSV(user)


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
    for line in open(path + 'squawk.csv'):
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
    with open(path + 'squawk.csv', 'w') as myfile:
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