from flask import Flask, jsonify
from flask import request

import os
import sys

app = Flask(__name__)

state = {}


def run(command):
    app.logger.info('Running command: ' + command)
    os.system(command)


def set_fan(value=None, exec_pref=''):
    script = '/home/sc/scripts/localfan'
    if value is None or value == 0:
        value = ''

    state['fanLevel'] = 0 if value == ' ' else value

    run(exec_pref + '{} {}'.format(script, value))


def set_cpu_power(value=None, exec_pref=''):
    script = '/home/sc/scripts/baobaoctl.sh'
    if value is None:
        value = (205, 255)

    state['cpuPowerAvg'] = value[0]
    state['cpuPowerMax'] = value[1]

    run(exec_pref + '{} {} {}'.format(script, value[0], value[1]))


def set_gpu_freq(value=None, exec_pref=''):
    if value is None:
        value = 1380

    # keep the float number send by js
    state['gpuFrequency'] = value
    # but set it to an integer
    run(exec_pref + 'nvidia-smi -ac 877,{}'.format(int(value)))


def set_gpu_power(value=None, exec_pref=''):
    if value is None:
        value = 250

    state['gpuPower'] = value

    run(exec_pref + 'nvidia-smi -pl {}'.format(value))


@app.route('/', methods=['GET'])
def control():
    return jsonify(state)


@app.route('/', methods=['POST'])
def control():
    prefix = 'sudo clush -w {} '.format(app.config.get('host'))
    r = request.get_json()

    if r['fanLevel'] != state['fanLevel']:
        set_fan(r['fanLevel'], prefix)
    if r['cpuPowerAvg'] != state['cpuPowerAvg'] or r['cpuPowerMax'] != state['cpuPowerMax']:
        set_cpu_power((r['cpuPowerAvg'], r['cpuPowerMax']), prefix)
    if r['gpuPower'] != state['gpuPower']:
        set_gpu_power(r['gpuPower'], prefix)
    if r['gpuFrequency'] != state['gpuFrequency']:
        set_gpu_power(r['gpuFrequency'], prefix)

    return jsonify(state)


def clean_ass(prefix):
    set_fan(None, prefix)
    set_cpu_power(None, prefix)
    set_gpu_freq(None, prefix)
    set_gpu_power(None, prefix)


if __name__ == '__main__':
    # get host name
    if len(sys.argv) != 2:
        exit(1)

    # clean ass before run
    command_prefix = 'sudo clush -w {} '.format(sys.argv[1])
    clean_ass(command_prefix)

    # start flask
    app.config['host'] = command_prefix
    app.run()
