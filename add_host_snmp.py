#coding:utf-8

import json
import requests
import xlrd

def login(user, password):
    post_data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": user,
            "password": password
        },
        "id": 1
    }
    ret = requests.post(url, data=json.dumps(post_data), headers=post_headers)
    print(ret.text)
    return json.loads(ret.text)['result']

def get_groupid(group_name):
    post_find = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                    group_name
                ]
            }
        },
        "auth": token,
        "id": 1
    }
    post_create = {
        "jsonrpc": "2.0",
        "method": "hostgroup.create",
        "params": {
            "name": group_name
        },
        "auth": token,
        "id": 1
    }

    #在zabbix中，查找该组名是否存在，如果存在，则返回组ID，否则新建组
    ret = requests.post(url, data=json.dumps(post_find), headers=post_headers)
    result = json.loads(ret.text)['result']

    if len(result) == 0:
        ret = requests.post(url, data=json.dumps(post_create), headers=post_headers)
        groupid = json.loads(ret.text)['result']['groupids'][0]
        return groupid
    else:
        groupid = result[0]['groupid']
        return groupid

def get_tempid(temp_name):
    post_find = {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": "extend",
            "filter": {
                "host": [
                    temp_name,
                ]
            }
        },
        "auth": token,
        "id": 1
    }
    ret = requests.post(url, data=json.dumps(post_find), headers=post_headers)
    temp_id = json.loads(ret.text)['result'][0]['templateid']
    return temp_id

def create_host(hostname, visible, ip, groupid, tempid, SN, type, port):
    post_data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": hostname,
            "name": visible,
            "interfaces": [
                {
                    "type": type,   # 1:agent; 2:SNMP; 3:IPMI; 4:JMX.
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": port,  #agent默认端口10050，SNMP默认161
                    "details": {
                        "version": 2,
                        "community": "{$SNMP_COMMUNITY}"
                }
                }
            ],
            "groups": [
                {
                    "groupid": groupid
                }
            ],
            "templates": [
                {
                    "templateid": tempid
                }
            ],
            "inventory_mode": 0,
            "inventory": {
                "serialno_a": SN,
            }
        },
        "auth": token,
        "id": 1
    }
    print(post_data)
    ret = requests.post(url, data=json.dumps(post_data), headers=post_headers)
    print(ret.text)

user = "Admin"
password = "zabbix"
url = 'http://192.168.1.220/zabbix/api_jsonrpc.php'
post_headers = {'Content-Type': 'application/json'}

token = login(user, password)


type = 2        # 1:agent; 2:SNMP; 3:IPMI; 4:JMX.
port = 161    #agent默认端口10050，SNMP默认161

workbook = xlrd.open_workbook("switch.xls")
table = workbook.sheets()[0]
for row in range(1, table.nrows):
    hostname = table.cell(row, 0).value
    visible = table.cell(row, 1).value
    ip = table.cell(row, 2).value
    groupid = get_groupid(table.cell(row, 3).value)
    tempid = get_tempid(table.cell(row, 4).value)
    SN = table.cell(row, 5).value
    print(hostname, visible, ip, groupid, tempid,SN)
    create_host(hostname,visible,ip,groupid,tempid,SN,type,port)
