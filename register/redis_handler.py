from .dispatcher import (
    ServiceDispatcher,
)
import json
from datetime import (
    datetime,
    timezone
)


def get_seconds_from_epoch_time(epoch):
    expiration_time = datetime.fromtimestamp(epoch, timezone.utc)
    return int((expiration_time - datetime.now(timezone.utc)).total_seconds())


def get_client_instance(access_token):
    client_instance = ServiceDispatcher.get_services('redis-runtime').get(str(access_token))
    if client_instance:
        try:
            return json.loads(client_instance)
        except:
            return None
    else:
        # TODO Raise an error if the client is not found
        return None


def add_client_instance(access_token, client_instance):
    ServiceDispatcher.get_services('redis-runtime').set(str(access_token),
                                                        json.dumps(client_instance),
                                                        ex=get_seconds_from_epoch_time(client_instance['exp'])
                                                        )
    return True
