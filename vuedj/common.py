"""SCHEMA PREF """
VERSION = 1.0
MAJOR_VERSION = 1
MINOR_VERSION = 0

"""MONITORING TABLES """
# failsafe so that if table exists insert row is not performed
Q_CREATE_SYSTEM_COUNTERS = ('CREATE TABLE IF NOT EXISTS [counter_system] ('
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

Q_CREATE_SYSTEM_CONTENT = ('CREATE TABLE IF NOT EXISTS [content_system] ('
                            '[counter_id] INTEGER NOT NULL,'
                            '[value] INTEGER,'
                            '[collection_timestamp] TIMESTAMP DEFAULT (strftime(\'%s\', \'now\')),'
                            'FOREIGN KEY([counter_id]) REFERENCES [counter_system]([counter_id]))')

Q_INSERT_SYSTEM_CONTENT = ('INSERT INTO [content_system] (counter_id,value) VALUES(?,?)')

Q_DASHBOARD_CARDS = ('SELECT a.[counter_id], b.[counter_name], a.[value], max(a.[collection_timestamp])'
                    ' FROM [content_system] a INNER JOIN [counter_system] b '
                    ' ON a.[counter_id] = b.[counter_id]'
                    ' GROUP BY a.[counter_id]')

Q_CREATE_DOCKER_COUNTERS = ('CREATE TABLE IF NOT EXISTS [counter_docker] ('
                            '[counter_id] INTEGER NOT NULL PRIMARY KEY,'
                            '[counter_name] VARCHAR(20),'
                            '[formula] TEXT)')
            
# unable to write escaped seq for >> docker stats --no-stream --format \'\{\{\.Container}}\t\{\{\.CPUPerc}}\')                           
Q_LIST_INSERT_DOCKER_COUNTERS = ('INSERT OR REPLACE INTO [counter_docker]'
                                    '(counter_id,counter_name,formula)'
                                    'VALUES'
                                    '(1,\'CPU Usage\',\'docker stats --no-stream --format container.cpuperc\')')                           

            
Q_CREATE_DOCKER_MASTER = ('CREATE TABLE IF NOT EXISTS [docker_master] ('
                            '[container_id] VARCHAR(40) PRIMARY KEY,'
                            '[name] VARCHAR(40),'
                            '[image] VARCHAR(40) )')
                            
Q_INSERT_DOCKER_MASTER = ('INSERT OR REPLACE INTO [docker_master] (container_id,name,image) VALUES(?,?,?)')                            
        

Q_CREATE_DOCKER_CONTENT = ('CREATE TABLE IF NOT EXISTS [content_docker] ('
                            '[counter_id] INTEGER NOT NULL REFERENCES [counter_docker]([counter_id]),'
                            '[container_id] TEXT NOT NULL REFERENCES [docker_master]([container_id]),' 
                            '[value] INTEGER,'
                            '[collection_timestamp] TIMESTAMP DEFAULT (strftime(\'%s\', \'now\')))')

Q_INSERT_DOCKER_CONTENT = ('INSERT INTO [content_docker] (counter_id,container_id,value) VALUES(?,?,?)')     

Q_GET_CONTAINER_ID = ('SELECT [container_id],[name]'
                    ' FROM [docker_master] ')
                    
Q_GET_DASHBOARD_CHART = ('SELECT a.[collection_timestamp] * 1000,  CAST(SUBSTR(a.[value],0,length(a.[value])) as decimal)'
                    ' FROM [content_docker] a INNER JOIN [docker_master] b '
                    ' ON a.[container_id] = b.[container_id]'
                    ' GROUP BY a.[container_id], a.[collection_timestamp] '
                    ' HAVING a.[container_id] = ?'
                    ' ORDER BY a.[collection_timestamp]')

Q_PURGE_OLD_SYSTEM_DATA = ('DELETE FROM [content_system]'
                        'WHERE DATETIME([collection_timestamp],\'unixepoch\') < DATETIME(\'now\',\'-1 week\')')

Q_PURGE_OLD_DOCKER_DATA = ('DELETE FROM [content_docker]'
                        'WHERE DATETIME([collection_timestamp],\'unixepoch\') < DATETIME(\'now\',\'-1 week\')')

#command >> docker ps -a --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.RunningFor}}\t{{.Command}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}'
Q_CREATE_DOCKER_OVERVIEW = ('CREATE TABLE IF NOT EXISTS [docker_overview] ('
                            '[state] VARCHAR,'
                            '[container_id] VARCHAR(40) PRIMARY KEY,'
                            '[name] VARCHAR(40),'
                            '[image] VARCHAR(40),'
                            '[running_for] VARCHAR,'
                            '[command] VARCHAR,'
                            '[ports] VARCHAR,'
                            '[latest_status] VARCHAR,'
                            '[networks] VARCHAR)')     

Q_CLEAR_DOCKER_OVERVIEW = ('DELETE FROM [docker_overview]')          

Q_INSERT_DOCKER_OVERVIEW_RUNNING = ('INSERT INTO [docker_overview] VALUES(\'Running\',?,?,?,?,?,?,?,?)')   
Q_INSERT_DOCKER_OVERVIEW_PAUSED = ('INSERT INTO [docker_overview] VALUES(\'Paused\',?,?,?,?,?,?,?,?)')   
Q_INSERT_DOCKER_OVERVIEW_EXITED = ('INSERT INTO [docker_overview] VALUES(\'Exited\',?,?,?,?,?,?,?,?)')   


Q_GET_DOCKER_OVERVIEW = ('SELECT * FROM [docker_overview]') 

"""SYSTEM COUNTER IDs"""
#temporarily here, not a feasible solution for other counters
TOTAL_DAPPS = 1
UPTIME = 2
STOPPED_DAPPS = 3
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
#DOCKER MASTER
CMD_DOCKER_MASTER = "docker ps -a --format '{{.ID}}\t{{.Names}}\t{{.Image}}'"
#DOCKER METRICS
CMD_CPU_USAGE = "docker stats -a --no-stream --format '{{.Container}}\t{{.CPUPerc}}'"
#DOCKER INFO
CMD_DOCKER_OVERVIEW_RUNNING = "docker ps -a --filter status=running --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.RunningFor}}\t{{.Command}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}'"
CMD_DOCKER_OVERVIEW_PAUSED = "docker ps -a --filter status=paused --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.RunningFor}}\t{{.Command}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}'"
CMD_DOCKER_OVERVIEW_EXITED = "docker ps -a --filter status=exited --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.RunningFor}}\t{{.Command}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}'"