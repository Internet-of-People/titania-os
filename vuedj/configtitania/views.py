from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import list_route

from .models import User, Schema
from .serializers import UserSerializer, SchemaSerializer

import common, sqlite3, subprocess, NetworkManager, os, crypt, pwd, getpass, spwd 

# fetch network AP details
nm = NetworkManager.NetworkManager
wlans = [d for d in nm.Devices if isinstance(d, NetworkManager.Wireless)]

@csrf_exempt
def handle_config(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        action = request.POST.get("_action")
        if action == 'getSchema':
            print(action)
            queryset = Schema.objects.all()
            schemaSet = len(queryset)
            if schemaSet == 0:
                setSchema = Schema(version=common.VERSION, major_version=common.MAJOR_VERSION, minor_version=common.MINOR_VERSION)
                setSchema.save()
                print('saved schema')
            serializer = SchemaSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif action == 'getUserDetails':
            print(action)
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif action == 'getAllAPs':
            wifi_aps = []   
            for dev in wlans:
                for ap in dev.AccessPoints:
                    wifi_aps.append(ap.Ssid)
            return JsonResponse(wifi_aps, safe=False)
        elif action == 'saveUserDetails':
            print(action)
            boxname = request.POST.get("boxname")
            username = request.POST.get("username")
            password = request.POST.get("password")
            encPass = crypt.crypt(password,"22")
            os.system("useradd -p "+encPass+" "+username)
            setUser = User(boxname=boxname, username=username, password=password)
            setUser.save()
            # connect to wifi ap user selected
            wifi_psk = request.POST.get("wifi_password")
            wifi_name = request.POST.get("wifi_ap")
            wlan0 = wlans[0]
            # get selected ap as currentwifi
            for dev in wlans:
                for ap in dev.AccessPoints:
                    if ap.Ssid == wifi_name:
                        currentwifi = ap
            # params to set password
            params = {
                    "802-11-wireless": {
                        "security": "802-11-wireless-security",
                    },
                    "802-11-wireless-security": {
                        "key-mgmt": "wpa-psk",
                        "psk": wifi_psk
                    },
                }
            conn = nm.AddAndActivateConnection(params, wlan0, currentwifi)
            return JsonResponse([{"STATUS":"SUCCESS"},{"RESPONSE":"Config saved successfully"}], safe=False)
        elif action == 'login':
            print(action)
            username = request.POST.get("username")
            password = request.POST.get("password")
            output=''
            """Tries to authenticate a user.
            Returns True if the authentication succeeds, else the reason
            (string) is returned."""
            try:
                enc_pwd = spwd.getspnam(username)[1]
                if enc_pwd in ["NP", "!", "", None]:
                    output = "user '%s' has no password set" % username
                if enc_pwd in ["LK", "*"]:
                    output = "account is locked"
                if enc_pwd == "!!":
                    output = "password has expired"
                # Encryption happens here, the hash is stripped from the
                # enc_pwd and the algorithm id and salt are used to encrypt
                # the password.
                if crypt.crypt(password, enc_pwd) == enc_pwd:
                    output = ''
                else:
                    output = "incorrect password"
            except KeyError:
                output = "user '%s' not found" % username
            if len(output) == 0:
                return JsonResponse({"username":username}, safe=False)
            else:
                return JsonResponse(output, safe=False)
        elif action == 'logout':
            print(action)
            username = request.POST.get("username")
            print(username+' ')
            queryset = User.objects.all().first()
            if username == queryset.username:
                return JsonResponse({"STATUS":"SUCCESS", "username":queryset.username}, safe=False)
        elif action == 'getDashboardCards':
            print(action)
            con = sqlite3.connect("dashboard.sqlite3")
            cursor = con.cursor()
            cursor.execute(common.Q_DASHBOARD_CARDS)
            rows = cursor.fetchall()
            print(rows)
            return JsonResponse(rows, safe=False)
        elif action == 'getDashboardChart':
            print(action)
            con = sqlite3.connect("dashboard.sqlite3")
            cursor = con.cursor()
            cursor.execute(common.Q_GET_CONTAINER_ID)
            rows = cursor.fetchall()
            print(rows)
            finalset = []
            for row in rows:
                cursor.execute(common.Q_GET_DASHBOARD_CHART,[row[0],])
                datasets = cursor.fetchall()
                print(datasets)
                data = {'container_name' : row[1], 'data': datasets}
                finalset.append(data)
            return JsonResponse(finalset, safe=False)
        elif action == 'getDockerOverview':
            print(action)
            con = sqlite3.connect("dashboard.sqlite3")
            cursor = con.cursor()
            cursor.execute(common.Q_GET_DOCKER_OVERVIEW)
            rows = cursor.fetchall()
            print(rows)
            finalset = []
            for row in rows:
                data = {'state': row[0], 'container_id': row[1], 'name': row[2],
                        'image': row[3], 'running_for': row[4],
                        'command': row[5], 'ports': row[6],
                        'status': row[7], 'networks': row[8]}
                finalset.append(data)
            return JsonResponse(finalset, safe=False)
        elif action == 'getContainerStats':
            print(action)
            con = sqlite3.connect("dashboard.sqlite3")
            cursor = con.cursor()
            cursor.execute(common.Q_GET_CONTAINER_ID)
            rows = cursor.fetchall()
            print(rows)
            finalset = []
            datasets_io = []
            datasets_mem = []
            datasets_perc = []
            for row in rows:
                datasets_io = []
                datasets_mem = []
                datasets_perc = []
                # values with % appended to them
                for iter in range(0,2):
                    cursor.execute(common.Q_GET_CONTAINER_STATS_CPU,[row[0],iter+1])
                    counter_val = cursor.fetchall()
                    datasets_perc.append(counter_val)
                # values w/o % appended to them
                for iter in range(2,4):
                    cursor.execute(common.Q_GET_CONTAINER_STATS,[row[0],iter+1])
                    counter_val = cursor.fetchall()
                    datasets_mem.append(counter_val)
                # values w/o % appended to them
                for iter in range(4,8):
                    cursor.execute(common.Q_GET_CONTAINER_STATS,[row[0],iter+1])
                    counter_val = cursor.fetchall()
                    datasets_io.append(counter_val)
                data = {'container_name' : row[1], 'data_io': datasets_io, 'data_mem': datasets_mem, 'data_perc': datasets_perc}
                finalset.append(data)
            return JsonResponse(finalset, safe=False)
        elif action == 'getThreads':
            print(action)
            rows = []
            ps = subprocess.Popen(['top', '-b','-n','1'], stdout=subprocess.PIPE).communicate()[0]
            processes = ps.decode().split('\n')
            # this specifies the number of splits, so the splitted lines
            # will have (nfields+1) elements
            nfields = len(processes[0].split()) - 1
            for row in processes[4:]:
                rows.append(row.split(None, nfields))
            return JsonResponse(rows, safe=False)
        elif action == 'getContainerTop':
            print(action)
            con = sqlite3.connect("dashboard.sqlite3")
            cursor = con.cursor()
            cursor.execute(common.Q_GET_CONTAINER_ID)
            rows = cursor.fetchall()
            resultset = []
            for i in rows:
                data = {}
                datasets = []
                ps = subprocess.Popen(['docker', 'top',i[0]], stdout=subprocess.PIPE).communicate()[0]
                processes = ps.decode().split('\n')
                # this specifies the number of splits, so the splitted lines
                # will have (nfields+1) elements
                nfields = len(processes[0].split()) - 1
                for p in processes[1:]:
                    datasets.append(p.split(None, nfields))
                data = {'container_name' : i[1], 'data': datasets}
                resultset.append(data)
            return JsonResponse(resultset, safe=False)
        return JsonResponse(serializer.errors, status=400)

def index(request):
    return render(request, 'index.html')

#not being used
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#not being used
class SchemaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    """Setting Schema"""
    # # setSchema = Schema(version=common.VERSION, major_version=common.MAJOR_VERSION, minor_version=common.MINOR_VERSION)
    # # setSchema.save()
    #
    # queryset = Schema.objects.all()
    # serializer_class = SchemaSerializer

