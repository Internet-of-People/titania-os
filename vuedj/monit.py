import subprocess, sched, time

#data colletion interval
data_collection = 60
#collection = 1

s = sched.scheduler(time.time, time.sleep)

def monit_output(sc):
    # threads
    print "Collection data \n\n"
    p = subprocess.check_output("ps axms | wc -l", shell=True)
    print('\n\nTotal Threads: ')
    print(p)

    # docker info
    p = subprocess.check_output("docker info", shell=True)
    print('\n\nDocker info: \n')
    print(p)

    # uptime
    p = subprocess.check_output("cat /proc/uptime", shell=True)
    print('\n\nUptime: ')
    print(p)

    # total dApps
    p = subprocess.check_output("docker ps | wc -l", shell=True)
    print('\n\nTotal dApps: ')
    print(p)

    # drilldown into all running app, has info like statuc, ports, id etc
    p = subprocess.check_output("docker ps", shell=True)
    print('\n\nRunning dApps info: \n')
    print(p)

    # status of stopped dApps
    p = subprocess.check_output("docker ps --filter status=stopped", shell=True)
    print('\n\nStopped dApps info: \n')
    print(p)
    s.enter(data_collection, 1, monit_output, (sc,))

s.enter(data_collection, 1, monit_output, (s,))

s.run()
