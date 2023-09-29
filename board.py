import json
import queue
import socket
import threading
import time

import certifi

import paho.mqtt.client as paho
from paho import mqtt


def mqtt_subscriber(client: paho.Client, events: queue.Queue) -> None:
    """This thread receives messages from the MQTT broker
    and puts the relevant events onto the events queue.
    """
    def on_message(client, userdata, message: paho.MQTTMessage) -> None:
        print("got message", message)
        event = json.loads(message.payload.decode())
        events.put(event)

    client.on_message = on_message

    while True:
        client.loop()
        time.sleep(.1)


def board_manager(events: queue.Queue) -> None:
    """This thread takes events from the events queue and changes
    the board display accordingly.
    """
    while True:
        try:
            event = events.get_nowait()
        except queue.Empty:
            # No message currently available
            pass
        else:
            print("processing event", event)
            if event["type"] == "ft":
                # Final time
                return

        time.sleep(.1)


if __name__ == "__main__":
    client = paho.Client(client_id=socket.gethostname(), userdata=None,
                         protocol=paho.MQTTv5)

    client.tls_set(ca_certs=certifi.where(),
                   tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("pizero", "E4Gq@pz8PwfdJYN")
    client.connect("cf63c06cf56d42f391e1bfc520cda10b.s2.eu.hivemq.cloud", 8883)

    client.subscribe("subboard/#", qos=1)

    events = queue.Queue()

    mqtt_subs_thread = threading.Thread(target=mqtt_subscriber,
                                        args=(client, events), daemon=True)
    mqtt_subs_thread.start()

    board_manager_thread = threading.Thread(
        target=board_manager, args=(events,), daemon=True)
    board_manager_thread.start()

    board_manager_thread.join()
