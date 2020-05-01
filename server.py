import json
import datetime
from flask import Flask, render_template
from flask_frozen import Freezer
app = Flask(__name__)
freezer = Freezer(app)

BC_TAGS = ['britishcolumbia', 'vancouver', 'victoria']
PRARIE_TAGS = ['alberta', 'edmonton', 'calgary', 'saskatchewan', 'manitoba']
ONTARIO_TAGS = ['toronto', 'ottawa', 'ontario']
QUEBEC_TAGS = ['montreal', 'quebec']
ATLANTIC_TAGS = ['newfoundland', 'novascotia', 'newbrunswick', 'pei']


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
    with open('scripts/results/canada.json') as f:
        rs = json.load(f)
        results_tor = [d for d in rs if d.get('region') == 'toronto']
        results_mon = [d for d in rs if d.get('region') == 'montreal']
        results_wes = [d for d in rs if d.get('region') in BC_TAGS]
        results_pra = [d for d in rs if d.get('region') in PRARIE_TAGS]
        results_ont = [d for d in rs if d.get('region') in ONTARIO_TAGS]
        results_que = [d for d in rs if d.get('region') in QUEBEC_TAGS]
        results_atl = [d for d in rs if d.get('region') in ATLANTIC_TAGS]
    date_str = datetime.date.today().strftime('%m-%d-%Y')

    return render_template('canada_t.html', date_str=date_str,
        results_tor=results_tor, results_mon=results_mon,
        results_wes=results_wes, results_atl=results_atl,
        results_pra=results_pra, results_ont=results_ont,
        results_que=results_que)


if __name__ == "__main__":
    freezer.freeze()
    app.run(host='0.0.0.0', port=5000)

# export FLASK_APP=server.py
# flask run --host=0.0.0.0
