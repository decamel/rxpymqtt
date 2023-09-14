from typing import Callable
from reactivex import Observable
import paho.mqtt.client as mqtt


def filter(
    topic: str,
) -> Callable[[Observable[mqtt.MQTTMessage]], Observable[mqtt.MQTTMessage]]:
    """Determines whether MQTTMessage satisfies
    specified topic

    Example:
      >>> op = filter('topic')

    Args:
      topic: Topic which should be satisfied by mqtt message

    Returns:
      An operator function that takes an observable source of
      mqtt messages and return only those that satisfies
      specified topic

    """
    from ._filter import filter_

    return filter_(topic)
