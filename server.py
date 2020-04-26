import json
import datetime
from flask import Flask, render_template
from flask_frozen import Freezer
app = Flask(__name__)
freezer = Freezer(app)


@app.route('/')
def index():
    with open('scripts/results/results_am.json') as f:
        results_am = json.load(f)
    with open('scripts/results/results_pf.json') as f:
        results_pf = json.load(f)
    date_str = datetime.date.today().strftime('%m-%d-%Y')
    return render_template('index_t.html', date_str=date_str,
        results_am=results_am, results_pf=results_pf)


@app.route('/canada.html')
def canada():
    with open('scripts/results/toronto.json') as f:
        results_tor = json.load(f)
    with open('scripts/results/montreal.json') as f:
        results_mon = json.load(f)
    with open('scripts/results/vancouver.json') as f:
        results_van = json.load(f)
    date_str = datetime.date.today().strftime('%m-%d-%Y')
    return render_template('canada_t.html', date_str=date_str,
        results_tor=results_tor, results_mon=results_mon,
        results_van=results_van)


if __name__ == "__main__":
    freezer.freeze()
    app.run(host='0.0.0.0', port=5000)

# export FLASK_APP=server.py
# flask run --host=0.0.0.0
