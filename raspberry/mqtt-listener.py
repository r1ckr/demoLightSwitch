import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import socket

host="test.mosquitto.org"
port=1883
topic="/r1ckr/led"

LED_PIN=18

# Setting up the pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN,GPIO.OUT)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # We let the user know that we've just connected
    blink(10, 'fast')
    
    # we send the local IP address {root-topic}/ip topic, just in case we need to connect back to it
    client.publish(topic+'/ip', get_ip_address())
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if str(msg.payload).lower() == 'on':
        print("Turning LED on")
        GPIO.output(LED_PIN,GPIO.HIGH)

    if str(msg.payload).lower() == 'off':
        print("Turning LED off")
        GPIO.output(LED_PIN,GPIO.LOW)

# Utility to blink the led
def blink(times, speed):
    delay = 0.35
    
    if speed == 'fast':
        delay = 0.05

    for x in xrange(1,times):
        GPIO.output(LED_PIN,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(LED_PIN,GPIO.LOW)
        time.sleep(delay)

# Utility to get the IP address of the interface used to connect to the internet
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()