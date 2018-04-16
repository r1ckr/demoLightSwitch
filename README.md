# Light Switch Demo
This is a demo to control a light in a Raspberry Pi using Alexa, MQTT and Lambda functions in AWS

Installation:
## Raspberry Pi

Get a Raspberry Pi and connect to it a LED in the pin 18, then clone this project from `/home/pi/`.
After that copy the systemd service into the right folder:
```bash
cd /home/pi
sudo cp demoLightSwitch/raspberry/mqtt-listener.service
sudo systemctl enable mqtt-listener.service
sudo systemctl start mqtt-listener.service
```

To test that it works you can send a message to the topic from another console:
```bash
# Turn it on
mosquitto_pub -h test.mosquitto.org -p 1883 -t "/r1ckr/led" -m "on"

# Turn it off
mosquitto_pub -h test.mosquitto.org -p 1883 -t "/r1ckr/led" -m "off"
```
That should turn on or off the LED

## Amazon Alexa
Go to developer.amazon.com and create a new skill, then in the JSON editor paste the content of the [definition.json](aws-alexa/definition.json) file.

After this is done, build the skill, then go to the **Endpoint** section and leave it there for further config after the next step.

## AWS Lambda
Now go to AWS Lambda and create a new function with a `lambda_basic_execution` role, choose to create it from scratch and later upload the contents of the aws-lambda folder as a zip file. As a result you should have the index.js file in the root folder of your lambda.

## Connecting AWS Lambda and Alexa
In AWS Lambda create an Alexa Skills Kit *trigger*, paste the Alexa **Skill ID** from the previously create skill.

Now copy the **ARN** from the AWS Lambda and paste it in the **Endpoint** section of the Alexa skill.


## Test it
Go to the test section of Alexa and say:
- Open light switch
- Turn the light on
- Turn the light off