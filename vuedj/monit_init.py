import sqlite3, common
# # Creates or opens a file called dashboard with a SQLite3 DB
db = sqlite3.connect('dashboard.sqlite3')

# Get a cursor object
cursor = db.cursor()
try:
    #TO DO: execute this in a loop
    cursor.execute(common.Q_CREATE_SYSTEM_COUNTERS)
    cursor.execute(common.Q_LIST_INSERT_SYSTEM_COUNTERS)
    cursor.execute(common.Q_CREATE_SYSTEM_CONTENT)
    cursor.execute(common.Q_CREATE_DOCKER_COUNTERS)
    cursor.execute(Q_LIST_INSERT_DOCKER_COUNTERS)
    cursor.execute(common.Q_CREATE_DOCKER_MASTER)
    cursor.execute(common.Q_CREATE_DOCKER_CONTENT)
except sqlite3.Error, e:
    print('Error %s',e)

db.commit()

db.close()
