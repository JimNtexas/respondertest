#responder
import sys, os
import random
import time
from paho.mqtt import client as mqtt_client


#  broker = 'broker.emqx.io'
broker = 'test.mosquitto.org'
port = 1883
topic = "/python/responder"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'JimNtexas'
password = 'UseAhash'

def handler(signum, frame):
    sys.exit(0)

def on_disconnect(client, userdata,rc):
    print("Broker disconnect!")
    print(userdata)
    sys.exit()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            m = "Connected flags" + str(flags) + "result code " + str(rc) + "client1_id  " + str(client)
            print(m)

        else:
            print("Failed to connect, return code %d\n", rc)
            sys.exit()

    CLEAN_SESSION = True
    client = mqtt_client.Client(client_id, clean_session=CLEAN_SESSION)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to broker")

        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:

        print("Connection failed")


def on_message(client, userdata, message):
    print("Message received: " + str(message.payload))

def on_subscribe(client, userdata, mid, granted_qos):
        print('subscribed')


def publish(client):
    msg_count = 0
    while True:
        try:

            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1

        except:
            break


def run():
    client = connect_mqtt()
    client.loop_start()


    while True:
        try:
            time.sleep(1)
            client.subscribe(topic)
            client.message_callback_add(topic, on_message )
        except:
            print('\ndisconnecting\n')
            client.disconnect()
            break

def print_hi():

    print("Responder running Python")
    print(sys.version)
    print("Version info.")
    print(sys.version_info)


if __name__ == '__main__':
    print_hi()
    run()
