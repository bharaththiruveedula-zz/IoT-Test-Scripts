from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("localgateway_to_awsiot")

def on_publish(client, userdata, mid):
 print "Message Published to AWS"

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "localgateway_to_awsiot":
        print(msg.topic+" "+str(msg.payload))
        awsMQTTClient = AWSIoTMQTTClient("bridgeiot1")
        awsMQTTClient.configureEndpoint("<AWS-ENDPOINT>", 8883)
        awsMQTTClient.configureCredentials("/etc/mosquitto/certs/rootCA.pem", "/etc/mosquitto/certs/private.key", "/etc/mosquitto/certs/cert.crt")
        awsMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        awsMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        awsMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        awsMQTTClient.configureMQTTOperationTimeout(5)
        awsMQTTClient.connect()
        awsMQTTClient.publish("localgateway_to_awsiot", str(msg.payload), 0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("<YOUR-6LBR-ROUTER>", 1883, 60)

client.loop_forever()
