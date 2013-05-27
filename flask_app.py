#!/usr/bin/env python

# Flask app
from skylines import app as flask_app

# ToscaWidgets
from tw.api import make_middleware

# TurboGears app
from skylines.config.middleware import make_app
from skylines.config.environment import conf_from_file

# WSGI server
from werkzeug.serving import run_simple
from paste.cascade import Cascade


if __name__ == '__main__':
    # Insert ToscaWidgets Middleware
    flask_app.wsgi_app = make_middleware(flask_app.wsgi_app, stack_registry=True)

    # Create TurboGears app
    tg_conf = conf_from_file()
    tg_app = make_app(tg_conf.global_conf, **tg_conf.local_conf)

    # Create WSGI cascade with tg priority
    app = Cascade([tg_app, flask_app])

    # Run the WSGI server
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)
