from flask import Flask, render_template, jsonify
from telemetry_engine import get_somatic_stats # Import our new engine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# NEW: The Telemetry Endpoint
@app.route('/stats')
def stats():
    data = get_somatic_stats()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)