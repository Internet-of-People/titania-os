from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.sessions.middleware import SessionMiddleware

from importlib import import_module
from django.conf import settings

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import list_route

from .models import SessionDetails
from .serializers import SessionDetailsSerializer

import os, common, sqlite3, subprocess, NetworkManager, crypt, pwd, getpass, spwd, socket, json, re, glob

# dashboard db
dashboard_db = "/datafs/titania/dashboard.sqlite3"
dapps_store_json = "/run/apps.json"

# get Session store from settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

# fetch network AP details
nm = NetworkManager.NetworkManager
wlans = [d for d in nm.Devices if isinstance(d, NetworkManager.Wireless)]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# fetch details of build version; called only once
def get_builddetails():
    """
    PRETTY_NAME of your Titania os (in lowercase).
    """
    with open("/etc/os-release") as f:
        osfilecontent = f.read().split("\n")
        # $PRETTY_NAME is at the 5th position
        version = osfilecontent[4].split('=')[1].strip('\"')
        build_id = osfilecontent[5].split('=')[1].strip('\"')
        # ux_id = osfilecontent[6].split('=')[1].strip('\"')
    platform = subprocess.check_output(common.GET_PLATFORM, shell=True, timeout=10).decode("utf-8").split('\n')[0]

    # wifi support according to hardware
    wifi_support = True
    available_devices = subprocess.check_output(common.GET_WIRELESS_DEVICES, shell=True, timeout=10).decode("utf-8")
    if len(available_devices) == 0:
        wifi_support = False

    return version, build_id, platform, wifi_support

# fetch system details
version, build_id, platform, wifi_support = get_builddetails()

def get_allconfiguredwifi():
    """
    nmcli con | grep 802-11-wireless
    """
    ps = subprocess.Popen('nmcli -t -f NAME,TYPE conn | grep 802-11-wireless', shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    wifirows = ps.split('\n')
    wifi = []
    for row in wifirows:
        name = row.split(':')
        print(name)
        wifi.append(name[0])
    return wifi

def get_allAPs():
    """
    nmcli con | grep 802-11-wireless
    """
    ps = subprocess.Popen('nmcli -t -f SSID,BARS device wifi list', shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    wifirows = ps.split('\n')
    wifi = []
    for row in wifirows:
        entry = row.split(':')
        print(entry)
        wifi.append(entry)
    return wifi
    # wifi_aps = []   
    # for dev in wlans:
    #     for ap in dev.AccessPoints:
    #         wifi_aps.append(ap.Ssid)
    # return wifi_aps

def get_ifconfigured():
    # get count of the number of docker users
    # docker:x:992:
    ps = subprocess.Popen('getent group | grep docker', shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    # remove /n
    output_string = ps.split('\n')[0]
    # get users
    users_list = output_string.split(':')[3]
    # if no docker users have been set yet, go to configure
    if len(users_list) == 0:
        return False
    else:
        return True

# logic to determine update status
#
# systemctl is-active update-process->|__ active -> get Perc of update 'updating'/ success / failure
#                                     |__inactive (systemctl status parsing) __ has not started 'initial'

# systemctl status parsing logic
# - initial state: inactive (dead)
# - success state: active (exited)
# - failure: active (exited) (Result: exit-code)

def get_updatestatus(service_name):
    print(service_name)
    data = {}
    is_activecall = 'systemctl is-active {}'.format(service_name)
    service_status = 'systemctl status {}'.format(service_name)
    print(is_activecall)
    state = subprocess.Popen(is_activecall, shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split('\n')[0]
    print(state)
    if state == 'inactive':
        print("Update not started yet")
        return 'initial', data
    elif state == 'active':
        print("Success/Failure/In Progress")
        status = subprocess.Popen(service_status, shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split('\n')[2]
        # '   Active: active (exited) since Wed 2018-03-28 18:46:01 UTC; 3h 35min ago'
        if 'active' in status and '(exited)' in status:
            if 'exit-code' in status:
                return 'failure', {}
            else:
                return 'success', {}
        elif 'active' in status:
            # for in progress
            try:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect("/tmp/swupdateprog")
                data = json.loads(sock.recv(8192, socket.MSG_WAITALL).decode('ascii'))
                sock.close()
                print(data)
                return 'updating', data
            except FileNotFoundError:
                print("No socket, either update is not started or has finished")
                return 'initial', data
            except ConnectionRefusedError:
                return 'failure', data
    elif state == 'failed':
        return 'failure', {}
    else:
        return 'initial', data

def get_dappsdetails():
    active_service_list = []
    dapps_store = json.load(open(dapps_store_json))
    dapps_list = list(dapps_store)
    # downloaded images
    downld_service_list = subprocess.Popen(common.DOWNLOADED_SERVICES,shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split('\n')
    # iterate through manifest
    for dapp in dapps_list:
        service_repo = dapp["image"]
        service_tag = dapp["tags"][0]
        service = 'dapp@{}.service'.format(dapp["id"])
        print(service_tag)
        if service_tag == "helper":
            # helper function, default is enabled
            dapp["is_active"] = common.SERVICE_ENABLED_AND_ACTIVE
        elif check_ifserviceenabled(dapp["id"]):
            if check_ifserviceactive(dapp["id"]):
                dapp["is_active"] = common.SERVICE_ENABLED_AND_ACTIVE
            else:
                dapp["is_active"] = common.SERVICE_ENABLED_AND_NOT_ACTIVE
        elif service_repo in downld_service_list: 
            dapp["is_active"] = common.SERVICE_DISABLED
        else:
            # not downloaded / downloading
            if check_ifservicedownloading(dapp["id"]) != "run":
                dapp["is_active"] = common.SERVICE_DOWNLOADING
            else:
                dapp["is_active"] = common.SERVICE_NOT_DOWNLOADED    
    return dapps_list

def get_containerswithavailableupdate():
    dapps_store = json.load(open(dapps_store_json))
    dapps_list = list(dapps_store)
    update_list = []
    for dapp in dapps_list:
        if check_ifserviceupdateavailable(dapp["id"]):
            update_list.append(dapp["id"])
    return update_list

def check_ifserviceenabled(dappid):
    is_enabled_service = common.IS_ENABLED_SERVICE.format(dappid)
    return subprocess.Popen(is_enabled_service, shell=True, stdout=subprocess.DEVNULL).wait() == 0

def check_ifserviceactive(dappid):
    is_active_service = common.IS_ACTIVE_SERVICE.format(dappid)
    return subprocess.Popen(is_active_service, shell=True, stdout=subprocess.DEVNULL).wait() == 0

def check_ifserviceupdateavailable(dappid):
    is_update_available = common.SERVICE_UPDATE_AVAILABLE_CHECK.format(dappid)
    update_available = subprocess.Popen(is_update_available,shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split('\n')[0]
    if update_available == "download":
        return True
    elif update_available == "latest":
        return False

def check_ifservicedownloading(dappid):
    CMD = [ "systemctl", "status", "--no-pager", "dapp@{}".format(dappid) ]
    print(CMD)
    # Ideally decode to utf-8, but Titania doesn't seem to like it right now
    for ln in subprocess.run(CMD, stdout=subprocess.PIPE).stdout.decode('ascii', 'ignore').split('\n'):
        # TODO: you can also handle PID: XYZ (docker) for running state
        print(ln)
        m = re.search(r'PID: [0-9]* \(dapp_([a-z]*)\.sh\)', ln)
        if m:
            return m.group(1)
    return "run"

def check_ifnatpmpenabled():
    CMD = [ "systemctl", "is-active", "natpmp-support.service", "--no-pager" ]
    output = subprocess.run(CMD, stdout=subprocess.PIPE).stdout.decode('ascii', 'ignore').split('\n')[0]
    if output == 'failed':
        return '0'
    else:
        return '1'

def validate_session(request):
    session_key = request.POST.get("session_key")
    try:
        key_exists = SessionDetails.objects.get(session_key=session_key)
    except (SessionDetails.DoesNotExist):
        return False
    return True

def validate_input(inputstring):
    while not re.match("^[a-zA-Z0-9_]*$", inputstring) and len(inputstring) > 0:
        print ("This uses beyond alphanumeric data")
        return False
    else:
        return True

def validate_filename(filename):
    print("validate_filename")
    return True

def set_boxname(boxname):
    # setting hostname, this will change the mask from titania.local
    subprocess.call(['hostnamectl','set-hostname',boxname])

    # restart avahi and llnrd
    subprocess.call(['systemctl','restart','avahi-daemon'])

def add_user(username, password):
    # create a random sal for the user and encrypt password with sha512
    encPass = crypt.crypt(password,crypt.mksalt(crypt.METHOD_SHA512))
    # subprocess escapes the username stopping code injection
    subprocess.call(['useradd','-G','docker,wheel','-p',encPass,username])
    
def add_newWifiConn(wifiname, wifiencrypt, wifipass):
    wlan0 = wlans[0]
    # get selected ap as currentwifi
    for dev in wlans:
        for ap in dev.AccessPoints:
            if ap.Ssid == wifiname:
                currentwifi = ap
    print(wifipass, wifiencrypt, wifiname)
    # params to set password
    if len(wifipass) == 0: #open wifi
        params = {
                    "802-11-wireless": {
                        "security": "open-wifi",
                    },
                    "open-wifi": {
                        "key-mgmt": "none",
                    }
                }
    else: 
        if wifiencrypt == "WPA (default)":
            params = {
                    "802-11-wireless": {
                        "security": "802-11-wireless-security",
                    },
                    "802-11-wireless-security": {
                        "key-mgmt": "wpa-psk",
                        "psk": wifipass
                    },
                }
        elif wifiencrypt == "WEP":
            params = {
                    "802-11-wireless": {
                        "security": "open-wifi",
                    },
                    "open-wifi": {
                        "key-mgmt": "none",
                        "wep_key0": wifipass,
                        "wep_tx_keyidx": "0"
                    },
                }
        else:
            params = {
                    "802-11-wireless": {
                        "security": "open-wifi",
                    },
                    "open-wifi": {
                        "key-mgmt": "none",
                    }
                }

    conn = nm.AddAndActivateConnection(params, wlan0, currentwifi)        

def delete_WifiConn(wifiap):
    """
    nmcli connection delete id <connection name>
    """
    cmd = 'nmcli connection delete id \'{}\''.format(wifiap)
    ps = subprocess.Popen(['nmcli', 'connection','delete','id',wifiap], stdout=subprocess.PIPE).communicate()[0]
    print(ps)

def edit_WifiConn(wifiname, wifipass):
    delete_WifiConn(wifiname)
    wlan0 = wlans[0]
    # get selected ap as currentwifi
    for dev in wlans:
        for ap in dev.AccessPoints:
            if ap.Ssid == wifiname:
                currentwifi = ap
    # params to set password
    params = {
            "802-11-wireless": {
                "security": "802-11-wireless-security",
            },
            "802-11-wireless-security": {
                "key-mgmt": "wpa-psk",
                "psk": wifipass
            },
        }
    conn = nm.AddAndActivateConnection(params, wlan0, currentwifi) 
    return     

# delete all session entries on startup
def reset_sessions_on_startup():
    try:
        initSessions = SessionDetails.objects.all().delete()
    except:
        print('Initial Startup')  

@csrf_exempt
def handle_config(request):
    """
    List all code snippets, or create a new snippet.
    """ 
    if request.method == 'POST':
        action = request.POST.get("_action")
        if validate_input(action):        
            # valid containers         
            docker_ids = subprocess.check_output(common.CMD_VALID_DOCKER_ID, shell=True, timeout=10).decode("utf-8").split('\n')

            if action == 'getSchema':
                return JsonResponse({"version":version, "build_id":build_id, "platform":platform, "wifi_support": wifi_support}, safe=False)
            elif action == 'getIfConfigured':
                configured = get_ifconfigured()
                # queryset = BoxDetails.objects.all()
                # serializer = BoxDetailsSerializer(queryset, many=True)
                return JsonResponse({"configState":configured}, safe=False)
            elif action == 'getAllAPs':
                wifi_aps = get_allAPs()
                return JsonResponse(wifi_aps, safe=False)
            elif action == 'saveUserDetails':
                print(action)
                boxname = request.POST.get("boxname")
                username = request.POST.get("username")
                password = request.POST.get("password")
                if validate_input(boxname) and validate_input(username) and not get_ifconfigured():
                    subprocess.Popen(['usermod', '--lock', 'root']).wait()
                    set_boxname(boxname)
                    wifi_pass = request.POST.get("wifi_password")
                    wifi_name = request.POST.get("wifi_ap")
                    wifi_encrpt = request.POST.get("wifi_encrpt")
                    if len(wifi_name) > 0:
                        add_newWifiConn(wifi_name, wifi_encrpt,wifi_pass)
                    add_user(username,password)
                    return JsonResponse({"STATUS":"SUCCESS"}, safe=False)
            elif action == 'login':
                print(action)
                username = request.POST.get("username")
                password = request.POST.get("password")
                if validate_input(username):
                    output=''
                    """Tries to authenticate a user.
                    Returns True if the authentication succeeds, else the reason
                    (string) is returned."""
                    try:
                        enc_pwd = spwd.getspnam(username)[1]
                        if enc_pwd in ["NP", "!", "", None]:
                            output = "User '%s' has no password set" % username
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
                            output = "login failed"
                    except KeyError:
                        output = "login failed"
                    if len(output) == 0:
                        # insert session code here
                        if not request.session.exists(request.session.session_key):
                            request.session.create() 
                            print(request.session.session_key)
                            print(get_client_ip(request))
                            setSessionRow = SessionDetails(session_key=request.session.session_key,username=username,client_ip=get_client_ip(request))
                            setSessionRow.save()
                        return JsonResponse({"username":username, "session_key": request.session.session_key}, safe=False)
                    else:
                        return JsonResponse(output, safe=False)
            if validate_session(request):
                if action == 'logout':
                    print(action)
                    username = request.POST.get("username")
                    if validate_input(username):
                        # delete loop for session id
                        deleteSessionRows = SessionDetails.objects.filter(username=username).delete()
                        deleteSessionRows.save()
                        return JsonResponse({"STATUS":"SUCCESS", "username":username}, safe=False)
                elif action == 'getDashboardCards':
                    print(action)
                    con = sqlite3.connect(dashboard_db)
                    cursor = con.cursor()
                    cursor.execute(common.Q_DASHBOARD_CARDS)
                    rows = cursor.fetchall()
                    return JsonResponse(rows, safe=False)
                elif action == 'getDashboardChart':
                    print(action)
                    con = sqlite3.connect(dashboard_db)
                    cursor = con.cursor()
                    # cursor.execute(common.Q_GET_CONTAINER_ID)
                    # rows = cursor.fetchall()
                    p = subprocess.check_output(common.CMD_DOCKER_MASTER, shell=True, timeout=10)
                    p = p.decode("utf-8")
                    p = p.split('\n')
                    lenofoutput = len(p)
                    finalset = []
                    for row in range(lenofoutput-1):
                        y = p[row].split('\t')
                        cursor.execute(common.Q_GET_DASHBOARD_CHART,[y[0],])
                        datasets = cursor.fetchall()
                        # print(datasets)
                        data = {'container_name' : y[1], 'data': datasets}
                        finalset.append(data)
                    return JsonResponse(finalset, safe=False)
                elif action == 'getDockerOverview':
                    print(action)
                    con = sqlite3.connect(dashboard_db)
                    cursor = con.cursor()
                    cursor.execute(common.Q_GET_DOCKER_OVERVIEW)
                    rows = cursor.fetchall()
                    # print(rows)
                    finalset = []
                    for row in rows:
                        if row[1] in docker_ids:
                            data = {'state': row[0], 'container_id': row[1], 'name': row[2],
                                    'image': row[3], 'running_for': row[4],
                                    'command': row[5], 'ports': row[6],
                                    'status': row[7], 'networks': row[8]}
                            finalset.append(data)
                    return JsonResponse(finalset, safe=False)
                elif action == 'getContainerStats':
                    print(action)
                    con = sqlite3.connect(dashboard_db)
                    cursor = con.cursor()
                    # cursor.execute(common.Q_GET_CONTAINER_ID)
                    # rows = cursor.fetchall()
                    # print(rows)

                    finalset = []
                    datasets_io = []
                    datasets_mem = []
                    datasets_perc = []

                    p = subprocess.check_output(common.CMD_DOCKER_MASTER, shell=True, timeout=10)
                    p = p.decode("utf-8")
                    p = p.split('\n')
                    lenofoutput = len(p)
                    finalset = []
                    for row in range(lenofoutput-1):
                        y = p[row].split('\t')
                        datasets_io = []
                        datasets_mem = []
                        datasets_perc = []
                        # values with % appended to them
                        for iter in range(0,2):
                            cursor.execute(common.Q_GET_CONTAINER_STATS_CPU,[y[0],iter+1])
                            counter_val = cursor.fetchall()
                            datasets_perc.append(counter_val)
                        # values w/o % appended to them
                        for iter in range(2,4):
                            cursor.execute(common.Q_GET_CONTAINER_STATS,[y[0],iter+1])
                            counter_val = cursor.fetchall()
                            datasets_mem.append(counter_val)
                        # values w/o % appended to them
                        for iter in range(4,8):
                            cursor.execute(common.Q_GET_CONTAINER_STATS,[y[0],iter+1])
                            counter_val = cursor.fetchall()
                            datasets_io.append(counter_val)
                        data = {'container_id': y[0], 'container_name' : y[1], 'data_io': datasets_io, 'data_mem': datasets_mem, 'data_perc': datasets_perc}
                        finalset.append(data)
                    return JsonResponse(finalset, safe=False)
                elif action == 'getThreads':
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
                    con = sqlite3.connect(dashboard_db)
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
                        data = {'container_id': i[0], 'container_name' : i[1], 'data': datasets}
                        resultset.append(data)
                    return JsonResponse(resultset, safe=False)
                elif action == 'getSettings':
                    print(action)
                    ps = subprocess.Popen(['grep', '/etc/group','-e','docker'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').split('\n')[0]
                    # sample ps 
                    # docker:x:992:pooja,asdasd,aaa,cow,dsds,priya,asdas,cowwwwww,ramm,asdasdasdasd,asdasdas,adam,run
                    userlist = ps.split(':')[3].split(',')
                    configuredwifi = get_allconfiguredwifi()
                    wifi_aps = get_allAPs()
                    return JsonResponse([{'users':userlist,'wifi':configuredwifi,'allwifiaps':wifi_aps}], safe=False)
                elif action == 'deleteUser':
                    print(action)
                    username = request.POST.get("username")
                    if validate_input(username):
                        ps = subprocess.Popen(['userdel', username], stdout=subprocess.PIPE).communicate()
                        fetchusers = subprocess.Popen(['grep', '/etc/group','-e','docker'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').split('\n')[0]
                        # sample ps 
                        # docker:x:992:pooja,asdasd,aaa,cow,dsds,priya,asdas,cowwwwww,ramm,asdasdasdasd,asdasdas,adam,run
                        userlist = fetchusers.split(':')[3].split(',')
                        configuredwifi = get_allconfiguredwifi()
                        wifi_aps = get_allAPs()
                        return JsonResponse([{'users':userlist,'wifi':configuredwifi,'allwifiaps':wifi_aps, 'reqtype': 'deleteuser', 'endpoint': username}], safe=False)
                elif action == 'addNewUser':
                    print(action)
                    username = request.POST.get("username")
                    password = request.POST.get("password")
                    if validate_input(username):
                        add_user(username,password)
                        fetchusers = subprocess.Popen(['grep', '/etc/group','-e','docker'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').split('\n')[0]
                        # sample ps 
                        # docker:x:992:pooja,asdasd,aaa,cow,dsds,priya,asdas,cowwwwww,ramm,asdasdasdasd,asdasdas,adam,run
                        userlist = fetchusers.split(':')[3].split(',')
                        configuredwifi = get_allconfiguredwifi()
                        wifi_aps = get_allAPs()
                        return JsonResponse([{'users':userlist,'wifi':configuredwifi,'allwifiaps':wifi_aps, 'reqtype': 'adduser', 'endpoint': username}], safe=False)
                elif action == 'addWifi':
                    # connect to wifi ap user selected
                    wifi_pass = request.POST.get("wifi_password")
                    wifi_name = request.POST.get("wifi_ap")
                    wifi_encrpt = request.POST.get("wifi_encrpt")
                    if len(wifi_name) > 0:
                        add_newWifiConn(wifi_name,wifi_encrpt,wifi_pass)
                    fetchusers = ''
                    fetchusers = subprocess.Popen(['grep', '/etc/group','-e','docker'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').split('\n')[0]
                    # sample ps 
                    # docker:x:992:pooja,asdasd,aaa,cow,dsds,priya,asdas,cowwwwww,ramm,asdasdasdasd,asdasdas,adam,run
                    userlist = fetchusers.split(':')[3].split(',')
                    configuredwifi = get_allconfiguredwifi()
                    print(configuredwifi)
                    wifi_aps = get_allAPs()
                    print(wifi_aps)
                    return JsonResponse([{'users':userlist,'wifi':configuredwifi,'allwifiaps':wifi_aps, 'reqtype': 'addwifi', 'endpoint': wifi_name}], safe=False)
                elif action == 'deleteWifi':
                    print(action)
                    # connect to wifi ap user selected
                    wifi_name = request.POST.get("wifi_ap")
                    delete_WifiConn(wifi_name)
                    fetchusers = subprocess.Popen(['grep', '/etc/group','-e','docker'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').split('\n')[0]
                    # sample ps 
                    # docker:x:992:pooja,asdasd,aaa,cow,dsds,priya,asdas,cowwwwww,ramm,asdasdasdasd,asdasdas,adam,run
                    userlist = fetchusers.split(':')[3].split(',')
                    configuredwifi = get_allconfiguredwifi()
                    wifi_aps = get_allAPs()
                    return JsonResponse([{'users':userlist,'wifi':configuredwifi,'allwifiaps':wifi_aps, 'reqtype': 'deletewifi', 'endpoint': wifi_name}], safe=False)
                elif action == 'editWifi':
                    print(action)
                    # connect to wifi ap user selected
                    wifi_name = request.POST.get("wifi_ap")
                    wifi_pass = request.POST.get("wifi_password")
                    if validate_input(wifi_name) and validate_input(wifi_pass):
                        edit_WifiConn(wifi_name,wifi_pass)
                        fetchusers = subprocess.Popen(['grep', '/etc/group','-e','docker'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').split('\n')[0]
                        # sample ps 
                        # docker:x:992:pooja,asdasd,aaa,cow,dsds,priya,asdas,cowwwwww,ramm,asdasdasdasd,asdasdas,adam,run
                        userlist = fetchusers.split(':')[3].split(',')
                        configuredwifi = get_allconfiguredwifi()
                        wifi_aps = get_allAPs()
                        return JsonResponse([{'users':userlist,'wifi':configuredwifi,'allwifiaps':wifi_aps, 'reqtype': 'editwifi', 'endpoint': wifi_name}], safe=False)
                elif action == 'fetchAlldApps':
                    print(action)
                    dapps_list = get_dappsdetails()
                    return JsonResponse({'STATUS':'SUCCESS','dapps_store':dapps_list}, safe=False)
                elif action == 'fetchUpdatableDapps':
                    update_list = get_containerswithavailableupdate()
                    print(update_list)
                    return JsonResponse({'STATUS':'SUCCESS','update_list':update_list}, safe=False)
                elif action == 'disableDapp':
                    print(action)
                    dappid = request.POST.get("id")
                    service = common.SERVICE_DISABLE.format(dappid)
                    os.system(service)
                    return JsonResponse({'STATUS':'SUCCESS'}, safe=False)
                elif action == 'enableDapp':
                    print(action)
                    dappid = request.POST.get("id")
                    service = common.SERVICE_ENABLE.format(dappid)
                    os.system(service)
                    return JsonResponse({'STATUS':'SUCCESS'}, safe=False)
                elif action == 'restartDapp':
                    print(action)
                    dappid = request.POST.get("id")
                    service = common.SERVICE_RESTART.format(dappid)
                    os.system(service)
                    return JsonResponse({'STATUS':'SUCCESS'}, safe=False)
                elif action == 'removeDapp':
                    print(action)
                    # docker rm world.libertaria.nginx 
                    # docker rmi libertaria/nginx:armv7 
                    dappid = request.POST.get("id")
                    image = request.POST.get("image")
                    service = common.DOCKER_RM_DAPP.format(dappid,image)
                    print(service)
                    os.system(service)
                    return JsonResponse({'STATUS':'SUCCESS'}, safe=False)
                elif action == 'downloadDapp':
                    print(action)
                    # docker pull <image>
                    # image = request.POST.get("image")
                    dappid = request.POST.get("id")
                    service = common.DAPP_DOWNLOAD.format(dappid)
                    print(service)
                    ps = subprocess.Popen(service,shell=True,stdout=subprocess.PIPE).communicate()[0]
                    print(ps)
                    return JsonResponse({'STATUS':'SUCCESS'}, safe=False)
                elif action == 'updateDapp':
                    print(action)
                    dappid = request.POST.get("id")
                    service = common.SERVICE_UPDATE.format(dappid)
                    print(service)
                    ps = subprocess.Popen(service,shell=True,stdout=subprocess.PIPE).communicate()[0]
                    print(ps)
                    return JsonResponse({'STATUS':'SUCCESS'}, safe=False)
                elif action == 'updateOSImage':
                    print(action)
                    data = request.FILES['file']
                    print(data)
                    if data:
                        # delete existing files before downloading new swu file
                        rm_file_regex = settings.MEDIA_ROOT + common.SWU_FILE_FORMAT
                        for filename in glob.glob(rm_file_regex) :
                            try:
                                os.remove( filename )
                            except OSError as e:  ## if failed, report it back
                                print(e)
                        # save file from persistent store to /tmp
                        path = default_storage.save(data.name, ContentFile(data.read()))
                        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                        # update call
                        file_path = settings.MEDIA_ROOT + data.name
                        # systemctl start swupdate@$(systemd-escape -p /tmp/titania-arm-rpi-v0.0-152-g3668500.swu).service
                        update_cmd = 'systemctl start swupdate@$(systemd-escape -p {}).service'.format(file_path)
                        print(update_cmd)
                        os.system(update_cmd)
                        return JsonResponse({'STATUS':'SUCCESS'}, safe=False)
                elif action == 'getUpdateStatus':
                    print(action)
                    image_name = request.POST.get("image_name")
                    file_path = settings.MEDIA_ROOT + image_name
                    print(action)
                    update_service = 'swupdate@$(systemd-escape -p {}).service'.format(file_path)
                    status, data = get_updatestatus(update_service)
                    print(status)
                    print(data)
                    # systemctl start swupdate@$(systemd-escape -p /tmp/titania-arm-rpi-v0.0-152-g3668500.swu).service
                    return JsonResponse({'STATUS':status,'data':data}, safe=False)  
                elif action == 'getNatpmpStatus':
                    print(action)
                    natpmp_status = check_ifnatpmpenabled()
                    return JsonResponse({'STATUS': natpmp_status}, safe=False)  
                elif action == 'rebootSystem':
                        print(action)
                        os.system('systemd-run --on-active=1 --timer-property=AccuracySec=100ms /sbin/shutdown -r now')
                        return JsonResponse({'STATUS':'SUCCESS'}, safe=False)  
                return JsonResponse({'STATUS':'FAILURE'}, safe=False)
            elif action == 'getUpdateStatus' or action == 'getNatpmpStatus':
                # TO DO, come up with bettr soln to handle this call output
                return JsonResponse({'STATUS':'FAILURE'}, safe=False)
            else:
                return JsonResponse({'STATUS':'REDIRECT'}, status=302)
    return JsonResponse({'STATUS':'FAILURE'}, safe=False)   

def index(request):
    return render(request, 'index.html')

class SessionDetailsViewSet(viewsets.ModelViewSet):
    queryset = SessionDetails.objects.all()
    serializer_class = SessionDetailsSerializer
