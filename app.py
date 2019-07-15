from flask import Flask, jsonify, render_template
import mon

app = Flask(__name__)

@app.route('/')
def index():
    response = app.response_class(
        response = "Pi monitor service is running :)",
        status=200,
        mimetype='text/plain'
    )

    return response

@app.route('/monitor')
def monitor():
    data = mon.get_system_info()
    return jsonify(data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
