import subprocess,common
# 
p = subprocess.check_output("docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}' ", shell=True)
print('output \n\n ')
print(p)
db = sqlite3.connect('dashboard.sqlite3')

# Get a cursor object
cursor = db.cursor()
p = p.split('\n')
lenofoutput = len(p)
print(len(p))
for x in range(lenofoutput-1):
    print(x)
    y = p[x].split('\t')
    cursor.execute(common.Q_INSERT_DOCKER_MASTER,[y[0], y[1], y[2]])
    db.commit()
    print(y)
print("over")
