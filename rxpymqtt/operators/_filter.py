from reactivex import compose
import reactivex.operators as rxo
from typing import Callable
from paho.mqtt.client import MQTTMessage


def _filterTopic(topic: str) -> Callable[[MQTTMessage], bool]:
    def _filter(msg: MQTTMessage) -> bool:
        return msg.topic == topic

    return _filter


def filter_(topic: str):
    return compose(rxo.filter(_filterTopic(topic)))
