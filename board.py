from datetime import datetime
import os
import queue
import socket
import threading
import time

import certifi
from dotenv import load_dotenv
import paho.mqtt.client as paho
from paho import mqtt

import subboard
from subboard.events import event_factory, EventType, Event


def mqtt_subscriber(client: paho.Client, events: queue.Queue) -> None:
    """This thread receives messages from the MQTT broker
    and puts the relevant events onto the events queue.
    """
    def on_message(client, userdata, message: paho.MQTTMessage) -> None:
        print("got message", message)
        event = event_factory(message.payload.decode())
        events.put(event)

    client.on_message = on_message

    while True:
        client.loop()
        time.sleep(.1)


def board_manager(events: queue.Queue) -> None:
    """This thread takes events from the events queue and changes
    the board display accordingly.
    """
    match = subboard.Match()
    display = subboard.TerminalDisplay()

    while True:
        try:
            event = events.get_nowait()  # type: Event
        except queue.Empty:
            # No message currently available
            if match.status == "scheduled":
                print(datetime.now())
            elif match.status == "started":
                remaining = match.clock.value()
                if remaining <= 0:
                    # The match is over
                    return
                display.update(match)
        else:
            print("processing event", event)
            if event.type == EventType.KICK_OFF:
                # Kick-off
                match.start(event.duration)
            elif event.type == EventType.SCORE:
                match.goal(event.who)

        time.sleep(.1)


if __name__ == "__main__":
    load_dotenv()

    client = paho.Client(client_id=socket.gethostname(), userdata=None,
                         protocol=paho.MQTTv5)

    client.tls_set(ca_certs=certifi.where(),
                   tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(os.getenv("MQTT_USERNAME"),
                           os.getenv("MQTT_PASSWORD"))
    client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))

    client.subscribe("subboard/#", qos=1)

    events = queue.Queue()

    mqtt_subs_thread = threading.Thread(target=mqtt_subscriber,
                                        args=(client, events), daemon=True)
    mqtt_subs_thread.start()

    board_manager_thread = threading.Thread(
        target=board_manager, args=(events,), daemon=True)
    board_manager_thread.start()

    board_manager_thread.join()
