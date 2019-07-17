from flask import Flask, jsonify, request, render_template
import mon
import net

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    response = app.response_class(
        response = "Pi monitor service is running :)",
        status=200,
        mimetype='text/plain'
    )

    return response

@app.route('/monitor', methods=['GET'])
def monitor():
    data = mon.get_system_info()
    return jsonify(data=data)

@app.route('/network', methods=['GET'])
def network():
    data = net.get_network_info()
    return jsonify(data=data)

@app.route('/functions/<action>', methods=['POST'])
def functions(action):
    if action is "shutdown":
        mon.shutdown()
    elif action is "reboot":
        mon.reboot()

    response = app.response_class(
        response = action + " initiated.",
        status=200,
        mimetype='text/plain'
    )

    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
