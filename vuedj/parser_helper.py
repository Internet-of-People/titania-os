import subprocess
# docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}
p = subprocess.check_output("docker stats --no-stream --format '{{.Container}}\t{{.CPUPerc}}' ", shell=True)
print('docker ps \n\n ')
print(p)
p= p.split('\t')
print(p)