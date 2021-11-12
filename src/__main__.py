#!/usr/bin/env python3

import connexion

from src.openapi_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./openapi_server/openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'ECE 461 - Fall 2021 - Project 2'},
                pythonic_params=True)
    app.run()


if __name__ == '__main__':
    main()
