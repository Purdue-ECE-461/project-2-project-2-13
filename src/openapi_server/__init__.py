import logging
from connexion.apps.flask_app import FlaskApp
from openapi_server import encoder

logging.basicConfig(level=logging.DEBUG)
app = FlaskApp(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml', pythonic_params=True)