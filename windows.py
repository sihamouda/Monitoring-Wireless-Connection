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


# This function will return the output of a Windows command as a string using subprocess
def read_data_from_cmd(cmd):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out = p.stdout.read().decode("unicode_escape")
    err = p.stderr.read().decode("unicode_escape")
    return out, err


# This function will parse the result of a Windows command using regular expressions
# We will used it specifically to get the signal power in %
def get_signal_power(cmd_result):
    signal_power = re.findall("Signal.*?:.*?([0-9]*)%", cmd_result, re.DOTALL)
    return signal_power


# print(get_signal_power(read_data_from_cmd('netsh wlan show interfaces')[0]))

# This function will parse the result of a Windows command using regular expressions
# We will used it specifically to get the ssid
def get_ssid(cmd_result):
    result = re.findall("SSID.*?ÿ:.*?([A-z0-9- ]*)", cmd_result, re.DOTALL)
    return result


# This function will show us a real time graph of the current AP' signal power in %
def wifi_statistics():
    current_time = []
    signal_power = []

    def show_signal_power(i):
        plt.style.use("fivethirtyeight")
        current_time.append(datetime.datetime.now())

        sp_int = int(
            get_signal_power(read_data_from_cmd("netsh wlan show interfaces")[0])[0]
        )
        signal_power.append(sp_int)

        # pp(signal_power)
        plt.cla()
        plt.plot(current_time, signal_power)

    animate = FuncAnimation(plt.gcf(), show_signal_power, interval=1000)
    plt.tight_layout()
    plt.show()


# wifi_statistics()

# read_data_from_cmd("netsh wlan show networks mode=Bssid")[0]

# This function will return available networks in a list of dicts
def get_networks():
    cmd_result = read_data_from_cmd("netsh wlan show networks mode=Bssid")[0]
    ssids = get_ssid(cmd_result)
    print(ssids)
    ssids = ssids[0::2]
    signal_power = get_signal_power(cmd_result)

    names = ["SSID", "SIGNAL"]
    lines = [list(tup) for tup in zip(ssids, signal_power)]

    networks = []
    for line in lines:
        networks.append(dict(zip(names, line)))
    print(networks)
    return networks


# this function will detect best network
def detect_best_network():
    signal = 0
    ssid = ""

    networks = get_networks()

    for network in networks:
        s = int(network["SIGNAL"])
        if s > signal:
            signal = s
            ssid = network["SSID"]

    return ssid[1:]


# print(detect_best_network())


def connect_network(ssid):

    cmd = "netsh wlan connect name='" + ssid + "'"

    result = read_data_from_cmd(cmd)
    print(result)
    # if result[0] == '':
    #    cmd = "notify-send 'error while connecting'"
    #    subprocess.Popen(cmd, shell=True)
    # else:
    #    cmd = "notify-send 'connected to "+ ssid +"'"
    #    subprocess.Popen(cmd, shell=True)


connect_network(detect_best_network())
