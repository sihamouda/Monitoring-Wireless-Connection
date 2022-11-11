from flask import Flask, render_template
from flask_socketio import SocketIO,send, emit


from linux_autoconnect import get_networks, connect_network, detect_best_network
import linux_common_tools as tools
from linux_wifi_stats import wifi_statistics

# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__)
socketio = SocketIO(app)


# Handler for default flask route
# Using jinja template to render html along with slider value as input
@app.route('/')
def index():
    return render_template('front.html')


# Handler for a message recieved over 'connect' channel
@socketio.on('connect')
def test_connect():
    emit('connection',  {'status':'connected'})


# @socketio.on('json')
# def handle_json(json):
#     send(json, json=True)




# Notice how socketio.run takes care of app instantiation as well.
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')


# @app.route("/")
# def network():
#     return render_template("front.html")

# @app.route("/socket")
# def socket():
#     async def handler(websocket):
#         while True:
#             cmd = "nmcli device wifi"
#             networks = get_networks(tools.read_data_from_shell(cmd)[0])
#             await websocket.send(json.dumps(networks))
#             await asyncio.sleep(random.random() * 2 + 1)
#             # print(f"{networks}")

#     async def main():
#         async with websockets.serve(handler,"localhost",8080):
#             await asyncio.Future()

#     asyncio.run(main())
