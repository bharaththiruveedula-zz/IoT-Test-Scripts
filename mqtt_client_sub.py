from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import paho.mqtt.client as mqtt
import ssl
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

def on_message(client, userdata, msg):
    if msg.topic == "localgateway_to_awsiot":
        print(msg.topic+" "+str(msg.payload))
        client = mqtt.Client()
        client.connect("<6LBR-ROUTER_ADDR>", 1883, 60)
        client.publish("awsiot_to_localgateway", msg.payload)


mqttc = mqtt.Client(client_id="mqtt-test")
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set("/etc/mosquitto/certs/rootCA.pem",
                certfile="/etc/mosquitto/certs/cert.crt",
                keyfile="/etc/mosquitto/certs/private.key",
              tls_version=2,
              ciphers=None)

mqttc.connect("<AWS_ENDPOINT>", port=8883) #AWS IoT service hostname and portno
mqttc.subscribe("localgateway_to_awsiot", qos=1) #The names of these topics start with $aws/things/thingName/shadow."
mqttc.loop_forever()
