#!/usr/bin/env python3

import logging
import connexion

from openapi_server import encoder


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml')
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
