# To pass shell commands we use subprocess
import subprocess

# To parse data using regular expressions we use re
import re

# To make a graph of the current AP' signal power
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# To get date and time
import datetime

# To print list in a nice way: mainly for testing
from pprint import pprint as pp


# This function will return the output of a Linux command as a string using subprocess
def read_data_from_shell(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out = p.stdout.read().decode()
    err = p.stderr.read().decode()
    return out, err


# This function will parse the result of a Linux command using regular expressions
# We will used it specifically to get the signal power in dBm
def get_signal_power(cmd_result):
    signal_power = re.findall("Signal level=(-[0-9]+) dBm", cmd_result, re.DOTALL)
    sp_int = int(signal_power[0])
    return sp_int


# This function will show us a real time graph of the current AP' signal power in dBm
def wifi_statistics():
    current_time = []
    signal_power = []

    def show_signal_power(i):
        plt.style.use("fivethirtyeight")
        current_time.append(datetime.datetime.now())
        signal_power.append(get_signal_power(read_data_from_shell("iwconfig")[0]))

        # pp(signal_power)
        plt.cla()
        plt.plot(current_time, signal_power)

    animate = FuncAnimation(plt.gcf(), show_signal_power, interval=1000)
    plt.tight_layout()
    plt.show()


# This function is used to convert the available networks table to list of dictonaries
def get_networks(cmd_result):
    cmd_result_list = cmd_result.splitlines()
    names = cmd_result_list[0].split()
    networks = []

    for line in cmd_result_list[1:]:
        if line.split()[0] != "*":
            newLine = ["False"] + line.split()
        else:
            newLine = ["True"] + line.split()[1:]

        if newLine.index("Infra") != 3:
            ssid = " ".join(newLine[2 : newLine.index("Infra")])
            newLine[2] = ssid
            del newLine[3 : newLine.index("Infra")]

        rate = " ".join(newLine[5:7])
        newLine[5] = rate
        del newLine[6]

        if len(newLine) > 9:
            security = " ".join(newLine[8:])
            newLine[8] = security
            del newLine[9:]

        networks.append(dict(zip(names, newLine)))

    return networks


# This function will detect the best available network
def detect_best_network():
    signal = 0
    ssid = ""
    cmd = "nmcli device wifi"

    networks = get_networks(read_data_from_shell(cmd)[0])

    for network in networks:
        s = int(network["SIGNAL"])
        if s > signal:
            signal = s
            ssid = network["SSID"]

    return ssid


# This function will connect to a network with given SSID
def connect_network(ssid):
    ssid = "\ ".join(ssid.split())
    cmd = "nmcli device wifi connect " + ssid

    read_data_from_shell(cmd)[0]
