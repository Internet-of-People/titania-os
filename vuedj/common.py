"""SCHEMA PREF """
VERSION = 1.0
MAJOR_VERSION = 1
MINOR_VERSION = 0

"""MONITORING TABLES """
# failsafe so that if table exists insert row is not performed
Q_CREATE_DASHBOARD_COUNTERS = ('CREATE TABLE [counter_master] ('
                            '[counter_id] INTEGER NOT NULL PRIMARY KEY,'
                            '[counter_name] VARCHAR(20),'
                            '[formula] TEXT)')

# replace row no 2 with LOC server fetched neighbouring nodes
Q_LIST_INSERT_DASHBOARD_COUNTERS = ('INSERT OR REPLACE INTO [counter_master] ('
                                    'counter_id,counter_name,formula)'
                                    'VALUES'
                                    '(1,\'Total dApps\',\'docker ps | wc -l\'),'
                                    '(2,\'Stopped dApps\',\'docker ps --filter status=stopped | wc -l\'),'
                                    '(3,\'Uptime\',\'cat /proc/uptime\'),'
                                    '(4,\'Threads\',\'ps axms | wc -l\' )')

Q_CREATE_DASHBOARD_CONTENT = ('CREATE TABLE IF NOT EXISTS [content] ('
                            '[counter_id] INTEGER NOT NULL,'
                            '[value] INTEGER,'
                            '[collection_timestamp] TIMESTAMP DEFAULT (strftime(\'%s\', \'now\')),'
                            'FOREIGN KEY([counter_id]) REFERENCES [counter_master]([counter_id]))')

Q_INSERT_DASHBOARD_CONTENT = ('INSERT INTO [content] (counter_id,value) VALUES(?,?)')

Q_DASHBOARD_CARDS = ('SELECT a.[counter_id], b.[counter_name], a.[value], max(a.[collection_timestamp])'
                    ' FROM [content] a INNER JOIN [counter_master] b '
                    ' ON a.[counter_id] = b.[counter_id]'
                    ' GROUP BY a.[counter_id]')
                    

"""COUNTER IDs"""
#temporarily here, not a feasible solution for other counters
TOTAL_DAPPS = 1
STOPPED_DAPPS = 2
UPTIME = 3
THREADS = 4
