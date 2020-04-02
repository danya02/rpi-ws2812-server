import redis
import serial
R = redis.Redis()
R.config_set("notify-keyspace-events", "KEA")

P = R.pubsub()
P.psubscribe('*')

PIPE = serial.Serial('/dev/ttyUSB0', 250000, timeout=10)

for event in P.listen():
    print(event)
    if event['channel'].endswith(b'set'):
        if event['data'] == b'power_supply':
            psu = R.get('power_supply')
            if psu.startswith(b'1'):
                print('Turn on PSU')
                PIPE.write(b'P')
            else:
                print('Turn off PSU')
                PIPE.write(b'p')
            PIPE.flush()

