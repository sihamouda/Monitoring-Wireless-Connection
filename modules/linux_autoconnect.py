#!/bin/python3

import linux_common_tools as tools

# To pass shell commands we use subprocess
import subprocess

import json

from pprint import pprint as pp

# This function is used to convert the available networks table to list of dictonaries
def get_networks(cmd_result):
    cmd_result_list = cmd_result.splitlines()
    names = cmd_result_list[0].split()
    # print(names)

    networks = []
    for line in cmd_result_list[1:]:
        if line.split()[0] != "*":
            newLine = ["False"] + line.split()
        else:
            newLine = ["True"] + line.split()[1:]
        # pp(newLine)

        if newLine.index("Infra") != 3:
            ssid = " ".join(newLine[2 : newLine.index("Infra")])
            newLine[2] = ssid
            del newLine[3 : newLine.index("Infra")]
        # pp(newLine)

        rate = " ".join(newLine[5:7])
        newLine[5] = rate
        del newLine[6]
        # pp(newLine)

        if len(newLine) > 9:
            security = " ".join(newLine[8:])
            newLine[8] = security
            del newLine[9:]
        # pp(newLine)
        networks.append(dict(zip(names, newLine)))

    # print(networks)
    # with open('networks.json', 'w') as f:
    #    json.dump(networks, f)

    # pp(networks)
    return networks


# This function will detect the best available network
def detect_best_network():
    signal = 0
    ssid = ""
    cmd = "nmcli device wifi"

    networks = get_networks(tools.read_data_from_shell(cmd)[0])

    for network in networks:
        s = int(network["SIGNAL"])
        if s > signal:
            signal = s
            ssid = network["SSID"]

    return ssid


# This function will connect to a network with given SSID
def connect_network(ssid):
    ssid_cmd = "\ ".join(ssid.split())
    cmd = "nmcli device wifi connect " + ssid_cmd

    result = tools.read_data_from_shell(cmd)

    if result[0] == "":
        cmd = "notify-send 'error while connecting'"
        subprocess.Popen(cmd, shell=True)
    else:
        cmd = "notify-send 'connected to " + ssid + "'"
        subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    # out,err=tools.read_data_from_shell("nmcli device wifi")
    # get_networks(out)

    # print(detect_best_network())
    connect_network(detect_best_network())
