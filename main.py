import subprocess
#import re
import time
import datetime
#import platform
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#import numpy as np

def get_Signal_Power(data):
    i=int(data.find("Signal level="))
    return i

def read_data_from_cmd():
    p= subprocess.Popen("iwconfig",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    return(out)

curtime,sp=[], []
data=read_data_from_cmd()

def show_Signal_Power(i):    
    curtime.append(datetime.datetime.now())
    sp.append(data[get_Signal_Power(data)+13:get_Signal_Power(data)+16])

    plt.cla()
    plt.plot(curtime,sp)



animate = FuncAnimation(plt.gcf(),show_Signal_Power,interval=1000)
plt.tight_layout()
plt.show()