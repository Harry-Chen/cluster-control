from flask import Flask, jsonify, request

import os
import sys

app = Flask(__name__)
app.debug = True

state = {}


def run(command):
    app.logger.info('Running command: ' + command)
    os.system(command)


def set_fan(value=None, exec_pref=''):
    script = '/home/harry/scripts/localfan'
    if value is None or value == 0:
        value = ''

    state['fanLevel'] = 0 if value == '' else value

    run(exec_pref + '{} {}'.format(script, value))


def set_cpu_power(value=None, exec_pref=''):
    script = '/home/sc/baobao/baobaoctl.sh'
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
def get_state():
    return jsonify(state)


@app.route('/', methods=['POST'])
def set_state():
    prefix = app.config.get('prefix')
    r = request.get_json()

    app.logger.info('Got new request: ' + str(r))

    if r['fanLevel'] != state['fanLevel']:
        set_fan(r['fanLevel'], prefix)

    if r['cpuPowerAvg'] != state['cpuPowerAvg'] or r['cpuPowerMax'] != state['cpuPowerMax']:
        set_cpu_power((r['cpuPowerAvg'], r['cpuPowerMax']), prefix)

    if r['gpuPower'] != state['gpuPower']:
        set_gpu_power(r['gpuPower'], prefix)

    if r['gpuFrequency'] != state['gpuFrequency']:
        set_gpu_freq(r['gpuFrequency'], prefix)

    return jsonify(state)


@app.route('/', methods=['DELETE'])
def reset_state():
    clean_ass()
    return jsonify(state)


def clean_ass():
    app.logger.info('Cleaning ass...')
    prefix = app.config.get('prefix')
    set_fan(None, prefix)
    set_cpu_power(None, prefix)
    set_gpu_freq(None, prefix)
    set_gpu_power(None, prefix)
    app.logger.info('Ass cleaned!')


if __name__ == '__main__':
    # get host name
    if len(sys.argv) != 2:
        print('Need hostname to run!')
        exit(1)

    # set prefix then clean ass
    app.config['prefix'] = 'sudo clush -w {} '.format(sys.argv[1])
    clean_ass()

    app.run(use_reloader=False)
