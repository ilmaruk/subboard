from datetime import datetime
import os
import queue
import socket
import threading
import time

from dotenv import load_dotenv
import paho.mqtt.client as paho

import subboard
from subboard.mqtt import connect
from subboard.events import event_factory, Event
from subboard.states import States


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
    clock = subboard.DescendingClock()
    match = subboard.Match(clock)
    state = subboard.BeforeMatchState(match)

    display = subboard.TerminalDisplay()

    while True:
        try:
            event = events.get_nowait()  # type: Event
        except queue.Empty:
            # No message currently available
            pass
        else:
            print("processing event", event)
            state = state.process_event(event)

        if state.type == States.BEFORE_MATCH:
            display.set(datetime.now().strftime("%H:%M:%S"))
        elif state.type == States.AFTER_MATCH:
            display.set("FT")
        elif state.type == States.DURING_MATCH:
            remaining = match.clock.current()
            if remaining <= 0:
                # The match is over
                events.put(Event('{"type":"stop"}'))

            display.update(match)

        time.sleep(.1)


if __name__ == "__main__":
    load_dotenv()

    client = connect(socket.gethostname(), os.getenv("MQTT_HOST"), int(os.getenv(
        "MQTT_PORT")), os.getenv("MQTT_USERNAME_PIZERO"), os.getenv("MQTT_PASSWORD_PIZERO"))
    client.subscribe("subboard/#", qos=1)

    events = queue.Queue()

    mqtt_subs_thread = threading.Thread(target=mqtt_subscriber,
                                        args=(client, events), daemon=True)
    mqtt_subs_thread.start()

    board_manager_thread = threading.Thread(
        target=board_manager, args=(events,), daemon=True)
    board_manager_thread.start()

    board_manager_thread.join()
