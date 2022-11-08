from flask import Flask, render_template

import json
from linux_autoconnect import get_networks, connect_network, detect_best_network
import linux_common_tools as tools

from linux_wifi_stats import wifi_statistics


app = Flask(__name__)


@app.route("/")
def network():
    return render_template("index.html")


@app.route("/networks")
def get_json():
    nets = get_networks(tools.read_data_from_shell("nmcli device wifi")[0])
    return json.dumps(nets)


@app.route("/connect")
def connect_best_network():
    connect_network(detect_best_network())


@app.route("/stats")
def show_stats():
    wifi_statistics()
