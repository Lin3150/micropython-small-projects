# 在这里写上你的代码 :-)
import network
import socket
import time
import time
from machine import UART
from umqtt.robust import MQTTClient, Pin
import sys
import os

def connect_network():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network')
        wlan.connect('your-ssid', 'your-password')
        while not wlan.isconnected():
            pass
    print('network config',wlan.ifconfig())
    print('connected')


#MQTT part
# information config
adafruit_url = b'io.adafruit.com'
your_username = b'lin3150'
your_apikey = b'aio_TEcc35OXCVXbUFMMt92VfNXDv0n9'
your_feed1 = b'open'
your_feed2 = b'close'
whole_feed1 = bytes('{:s}/feeds/{:s}'.format(your_username, your_feed1), 'utf-8')
whole_feed2 = bytes('{:s}/feeds/{:s}'.format(your_username, your_feed1), 'utf-8')
# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
client = MQTTClient(client_id=mqtt_client_id,
                    server=adafruit_url,
                    user=your_username,
                    password=your_apikey,
                    ssl=False)


#uart

uart = UART(0, 9600)
uart.init(9600, bits=8, stop=1)
open_data = 'A1 F1 1C 2F 33'
close_data = 'A1 F1 2D 1B 21'

#led

pin2 = Pin(2, Pin.OUT)
pin2.value(1)


def callback_action(feed, msg):
    print('Received Data:  feed = {}, Msg = {}'.format(feed, msg))
    if your_feed1 in feed:
        action = str(msg, 'utf-8')
        if action == 'ON':
            uart.write(open_data)
        else:
            uart.write(close_data)
        print('uart done')
    if your_feed2 in feed :
        action = str(msg, 'utf-8')
        if action == 'ON':
            pin2.value(0)
        else:
            pin2.value(1)
        print('led done')


def main():
    connect_network()
    client.set_callback(callback_action)
    client.subscribe(mqtt_feedname1)
    client.subscribe(mqtt_feedname2)
    while True:
        try:
            client.wait_msg()
        except KeyboardInterrupt:
            print('exit')
            client.disconnect()
            sys.exit()

if __name__ == '__main__':
    main()
