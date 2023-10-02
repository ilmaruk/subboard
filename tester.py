# A generator of events to test the subscriber
import json
import os
import time

import certifi
from dotenv import load_dotenv
import paho.mqtt.client as paho

from subboard.events import EventType
from subboard.mqtt import connect


def test(client: paho.Client, topic: str) -> None:
    client.loop_start()

    print("KICK_OFF")
    payload = json.dumps({"type": EventType.KICK_OFF, "duration": 30})
    client.publish(topic, payload, qos=1)
    time.sleep(2.5)

    # print("HOME GOAL")
    # payload = json.dumps({"type": EventType.SCORE, "who": "home"})
    # client.publish(topic, payload, qos=1)
    # time.sleep(2.5)

    # print("AWAY GOAL")
    # payload = json.dumps({"type": EventType.SCORE, "who": "away"})
    # client.publish(topic, payload, qos=1)
    # time.sleep(2.5)

    # print("PAUSE")
    # payload = json.dumps({"type": EventType.PAUSE})
    # client.publish(topic, payload, qos=1)
    # time.sleep(2.5)

    # print("RESUME")
    # payload = json.dumps({"type": EventType.RESUME})
    # client.publish(topic, payload, qos=1)
    # time.sleep(2.5)

    client.loop_stop()


if __name__ == "__main__":
    load_dotenv()

    client = connect("pytester", os.getenv("MQTT_HOST"), int(os.getenv(
        "MQTT_PORT")), os.getenv("MQTT_USERNAME_TESTER"), os.getenv("MQTT_PASSWORD_TESTER"))

    test(client, "subboard/test")

    client.disconnect()
