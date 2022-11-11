from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

from threading import Lock

import sys

sys.path.insert(0, "./modules")

from linux_autoconnect import get_networks, connect_network, detect_best_network
import linux_common_tools as tools
from linux_wifi_stats import wifi_statistics


# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__)
socketio = SocketIO(app)

thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(3)
        
        cmd = "nmcli device wifi"
        networks = get_networks(tools.read_data_from_shell(cmd)[0])
        
        socketio.emit("connection",networks)


# Handler for default flask route
# Using jinja template to render html along with slider value as input
@app.route("/")
def index():
    return render_template("front.html")


# Handler for a message recieved over 'connect' channel
@socketio.on("connect")
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


# Notice how socketio.run takes care of app instantiation as well.
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
