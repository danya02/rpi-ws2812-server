import redis
import serial
R = redis.Redis()
R.config_set("notify-keyspace-events", "KEA")

P = R.pubsub()
P.psubscribe('*')

LED_COUNT = 550

PIPE = serial.Serial('/dev/ttyUSB1', 500000, timeout=10)

def write_colors(colors):
    buf = bytearray(b'Ada')
    hi, lo = divmod(len(colors)-1, 256)
    buf.append(hi)
    buf.append(lo)
    buf.append(hi ^ lo ^ 0x55)
    print(buf)
    for color in colors:
        for shade in color:
            buf.append(shade)
    print(buf)
    PIPE.write(buf)
    PIPE.flush()

for event in P.listen():
    print(event)
    if event['channel'].endswith(b'set'):
        if event['data'] == b'power_supply':
            psu = R.get('power_supply')
            if psu.startswith(b'1'):
                print('Turn on PSU')
                write_colors([(255,0,0), (0, 255, 0), (0, 0, 255)]*int(LED_COUNT/3))
            else:
                print('Turn off PSU')
                write_colors([(0,0,0)])

