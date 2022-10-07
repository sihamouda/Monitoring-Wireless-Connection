import subprocess
#import re
import time
#import platform
#import matplotlib.pyplot as plt
#import numpy as np

def get_Signal_Power(data):
    i=int(data.find("Signal level="))
    return i

def read_data_from_cmd():
    p= subprocess.Popen("iwconfig",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    return(out)
    
def show_Signal_Power(data):
    i=0
    while(i<5):
        print(data[get_Signal_Power(data)+13:get_Signal_Power(data)+16])
        i+=1
        time.sleep(1)

data=read_data_from_cmd()
show_Signal_Power(data)
