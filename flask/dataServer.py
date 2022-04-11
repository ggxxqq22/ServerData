from crypt import methods
from flask_cors import CORS
from flask import Flask, jsonify
import os
import psutil
import platform
import getpass
import time
import datetime
import csv
import warnings
from pynvml import *
import json
warnings.filterwarnings("ignore")
charset = "utf8"
app = Flask(__name__)
CORS(app)


@app.route('/gpu', methods=['post', 'get'])
def gpu():
    nvidia_dict = {
        "state": True,
        "nvidia_count": 0,
        "gpus": []
    }
    nvmlInit()
    for i in range(nvmlDeviceGetCount()):
        handle = nvmlDeviceGetHandleByIndex(i)
        memory_info = nvmlDeviceGetMemoryInfo(handle)
        gpu = {
            "gpu_name": nvmlDeviceGetName(handle).decode('utf-8'),
            "total": memory_info.total,
            "free": memory_info.free,
            "used": memory_info.used,
            "temperature": f"{nvmlDeviceGetTemperature(handle, 0)}",
            "powerStatus": nvmlDeviceGetPowerState(handle)
        }
        nvidia_dict['gpus'].append(gpu)
    print(nvidia_dict['gpus'])
    if len(nvidia_dict['gpus']) != 0:
        nvidia_dict['state'] = True
    else:
        nvidia_dict['state'] = False
    return json.dumps(nvidia_dict)


@app.route('/cpu', methods=['post', 'get'])
def cpu():
    print(str(psutil.cpu_percent(1)) + '%')
    return str(psutil.cpu_percent(1)) + '%'


@app.route('/getData', methods=['post', 'get'])
def getdata():
    list = []
    with open('data.csv') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            list.append(row)

    return json.dumps(list[-1])


@app.route('/getHistory', methods=['post', 'get'])
def gethistory():
    list = []
    with open('data.csv') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            list.append(row)
    if list[0]['nvidia_count'] == '1':
        print("初始化res")
        res = {
            "gpu_count": 0,
            "cpu": [],
            "gpu0_tem": [],
            "gpu0_used": []
        }
        for i in range(len(list)):
            a = eval(list[i]['gpu0'])
            print(a)
            res['cpu'].append(list[i]['cpu'])
            res['gpu0_tem'].append(a['temperature'])
            res['gpu0_used'].append(a['used'])

    return json.dumps(res)


@app.route('/test', methods=['post', 'get'])
def test():
    list = []
    with open('data.csv') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            list.append(row)
    if list[0]['nvidia_count'] == '1':
        a = list[0]['gpu0']
        a = eval(a)
        print(a['used'])
        return "success"


@app.route('/init', methods=['post', 'get'])
def init():
    with open('data.csv', 'w') as f:
        c = csv.reader(f)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=10088)
