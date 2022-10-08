import subprocess
#import re
import time
import datetime
import platform
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pprint import  pprint as pp
#import numpy as np

def get_Signal_Power(data):
    i=int(data.find("Signal level="))
    return i

def read_data_from_cmd():
    p= subprocess.Popen("iwconfig",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    return(out)

#curtime,sp=[], []
#data=read_data_from_cmd()

def show_Signal_Power(i):    
    curtime.append(datetime.datetime.now())
    sp.append(data[get_Signal_Power(data)+13:get_Signal_Power(data)+16])

    plt.cla()
    plt.plot(curtime,sp)

#animate = FuncAnimation(plt.gcf(),show_Signal_Power,interval=1000)
#plt.tight_layout()
#plt.show()

def show_network():
    cmd = "nmcli device wifi"
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    return out

def networks_List(data):    
    names=data.splitlines()[0].split()
    networks=[]
    
    for line in data.splitlines()[1:]:
        if line.split()[0] != '*':
            newLine=['False']+line.split()
        else:
            newLine=['True']+line.split()[1:] 
        
        if newLine.index('Infra') != 3:
            SSID=' '.join(newLine[2:newLine.index('Infra')])
            newLine[2]=SSID
            del newLine[3:newLine.index('Infra')]
        
        RATE=' '.join(newLine[5:7])
        newLine[5]=RATE
        del newLine[6]

        if len(newLine) > 9:
            SECURITY=' '.join(newLine[8:])
            newLine[8]=SECURITY
            del newLine[9:]
        
        networks.append(dict(zip(names,newLine)))
    
    return(networks)

def detect_best_network():
    signal=0
    SSID=''
    for network in networks_List(show_network()):
        s = int(network['SIGNAL'])
        if s > signal:
            signal=s
            SSID=network['SSID']

    SSID="\ ".join(SSID.split())
    return SSID

def connect_network(SSID):
    cmd="nmcli device wifi connect "+SSID
    print(cmd)
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    err = p.stderr.read().decode()
    print(out)
    print(err)

#detect_best_network()
connect_network(detect_best_network())