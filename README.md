# RxPyMqtt

Wrapped paho.mqtt.Client reactivex Subject

## Usage

```python

import paho.mqtt.Client as mqtt
import reactivex.operators as rxo
import rxpymqtt as rxmq

# Create default paho.mqtt client
client: mqtt.Client = mqtt.Client()

rxClient = rxmq.Subject(client)

# Create credentials object if you need to authenticate that client
authData = rxmq.ConnectionCredentials(
  username='broker_username',
  password='password'
)
# Required broker connection options
options = rxmq.ConnectionOptions(
  host='localhost',
  port=31883, # specify custom port if needed. by default it has value of 1883
  credentials=authData # optional authentication data
)


rxClient.connect(options) # wil set authentication data to that client
                          # and call asyncronous connection

rxClient.withTopic('test', 0).subscribe(
  lambda msg: print(msg.payload.decode('utf-8'))
) # subscribe to specific topic

rxClient.subscribe(
  lambda msg: print(msg.payload.decode('utf-8'))
) # subscribe to all received messages


# Subscribe to topics when broker connection successfully established
rxClient.connected.pipe(
  rxo.map(lambda _: client.subscibe('another topic')) # you can still use default client to subscribe
) 

rxClient.disconnected.subscribe(
  lambda _: print('Broker connection established')
)

rxClient.disconnected.subscribe(
  lambda _: print('Broker connection lost')
)


# Start infinite blocking loop
rxClient.loop_forever()

```

# Examples

## Broker dependant

Make sure to run next command from project root before any example execution

```sh
docker compose -f ./examples/docker/docker-compose.yml up
```

or if you do not want to watch for broker logs
```sh
docker compose -f ./examples/docker/docker-compose.yml up -d
```

- `connection` Demonstrates how to determine whether client has connected to specified broker




