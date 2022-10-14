import linux_common_tools as tools


# To get date and time
import datetime

# To make a graph of the current AP' signal power
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# This function will show us a real time graph of the current AP' signal power in dBm
def wifi_statistics():
    current_time = []
    signal_power = []

    def show_signal_power(i):
        plt.style.use("fivethirtyeight")
        current_time.append(datetime.datetime.now())
        signal_power.append(tools.get_signal_power(tools.read_data_from_shell("iwconfig")[0]))

        # pp(signal_power)
        plt.cla()
        plt.plot(current_time, signal_power)

    animate = FuncAnimation(plt.gcf(), show_signal_power, interval=1000)
    plt.tight_layout()
    plt.show()

wifi_statistics()