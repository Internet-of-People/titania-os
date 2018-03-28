import subprocess, sched, time, sqlite3, common, signal, sys

# Creates or opens a file called dashboard with a SQLite3 DB
db = sqlite3.connect('/datafs/titania/dashboard.sqlite3')

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
    cursor.execute(common.Q_CREATE_DOCKER_OVERVIEW)
except sqlite3.Error as err:
    print('Error %s', er)
db.commit()

data_collection = 30
s = sched.scheduler(time.time, time.sleep)

# TO DO: make an option to disable all monitoring from UI
# def signal_handler(signal, frame):
#     print('Exiting Monit Script')
#     db.close()
#     sys.exit(0)

def convert_to_bytes(input):
    p = input.split(' ')
    num = float(p[0])
    if p[1] == 'kiB' or p[1] == 'kB':
        num = num*1000
    elif p[1] == 'MiB' or p[1] == 'MB':
        num = num*1000*1000
    elif p[1] == 'GiB' or p[1] == 'GB':
        num = num*1000*1000*1000
    return num

def monit_routine(s):
    # Maintainance loop 
    cursor.execute(common.Q_EXTRACT_OLD_SYSTEM_DATA)
    cursor.execute(common.Q_AGGREGATE_OLD_SYSTEM_DATA)
    cursor.execute(common.Q_PURGE_OLD_SYSTEM_DATA)
    cursor.execute(common.Q_INSERT_AGGREGATE_SYSTEM_DATA)
    cursor.execute(common.Q_EXTRACT_OLD_DOCKER_DATA)
    cursor.execute(common.Q_AGGREGATE_OLD_DOCKER_DATA)
    cursor.execute(common.Q_PURGE_OLD_DOCKER_DATA)
    cursor.execute(common.Q_INSERT_AGGREGATE_DOCKER_DATA)
    # for x in common.Q_TEMP_TABLES:
    #     print(x)
    #     print(common.Q_DROP_TABLE)
    #     cursor.execute(common.Q_DROP_TABLE, [x])
    db.commit()

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
    p = p.decode("utf-8")
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
    p = subprocess.check_output(common.CMD_DOCKER_MASTER, shell=True)
    p = p.decode("utf-8")
    p = p.split('\n')
    lenofoutput = len(p)
    for x in range(lenofoutput-1):
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_MASTER,[y[0], y[1], y[2]])
        db.commit()
    # cpu usage docker wise
    p = subprocess.check_output(common.CMD_DOCKER_STATS, shell=True)
    p = p.decode("utf-8")
    p = p.split('\n')
    lenofoutput = len(p)
    for x in range(lenofoutput-1):
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.CPU_USAGE, y[0], y[1]])
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.MEM_PERC, y[0], y[2]])
        #format 7.691 MiB / 927.3 MiB = mem used / limit of mem
        mem = y[3].split('/ ')
        mem_usage = convert_to_bytes(mem[0])
        mem_usage_limit = convert_to_bytes(mem[1])
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.MEM_USAGE, y[0], mem_usage])
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.MEM_USAGE_LIMIT, y[0], mem_usage_limit])
        #format 168 kB / 3.08 MB 
        net = y[4].split('/ ')
        net_i = convert_to_bytes(net[0])
        net_o = convert_to_bytes(net[1])
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.NET_IN, y[0], net_i])
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.NET_OUT, y[0], net_o])
        #format 6.68 MB / 4.1 kB
        block = y[5].split('/ ')
        block_i = convert_to_bytes(block[0])
        block_o = convert_to_bytes(block[1])
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.BLOCK_IN, y[0], block_i])
        cursor.execute(common.Q_INSERT_DOCKER_CONTENT,[common.BLOCK_OUT, y[0], block_o])
        db.commit()
    # end container level monitoring - currently works for CPU Usage

    # docker overview- first delete all entries and then populate snapshot.
    # we donot need to retain previous status    
    # delete previous snapshot
    cursor.execute(common.Q_CLEAR_DOCKER_OVERVIEW)
    db.commit()
    #for running
    p = subprocess.check_output(common.CMD_DOCKER_OVERVIEW_RUNNING, shell=True)
    p = p.decode("utf-8")
    p = p.split("\n")
    lenofoutput = len(p)
    for x in range(lenofoutput-1):
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_OVERVIEW_RUNNING,y)
        db.commit()
    #for paused
    p = subprocess.check_output(common.CMD_DOCKER_OVERVIEW_PAUSED, shell=True)
    p = p.decode("utf-8")
    p = p.split("\n")
    lenofoutput = len(p)
    for x in range(lenofoutput-1):
        cursor.execute(common.Q_INSERT_DOCKER_OVERVIEW_PAUSED,y)
        db.commit()
    #for exited
    p = subprocess.check_output(common.CMD_DOCKER_OVERVIEW_EXITED, shell=True)
    p = p.decode("utf-8")
    p = p.split("\n")
    lenofoutput = len(p)
    for x in range(lenofoutput-1):
        y = p[x].split('\t')
        cursor.execute(common.Q_INSERT_DOCKER_OVERVIEW_EXITED,y)
        db.commit()
    # end docker overview

    s.enter(data_collection, 1, monit_routine, (s,))

s.enter(data_collection, 1, monit_routine, (s,))
# signal.signal(signal.SIGINT, signal_handler)
# signal.pause()
s.run()
