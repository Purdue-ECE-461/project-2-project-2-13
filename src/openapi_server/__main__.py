import logging
from openapi_server import app

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="localhost", port=8080, debug=True)