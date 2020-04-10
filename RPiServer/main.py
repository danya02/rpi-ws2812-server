#!/usr/bin/python3
import time
from flask import Flask, request, render_template, redirect, url_for, jsonify
import redis
import json
from functools import wraps

app = Flask(__name__)
R = redis.Redis()

def locks_pixels(fun):
    @wraps(fun)
    def wrapped(*args, **kwargs):
        if R.get('pix_lock')!=b'open':
            return jsonify({'status':'locked'}), 429
        R.set('pix_lock', 'locked')
        out = fun(*args, **kwargs)
        R.set('pix_lock', 'open')
        return out
    return wrapped

def redirect_for(what, **params):
    return redirect(url_for(what, **params))

@app.route('/enable')
def enable_led_psu():
    R.set('power_supply', b'1')
    return 'Enabled'

@app.route('/disable')
def disable_led_psu():
    R.set('power_supply', b'0')
    return redirect_for('fill')


@app.route('/toggle')
def toggle_led_psu():
    if R.get('power_supply').startswith(b'0'):
        return enable_led_psu()
    else:
        return disable_led_psu()

def led_count():
    return json.loads(R.get('led_count'))

@app.route('/fill')
def fill():
    return render_template('fill_color.html', color='#000000')

@locks_pixels
@app.route('/color/fill', methods=['PUT'])
def fill_color():
    data = request.json or json.loads(request.data)
    color = data['color']
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5: ], 16)
    for i in range(led_count()):
        R.set(str(i), json.dumps((r, g, b)))
    R.set('commit', 1)
    return jsonify({'status': 'ok'})

if __name__=='__main__':
    app.run('0.0.0.0')
