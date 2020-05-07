#!/usr/bin/env python3

import connexion


def greeting(name):
    return 'Hello {name}'.format(name=name)

def create_app():
    local_app = connexion.FlaskApp(__name__, port=5000, specification_dir='openapi/')
    local_app.add_api('spec.yaml', arguments={'title': 'Hello World Example'})

    return local_app.app
