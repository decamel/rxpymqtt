import paho.mqtt.client as mqtt
import rxpymqtt as rxmqtt


# Define Broker connection credentials
    # and broker network address
host='localhost'
port=41883

connectionOptions = rxmqtt.ConnectionOptions(host, port)

client = mqtt.Client('client_id')

rxclient = rxmqtt.Subject(client);

rxclient.connect(connectionOptions)

rxclient.connected.subscribe(
  lambda _: print('Connected')
)

rxclient.loop_forever()

