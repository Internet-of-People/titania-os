import subprocess, sched, time, sqlite3, common, signal, sys

# Creates or opens a file called dashboard with a SQLite3 DB
db = sqlite3.connect('dashboard.sqlite3')

# Get a cursor object
cursor = db.cursor()
data_collection = 60
s = sched.scheduler(time.time, time.sleep)

def signal_handler(signal, frame):
    print('Exiting Monit Script')
    db.commit()
    db.close()
    sys.exit(0)

def monit_routine(s):
    # total dApps
    p = subprocess.check_output("docker ps | wc -l", shell=True)
    print('\n\nTotal dApps: ')
    print(p.strip())
    cursor.execute(common.Q_INSERT_DASHBOARD_CONTENT,[common.TOTAL_DAPPS, p])

    # status of stopped dApps
    p = subprocess.check_output("docker ps --filter status=stopped", shell=True)
    print('\n\nStopped dApps info: \n')
    print(p.strip())
    cursor.execute(common.Q_INSERT_DASHBOARD_CONTENT,[common.STOPPED_DAPPS, p])

    # uptime
    p = subprocess.check_output("cat /proc/uptime", shell=True)
    print('\n\nUptime: ')
    print(p.strip())
    cursor.execute(common.Q_INSERT_DASHBOARD_CONTENT,[common.UPTIME, p])

    # threads
    p = subprocess.check_output("ps axms | wc -l", shell=True)
    print('\n\nTotal Threads: ')
    print(p.strip())
    cursor.execute(common.Q_INSERT_DASHBOARD_CONTENT,[common.THREADS, p])

    s.enter(data_collection, 1, monit_routine, (s,))

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
s.enter(data_collection, 1, monit_routine, (s,))
s.run()
