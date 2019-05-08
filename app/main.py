from flask import Flask
import json
import psutil

app = Flask(__name__)

@app.route('/version')
def version():

    return "v0.1.0"


@app.route('/cpu')
def cpu():
    cpu = psutil.cpu_times()

    return json.dumps(cpu._asdict())


@app.route('/mem')
def mem():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return json.dumps({
                "virtual" : mem._asdict(),
                "swap" : swap._asdict()
                })


@app.route('/process')
def process():
    proc = ([{"pid" : p.pid, "username" : p.info['username'], "name" : p.info['name'], "cpu" : sum(p.info['cpu_times'])} 
            for p in sorted(psutil.process_iter(attrs=['name', 'cpu_times', 'username']), 
            key=lambda p: sum(p.info['cpu_times'][:2]))][-3:])

    return json.dumps(proc)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)