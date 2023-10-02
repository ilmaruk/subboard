import paho.mqtt.client as paho
from paho import mqtt

import certifi


def connect(client_id: str, host: str, port: int, username: str, password: str) -> paho.Client:
    client = paho.Client(client_id=client_id,
                         userdata=None, protocol=paho.MQTTv5)

    client.tls_set(ca_certs=certifi.where(),
                   tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(username, password)
    client.connect(host, port)

    return client
