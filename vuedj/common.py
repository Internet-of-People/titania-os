"""SCHEMA PREF """
VERSION = 1.0
MAJOR_VERSION = 1
MINOR_VERSION = 0

"""MONITORING TABLES """
# failsafe so that if table exists insert row is not performed
Q_CREATE_SYSTEM_COUNTERS = ('CREATE TABLE [counter_system] ('
                            '[counter_id] INTEGER NOT NULL PRIMARY KEY,'
                            '[counter_name] VARCHAR(20),'
                            '[formula] TEXT)')

# replace row no 2 with LOC server fetched neighbouring nodes
Q_LIST_INSERT_SYSTEM_COUNTERS = ('INSERT OR REPLACE INTO [counter_system] ('
                                    'counter_id,counter_name,formula)'
                                    'VALUES'
                                    '(1,\'Total dApps\',\'docker ps | wc -l\'),'
                                    '(2,\'Stopped dApps\',\'docker ps --filter status=stopped | wc -l\'),'
                                    '(3,\'Uptime\',\'cat /proc/uptime\'),'
                                    '(4,\'Threads\',\'ps axms | wc -l\' )')

Q_CREATE_SYSTEM_CONTENT = ('CREATE TABLE IF NOT EXISTS [content] ('
                            '[counter_id] INTEGER NOT NULL,'
                            '[value] INTEGER,'
                            '[collection_timestamp] TIMESTAMP DEFAULT (strftime(\'%s\', \'now\')),'
                            'FOREIGN KEY([counter_id]) REFERENCES [counter_system]([counter_id]))')

Q_INSERT_SYSTEM_CONTENT = ('INSERT INTO [content] (counter_id,value) VALUES(?,?)')

Q_DASHBOARD_CARDS = ('SELECT a.[counter_id], b.[counter_name], a.[value], max(a.[collection_timestamp])'
                    ' FROM [content] a INNER JOIN [counter_system] b '
                    ' ON a.[counter_id] = b.[counter_id]'
                    ' GROUP BY a.[counter_id]')

Q_CREATE_DOCKER_COUNTERS = ('CREATE TABLE [counter_docker] ('
                            '[counter_id] INTEGER NOT NULL PRIMARY KEY,'
                            '[counter_name] VARCHAR(20),'
                            '[formula] TEXT)')
            
Q_CREATE_DOCKER_MASTER = ('CREATE TABLE [docker_master] ('
                            '[container_id] TEXT PRIMARY KEY ,'
                            '[formula] TEXT)')
                            
Q_LIST_INSERT_DOCKER_COUNTERS = ('INSERT OR REPLACE INTO [counter_docker]'
                                    '(counter_id,counter_name,formula)'
                                    'VALUES'
                                    '(1,\'CPU Usage\',\'docker stats --no-stream --format \'{{.Container}}\t{{.CPUPerc}}\')')                           

Q_CREATE_DOCKER_CONTENT = ('CREATE TABLE IF NOT EXISTS [content_docker] ('
                            '[counter_id] INTEGER NOT NULL REFERENCES [counter_docker]([counter_id]),'
                            '[container_id] TEXT NOT NULL REFERENCES [counter_docker]([container_id])' 
                            '[value] INTEGER,'
                            '[collection_timestamp] TIMESTAMP DEFAULT (strftime(\'%s\', \'now\')))')

Q_INSERT_DOCKER_CONTENT = ('INSERT INTO [content_docker] (counter_id,container_id,value) VALUES(?,?,?)')                    

"""SYSTEM COUNTER IDs"""
#temporarily here, not a feasible solution for other counters
TOTAL_DAPPS = 1
STOPPED_DAPPS = 2
UPTIME = 3
THREADS = 4

"""DOCKER COUNTER IDs"""
#temporarily here, not a feasible solution for other counters
CPU_USAGE = 1

"""COMMANDS TO FETCH METRICS"""
#SYSTEM METRICS
CMD_TOTAL_DAPPS = "docker ps | wc -l"
CMD_STOPPED_DAPPS = "docker ps --filter status=paused | wc -l"
CMD_UPTIME = "cat /proc/uptime"
CMD_THREADS = "ps axms | wc -l"
#DOCKER METRICS
CMD_CPU_USAGE = "docker stats --no-stream --format '{{.Container}}\t{{.CPUPerc}}'"
