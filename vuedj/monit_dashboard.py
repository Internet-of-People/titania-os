import subprocess, sched, time, sqlite3, common, signal, sys

# Creates or opens a file called dashboard with a SQLite3 DB
db = sqlite3.connect('dashboard.sqlite3')

# Get a cursor object
cursor = db.cursor()
data_collection = 10
s = sched.scheduler(time.time, time.sleep)

def signal_handler(signal, frame):
    print('Exiting Monit Script')
    db.close()
    sys.exit(0)

def monit_routine(s):
    # total dApps
    p = subprocess.check_output(common.CMD_TOTAL_DAPPS, shell=True)
    print('\n\nTotal dApps: ')
    print(p.strip())
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.TOTAL_DAPPS, p])
    db.commit()

    # status of stopped dApps
    # link >> https://docs.docker.com/engine/reference/commandline/ps/#filtering
    p = subprocess.check_output(common.CMD_STOPPED_DAPPS, shell=True)
    print('\n\nStopped dApps:')
    print(p.strip())
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.STOPPED_DAPPS, p])
    db.commit()

    # uptime
    p = subprocess.check_output(common.CMD_UPTIME, shell=True)
    print('\n\nUptime: ')
    p = p.split(' ')
    print(p[0].strip())
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.UPTIME, p[0]])
    db.commit()

    # threads
    p = subprocess.check_output(common.CMD_THREADS, shell=True)
    print('\n\nTotal Threads: ')
    print(p.strip())
    cursor.execute(common.Q_INSERT_SYSTEM_CONTENT,[common.THREADS, p])
    
    # cpu usage docker wise
    p = subprocess.check_output(common.CMD_CPU_USAGE, shell=True)
    print('\n\nCPU USAGE: ')
    print(p.strip())
    rows = p.split('\t')
    print(rows)
    #cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.CPU_USAGE, , p])
    
    s.enter(data_collection, 1, monit_routine, (s,))

s.enter(data_collection, 1, monit_routine, (s,))
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
s.run()
