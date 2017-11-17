import subprocess, sched, time, sqlite3, common, signal, sys

# Creates or opens a file called dashboard with a SQLite3 DB
db = sqlite3.connect('dashboard.sqlite3')

# Get a cursor object
cursor = db.cursor()

# initialize the monitoring schema
try:
    #TO DO: execute this in a loop
    cursor.execute(common.Q_CREATE_SYSTEM_COUNTERS)
    cursor.execute(common.Q_LIST_INSERT_SYSTEM_COUNTERS)
    cursor.execute(common.Q_CREATE_SYSTEM_CONTENT)
    cursor.execute(common.Q_CREATE_DOCKER_COUNTERS)
    cursor.execute(common.Q_LIST_INSERT_DOCKER_COUNTERS)
    cursor.execute(common.Q_CREATE_DOCKER_MASTER)
    cursor.execute(common.Q_CREATE_DOCKER_CONTENT)
except sqlite3.Error, e:
    print('Error %s',e)
db.commit()

data_collection = 30
s = sched.scheduler(time.time, time.sleep)

# TO DO: make an option to disable all monitoring from UI
# def signal_handler(signal, frame):
#     print('Exiting Monit Script')
#     db.close()
#     sys.exit(0)

def monit_routine(s):
    # TO DO: write a maintainance loop here

    # start system level collection
    # total dApps
    p = subprocess.check_output(common.CMD_TOTAL_DAPPS, shell=True)
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.TOTAL_DAPPS, p])
    db.commit()

    # status of stopped dApps
    # link >> https://docs.docker.com/engine/reference/commandline/ps/#filtering
    p = subprocess.check_output(common.CMD_STOPPED_DAPPS, shell=True)
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.STOPPED_DAPPS, p])
    db.commit()

    # uptime
    p = subprocess.check_output(common.CMD_UPTIME, shell=True)
    p = p.split(' ')
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.UPTIME, p[0]])
    db.commit()

    # threads
    p = subprocess.check_output(common.CMD_THREADS, shell=True)
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.THREADS, p])
    db.commit()
    # end system level collection

    # start container level monitoring - currently works for CPU Usage
    # docker info, id, image and name
    p = subprocess.check_output("docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}' ", shell=True)
    p = p.split('\n')
    lenofoutput = len(p)
    for x in range(lenofoutput-1):
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_MASTER,[y[0], y[1], y[2]])
        db.commit()
    # cpu usage docker wise
    p = subprocess.check_output("docker stats --no-stream --format '{{.Container}}\t{{.CPUPerc}}' ", shell=True)
    p = p.split('\n')
    lenofoutput = len(p)
    for x in range(lenofoutput-1):
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.CPU_USAGE, y[0], y[1]])
        db.commit()
    # end container level monitoring - currently works for CPU Usage

    s.enter(data_collection, 1, monit_routine, (s,))

s.enter(data_collection, 1, monit_routine, (s,))
# signal.signal(signal.SIGINT, signal_handler)
# signal.pause()
s.run()
