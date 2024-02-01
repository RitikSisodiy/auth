import redis
from django.conf import settings
import traceback
from register.logger import (
    log_startup_info
)


class ServiceDispatcher:
    service_instance = {}

    def __init__(self):
        try:
            self.service_instance['redis-runtime'] = redis.Redis(
                host=settings.GEMS_OAUTH_INTROSPECTOR['REDIS_CONFIGURATION']['HOST'],
                port=settings.GEMS_OAUTH_INTROSPECTOR['REDIS_CONFIGURATION']['PORT'],
                db=settings.GEMS_OAUTH_INTROSPECTOR['REDIS_CONFIGURATION']['DB']
            )
            log_startup_info("SERVICE-STARTED",
                             {
                                 "where": "Redis Client for OAuth Authentication Started",
                             })
        except Exception as e:
            log_startup_info("STARTUP-EXCEPTION",
                             {
                                 "where": "Redis Client for OAuth Authentication Started",
                                 "traceback": traceback.format_exception(type(e), e, e.__traceback__)
                             })

    # This method returns the service that has been deployed under the it's respective name for usage.
    @classmethod
    def get_services(cls, name):
        try:
            return cls.service_instance[name]
        except:
            # TODO Raise an error if the service is not found
            return None
