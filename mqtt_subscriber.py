#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import paho.mqtt.client as paho
from paho import mqtt
import os
import argparse

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    
# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print("topic: " + msg.topic + " qos: " + str(msg.qos) + " payload: " + str(msg.payload))

def prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="specify the topic name")
    return parser.parse_args()

def main():
    user_input = prepare_args()

    topic = user_input.topic

    # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    client = paho.Client(client_id="box_1", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    
    # set username and password
    mqtt_passwd = os.environ["HIVEMQ_PASSWORD"]
    client.username_pw_set("IoT_2022_drug_dealer", mqtt_passwd)
    
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect("4e2bde16ffff46d9a8f341015b213f81.s2.eu.hivemq.cloud", 8883)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.subscribe(topic, qos=1)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.unsubscribe(topic)
        client.disconnect()


if __name__ == '__main__':
    main()

