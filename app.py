from flask import Flask, json, render_template
import mon

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor')
def monitor():
    data = mon.get_system_info()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
