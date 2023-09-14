import paho.mqtt.client as mqtt
import reactivex as rx
import reactivex.operators as rxo
from ..operators import filter

from typing import Tuple, TypeAlias, Any, Optional
from typing_extensions import Self

Payload: TypeAlias = str | bytes | bytearray | float
UserData = Any

TOnConnect: TypeAlias = Tuple[
    mqtt.Client,
    UserData,
    dict[str, int],
    int | mqtt.ReasonCodes | None,
    mqtt.Properties | None,
]

TOnDisconnect: TypeAlias = Tuple[
    mqtt.Client,
    UserData,
    int | mqtt.ReasonCodes | None,
    mqtt.Properties | None,
]


class ConnectionCredentials:
    _username: str
    _password: str

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        pass

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self):
        return self._password

    def withUsername(self, username: str) -> Self:
        self._username = username
        return self

    def withPassword(self, password: str) -> Self:
        self._password = password
        return self

    def __bool__(self) -> bool:
        return bool(len(self._username)) and bool(len(self._password))

    def __repr__(self) -> str:
        return f"ConnectionCredentials({self.username}:{self.password})"


class ConnectionOptions:
    """Broker connection options
    Args:
      host - broker host address
      port - broker network port. defaults to 1883
    """

    _host: str
    _port: int

    _credentials: Optional[ConnectionCredentials]

    def __init__(
        self,
        host: str,
        port: int = 1883,
        credentials: Optional[ConnectionCredentials] = None,
    ) -> None:
        if len(host) == 0:
            raise ValueError("Host path can not be empty")
        self._host = host
        self._port = port
        self._credentials = credentials

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def credentials(self) -> Optional[ConnectionCredentials]:
        return self._credentials

    def __repr__(self) -> str:
        return f"ConnectionOptions({self.host}:{self.port})"


class Subject(rx.Subject[mqtt.MQTTMessage]):
    _client: mqtt.Client
    """MQTT client instance"""

    _connectedSubject: rx.Subject[TOnConnect]
    """Stream of connection events of mqtt client"""

    _disconnectedSubject: rx.Subject
    """Stream of disconnection events of mqtt client"""

    def __init__(self, client: mqtt.Client) -> None:
        super().__init__()
        self._client = client
        self._connectedSubject = rx.Subject()
        self._disconnectedSubject = rx.Subject()
        self._client.on_connect = self._onConnect()
        self._client.on_disconnect = self._onDisconnect()
        self._client.on_message = self._onMessage()

    def dispose(self) -> None:
        self._connectedSubject.dispose()
        self._disconnectedSubject.dispose()
        return super().dispose()

    def _onMessage(self):
        def _on_message(
            client: mqtt.Client, userdata: UserData, message: mqtt.MQTTMessage
        ):
            self.on_next(message)

        return _on_message

    def _onConnect(self):
        """Returns mqtt client connect event handler"""

        def _on_connect(
            client: mqtt.Client,
            userdata: UserData,
            flags: dict[str, int],
            rc: int | mqtt.ReasonCodes | None,
            properties: mqtt.Properties | None,
        ):
            """Emits arguments received from mqtt client on_connect callback
            into connectedSubject"""
            self._connectedSubject.on_next((client, userdata, flags, rc, properties))

        return _on_connect

    def _onDisconnect(self):
        """Returns mqtt client disconnect event handler"""

        def _on_disconnect(
            client: mqtt.Client,
            userdata: UserData,
            rc: int | mqtt.ReasonCodes | None,
            properties: mqtt.Properties | None,
        ):
            """Emits arguments received from mqtt client on_disconnect callback
            into disconnectedSubject"""
            self._disconnectedSubject.on_next((client, userdata, rc, properties))
            pass

        return _on_disconnect

    def connect(self, options: ConnectionOptions):
        """Establishes connection with remote mqtt broker
        This is non-blocking async operation
        """
        if bool(options.credentials):
            self._client.username_pw_set(
                options.credentials.username, options.credentials.password
            )
        self._client.connect_async(host=options.host, port=options.port)

    def loop_forever(self):
        """Starts infinite blocking loop"""
        self.loop_forever()

    def loop_start(self):
        """Starts non-blocking infinite loop"""
        self.loop_start()

    # ---------------------------------------------------------------------------- #

    @property
    def connected(self) -> rx.Observable[TOnConnect]:
        """Returns Observable which contains connect events of MQTT client"""
        return self._connectedSubject

    @property
    def disconnected(self) -> rx.Observable[TOnDisconnect]:
        """Returns Observable which contains disconect events of MQTT client"""
        return self._disconnectedSubject

    def withTopic(self, topic: str, qos: int = 1) -> rx.Observable[mqtt.MQTTMessage]:
        """Observable with MQTTMessages filtered by specified topic

        Returns Observable which contains MQTTMessage for specified topic
        Client will subscibe to that topic automatically

        Can be called before connection established

        """
        return self.connected.pipe(
            rxo.map(lambda _: self._client.subscribe(topic, qos)),
            rxo.map(lambda _: self.pipe(filter(topic))),
            rxo.switch_latest(),
        )

    def next(self, topic: str, msg: Payload | None, qos: int = 0) -> Self:
        """Publishes"""
        self._client.publish(topic, msg, qos)
        return self
