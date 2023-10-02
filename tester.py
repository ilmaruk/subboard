# A generator of events to test the subscriber
import json
import os
import time

import certifi
from dotenv import load_dotenv
import paho.mqtt.client as paho
from paho import mqtt

from subboard.events import EventType


def test(client: paho.Client, topic: str) -> None:
    client.loop_start()

    payload = json.dumps({"type": EventType.KICK_OFF, "duration": 300})
    client.publish(topic, payload, qos=1)
    time.sleep(2.5)

    payload = json.dumps({"type": EventType.SCORE, "who": "home"})
    client.publish(topic, payload, qos=1)
    time.sleep(2.5)

    payload = json.dumps({"type": EventType.SCORE, "who": "away"})
    client.publish(topic, payload, qos=1)
    time.sleep(2.5)

    payload = json.dumps({"type": EventType.PAUSE})
    client.publish(topic, payload, qos=1)
    time.sleep(2.5)

    payload = json.dumps({"type": EventType.RESUME})
    client.publish(topic, payload, qos=1)
    time.sleep(2.5)

    client.loop_stop()


if __name__ == "__main__":
    load_dotenv()

    client = paho.Client(client_id="pytester",
                         userdata=None, protocol=paho.MQTTv5)

    client.tls_set(ca_certs=certifi.where(),
                   tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(os.getenv("MQTT_USERNAME_TESTER"),
                           os.getenv("MQTT_PASSWORD_TESTER"))
    client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))

    test(client, "subboard/test")

    client.disconnect()
