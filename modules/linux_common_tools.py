# To pass shell commands we use subprocess
import subprocess

# To parse data using regular expressions we use re
import re

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


if __name__ == "__main__":
    output, error = read_data_from_shell("iwconfig")
    # print("out: "+output)
    # print("======")
    # print("err: "+error)
    print(get_signal_power(output))
