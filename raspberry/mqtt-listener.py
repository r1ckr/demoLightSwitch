import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

host="test.mosquitto.org"
port=1883
topic="/r1ckr/led"

# Setting up the pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if str(msg.payload).lower() == 'on':
        print("Turning LED on")
        GPIO.output(18,GPIO.HIGH)

    if str(msg.payload).lower() == 'off':
        print("Turning LED off")
        GPIO.output(18,GPIO.LOW)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()