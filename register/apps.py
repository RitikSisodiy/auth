from django.apps import AppConfig
from .dispatcher import (
    ServiceDispatcher,
)
import sys
from register.logger import (
    log_startup_info
)


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

    # The App Startup Script that will be running when the app is started up. It loads the
    # ServiceDispatcher module and initialises it.
    def ready(self):
        is_manage_py = any(arg.casefold().endswith("manage.py") for arg in sys.argv)
        is_runserver = any(arg.casefold() == "runserver" for arg in sys.argv)

        if (is_manage_py and is_runserver) or (not is_manage_py):
            # Initialises the Service Dispatcher
            ServiceDispatcher()

            log_startup_info("APP-LOADED",
                             {
                                 "where": "Register App",
                             })
