import sys
import json
j = open(sys.argv[1]).read()
vars = json.loads(j)
print(vars['DISTRO_VERSION'])
