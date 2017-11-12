import subprocess, sched, time, sqlite3, common, signal, sys

# Creates or opens a file called dashboard with a SQLite3 DB
db = sqlite3.connect('dashboard.sqlite3')

# Get a cursor object
cursor = db.cursor()
data_collection = 10
s = sched.scheduler(time.time, time.sleep)

# def signal_handler(signal, frame):
#     print('Exiting Monit Script')
#     db.close()
#     sys.exit(0)

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
    db.commit()
    
    #docker info, id, image and name
    p = subprocess.check_output("docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}' ", shell=True)
    print('output \n\n ')
    print(p)
    p = p.split('\n')
    lenofoutput = len(p)
    print(len(p))
    for x in range(lenofoutput-1):
        print(x)
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_MASTER,[y[0], y[1], y[2]])
        db.commit()
        print(y)
    # cpu usage docker wise
    p = subprocess.check_output("docker stats --no-stream --format '{{.Container}}\t{{.CPUPerc}}' ", shell=True)
    print('output \n\n ')
    print(p)
    p = p.split('\n')
    lenofoutput = len(p)
    print(len(p))
    for x in range(lenofoutput-1):
        print(x)
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.CPU_USAGE, y[0], y[1]])
        db.commit()
        print(y)
    
    s.enter(data_collection, 1, monit_routine, (s,))

s.enter(data_collection, 1, monit_routine, (s,))
# signal.signal(signal.SIGINT, signal_handler)
# signal.pause()
s.run()
