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
                                    '(1,\'Total dApps\',\'docker ps --format .ID | wc -l\'),'
                                    '(2,\'Stopped dApps\',\'docker ps --format .ID --filter status=exited | wc -l\'),'
                                    '(3,\'Uptime\',\'cat /proc/uptime\'),'
                                    '(4,\'Threads\',\'ps axms | wc -l\' )')

Q_CREATE_SYSTEM_CONTENT = ('CREATE TABLE IF NOT EXISTS [content_system] ('
                            '[counter_id] INTEGER NOT NULL,'
                            '[value] INTEGER,'
                            '[collection_timestamp] TIMESTAMP DEFAULT (strftime(\'%s\', \'now\')),'
                            'FOREIGN KEY([counter_id]) REFERENCES [counter_system]([counter_id]))')

Q_INSERT_SYSTEM_CONTENT = ('INSERT INTO [content_system] (counter_id,value) VALUES(?,?)')

Q_DASHBOARD_CARDS = ('SELECT a.[counter_id], b.[counter_name], CAST(a.[value] as decimal), max(a.[collection_timestamp])'
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
                    ' WHERE a.[container_id] = ? '
                    ' AND a.[counter_id] = 1'
                    ' ORDER BY a.[collection_timestamp]')

Q_GET_CONTAINER_STATS_CPU = ('SELECT a.[collection_timestamp] * 1000,  CAST(SUBSTR(a.[value],0,length(a.[value])) as decimal)'
                    ' FROM [content_docker] a INNER JOIN [docker_master] b '
                    ' ON a.[container_id] = b.[container_id]'
                    ' WHERE a.[container_id] = ? '
                    ' AND a.[counter_id] = ?'
                    ' ORDER BY a.[collection_timestamp]')

Q_GET_CONTAINER_STATS = ('SELECT a.[collection_timestamp] * 1000,  a.[value] '
                    ' FROM [content_docker] a INNER JOIN [docker_master] b '
                    ' ON a.[container_id] = b.[container_id]'
                    ' WHERE a.[container_id] = ? '
                    ' AND a.[counter_id] = ?'
                    ' ORDER BY a.[collection_timestamp]')

# Maintainance logic
# 
# Create temp table with data older than 1 week
# create table temp as
#    ...> select * from content_docker
#    ...> WHERE DATETIME([collection_timestamp],
#    ...> 'unixepoch') < DATETIME('now','-1 week');                        

# Aggregating values
# create table temp2 as
# select max(value),container_id,counter_id
#    ...> from temp
#    ...> group by container_id, counter_id

# Factoring time into the aggregation
# sqlite> select counter_id, max(value),container_id, collection_timestamp
#    ...> from temp                                           
#    ...> group by container_id, counter_id, date(collection_timestamp, 'unixepoch');

# purge all entries
# insert into existing table
# insert into content_docker
# select * from temp2

# Run the same logic for multiple aggregations


Q_EXTRACT_OLD_SYSTEM_DATA = ('CREATE TEMPORARY TABLE IF NOT EXISTS system_temp AS'
                            ' SELECT * FROM [content_system]'
                            ' WHERE DATETIME([collection_timestamp],\'unixepoch\') < DATETIME(\'now\',?)')

Q_AGGREGATE_OLD_SYSTEM_DATA = ('CREATE TEMPORARY TABLE IF NOT EXISTS [system_temp2] AS'
                            ' SELECT [counter_id], max([value]) as [value] , [collection_timestamp]'
                            ' FROM [system_temp] '
                            ' GROUP BY [counter_id], date([collection_timestamp], \'unixepoch\')')                            

Q_PURGE_OLD_SYSTEM_DATA = ('DELETE FROM [content_system]'
                        'WHERE DATETIME([collection_timestamp],\'unixepoch\') < DATETIME(\'now\',?)')

Q_INSERT_AGGREGATE_SYSTEM_DATA = ('INSERT OR REPLACE INTO [content_system] '
                                    ' SELECT * FROM [system_temp2]')

Q_EXTRACT_OLD_DOCKER_DATA = ('CREATE TEMPORARY TABLE IF NOT EXISTS [docker_temp] AS'
                            ' SELECT * FROM [content_docker]'
                            ' WHERE DATETIME([collection_timestamp],\'unixepoch\') < DATETIME(\'now\',?)')

Q_AGGREGATE_OLD_DOCKER_DATA = ('CREATE TEMPORARY TABLE IF NOT EXISTS  [docker_temp2] AS'
                            ' SELECT [counter_id], [container_id], max([value]) as [value] , [collection_timestamp]'
                            ' FROM [docker_temp] '
                            ' GROUP BY [container_id], [counter_id], date([collection_timestamp], \'unixepoch\')')                            

Q_PURGE_OLD_DOCKER_DATA = ('DELETE FROM [content_docker]'
                        'WHERE DATETIME([collection_timestamp],\'unixepoch\') < DATETIME(\'now\',?)')

Q_INSERT_AGGREGATE_DOCKER_DATA = ('INSERT OR REPLACE INTO [content_docker] '
                                    ' SELECT * FROM [docker_temp2]')

# Q_DROP_TABLE = ('DROP TABLE IF EXISTS ')
# Q_TEMP_TABLES = ['system_temp2','system_temp2','docker_temp','docker_temp2']

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
STOPPED_DAPPS = 2
UPTIME = 3
THREADS = 4

"""DOCKER COUNTER IDs"""
#temporarily here, not a feasible solution for other counters
CPU_USAGE = 1
MEM_PERC = 2
MEM_USAGE = 3
MEM_USAGE_LIMIT = 4
NET_IN = 5
NET_OUT = 6
BLOCK_IN = 7
BLOCK_OUT = 8

DOCKER_COUNTER_NAMES = ['CPU_USAGE', 'MEM_PERC','MEM_USAGE','MEM_USAGE_LIMIT','NET_IN','NET_OUT','BLOCK_IN','BLOCK_OUT']

"""COMMANDS TO FETCH METRICS"""
#SYSTEM METRICS
CMD_TOTAL_DAPPS = "docker ps -a --format '{{.ID}}' | wc -l"
CMD_STOPPED_DAPPS = "docker ps -a --format '{{.ID}}' --filter status=exited | wc -l"
CMD_UPTIME = "cat /proc/uptime"
CMD_THREADS = "ps | wc -l"
#DOCKER MASTER
CMD_DOCKER_MASTER = "docker ps -a --format '{{.ID}}\t{{.Names}}\t{{.Image}}'"
# VALID DOCKER CONTAINERS 
CMD_VALID_DOCKER_ID = "docker ps -a --format '{{.ID}}'"
#DOCKER METRICS
CMD_DOCKER_STATS = "docker stats --no-stream --format '{{.Container}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}'"
#DOCKER INFO
CMD_DOCKER_OVERVIEW_RUNNING = "docker ps -a --filter status=running --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.RunningFor}}\t{{.Command}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}'"
CMD_DOCKER_OVERVIEW_PAUSED = "docker ps -a --filter status=paused --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.RunningFor}}\t{{.Command}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}'"
CMD_DOCKER_OVERVIEW_EXITED = "docker ps -a --filter status=exited --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.RunningFor}}\t{{.Command}}\t{{.Ports}}\t{{.Status}}\t{{.Networks}}'"


"""AGGREGATION INTERVALS"""
AGGREGATES = ['-1 week','-4 days','-1 day','-12 hour','-6 hours','-3 hours','-1 hour']

"""dAPP HUB"""
IS_ENABLED_SERVICE = "systemctl is-enabled dapp@{}.service"
IS_ACTIVE_SERVICE = "systemctl is-active dapp@{}.service"
DOWNLOADED_SERVICES = "docker images --format '{{.Repository}}:{{.Tag}}'"
IS_SERVICE_DOWNLOADING = "systemctl status dapp@{} --no-pager"
SERVICE_ENABLED_AND_ACTIVE = 1
SERVICE_DISABLED = 0
SERVICE_NOT_DOWNLOADED = -1
SERVICE_DOWNLOADING = 2
SERVICE_ENABLED_AND_NOT_ACTIVE = 3
SERVICE_UPDATE_AVAILABLE_CHECK = "/opt/titania/bin/dapp_update.sh {} -n"
SERVICE_DISABLE = "systemctl disable dapp@{0}.service; systemctl stop dapp@{0}.service"
SERVICE_ENABLE = "systemctl enable dapp@{0}.service; systemctl start dapp@{0}.service"
SERVICE_RESTART = "systemctl restart dapp@{0}.service"
DOCKER_RM_DAPP = "docker rm {}; docker rmi {}"
DAPP_DOWNLOAD = "systemctl start dapp@{0}.service;systemctl enable dapp@{0}.service; systemctl start dapp@{0}.service"
SERVICE_UPDATE = "/opt/titania/bin/dapp_update.sh {0}; systemctl enable dapp@{0}.service; systemctl start dapp@{0}.service"

"""Os Update Params"""
SWU_FILE_FORMAT = "titania-arm-rpi-*.swu"

"""Check System Specs"""
GET_PLATFORM = "uname -m"
GET_WIRELESS_DEVICES = "rfkill list"