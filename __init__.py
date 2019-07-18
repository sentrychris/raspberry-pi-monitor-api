from flask import Flask, jsonify, request, render_template
import system
import network
import wireless

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    response = app.response_class(
        response = "Pi monitor service is running :)",
        status = 200,
        mimetype='text/plain'
    )

    return response

@app.route('/system', methods=['GET'])
def sysres():
    data = system.get_system_info()
    return jsonify(data=data)

@app.route('/network', methods=['GET'])
def sysnet():
    data = network.get_network_info()
    return jsonify(data=data)

@app.route('/network/counter/<interface>', methods=['GET'])
def streamed_sysnet(interface):
    def generate():
        for stat in network.counter(interface):
            yield stat

    return app.response_class(
        response = generate(),
        status = 200,
        mimetype='application/json'
    )

@app.route('/network/wireless', methods=['GET'])
def syswifi():
    data = wireless.get_wifi_info()
    return jsonify(data=data)

@app.route('/action/<action>', methods=['POST'])
def action(action):
    if action is "shutdown":
        system.shutdown()
    elif action is "reboot":
        system.reboot()

    response = app.response_class(
        response = action + " initiated.",
        status=200,
        mimetype='text/plain'
    )

    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
