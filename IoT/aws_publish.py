from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

import picture_capture




# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a21xxb3zewrt7o-ats.iot.ap-southeast-2.amazonaws.com"
CLIENT_ID = "langhae-20220521"
PATH_TO_CERT = "/home/pi/workspace/final_project/certs/32edc2cdf4a1e8aa7c497cd174252d6c57e0365ee94b3849961dc79a698c46d9-certificate.pem.crt"
PATH_TO_KEY = "/home/pi/workspace/final_project/certs/32edc2cdf4a1e8aa7c497cd174252d6c57e0365ee94b3849961dc79a698c46d9-private.pem.key"
PATH_TO_ROOT = "/home/pi/workspace/final_project/certs/AmazonRootCA1.pem"
MESSAGE = "Hello World"
TOPIC = "data/langhae-20220521" # 토픽
RANGE = 20

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERT,
            pri_key_filepath=PATH_TO_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_ROOT,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
            
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')
for i in range (RANGE):
    data = picture_capture.capture()
    message = {"message" : data}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")
    t.sleep(0.1)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()