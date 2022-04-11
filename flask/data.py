from crypt import methods
from email import header
from flask_cors import CORS
from flask import Flask, jsonify
import os
import psutil
import csv
import platform
import getpass
import time
import datetime
import warnings
from pynvml import *
import json


def getData():
    data_dict = {
        "state": True,
        "nvidia_count": 0,
        "gpu0": {},
        "gpu1": {},
        "cpu": 0,
    }
    nvmlInit()
    data_dict['nvidia_count'] = nvmlDeviceGetCount()
    data_dict['cpu'] = str(psutil.cpu_percent(1))
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
        name = 'gpu' + str(i)
        data_dict[name] = gpu
    print(data_dict['gpu0'])
    print(data_dict['gpu1'])
    if data_dict['gpu0'] != {}:
        data_dict['state'] = True
    else:
        data_dict['state'] = False

    return data_dict


if __name__ == '__main__':
    cnt = 0
    header = ['state', 'nvidia_count', 'gpu0', 'gpu1', 'cpu']
    with open('data.csv', 'w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        writer.writeheader()  # 写入列名
    while True:
        time.sleep(5)
        cnt += 5
        if cnt % 3600 == 0:
            print("已运行{}h---------------------".format(cnt / 3600))
        with open('data.csv', 'a', newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
            writer.writerow(getData())  # 写入数据
