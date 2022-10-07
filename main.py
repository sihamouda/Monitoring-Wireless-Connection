import subprocess
#import re
#import time
#import platform
#import matplotlib.pyplot as plt
#import numpy as np

def read_data_from_cmd():
    p= subprocess.Popen("iwconfig",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = p.stdout.read().decode()
    print(out)
    

read_data_from_cmd()
