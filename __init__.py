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
