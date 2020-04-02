#!/usr/bin/python3
import time
from flask import Flask
import redis

app = Flask(__name__)
R = redis.Redis()

@app.route('/enable')
def enable_led_psu():
    R.set('power_supply', b'1')
    return 'Enabled'

@app.route('/disable')
def disable_led_psu():
    R.set('power_supply', b'0')
    return 'Disabled'


@app.route('/toggle')
def toggle_led_psu():
    if R.get('power_supply').startswith(b'0'):
        return enable_led_psu()
    else:
        return disable_led_psu()

if __name__=='__main__':
    app.run('0.0.0.0')
