from flask import Flask
from flask_restful import Api
from endpoints.Scraping import Scraping
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from flask_log_request_id import RequestID, RequestIDLogFilter

app = Flask(__name__)
api = Api(app)
RequestID(app)

api.add_resource(Scraping, "/v1/scraping")

logname = "service.log"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(logname)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(request_id)s - %(message)s"))
handler.addFilter(RequestIDLogFilter())  # << Add request id contextual filter
logger.addHandler(handler)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5002)
