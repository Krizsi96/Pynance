#!/usr/bin/env python3
from authentication.authentication import Authentication
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting gsheets")
try:
    user = Authentication("/home/kristof/Pynance/gsheets")
except FileNotFoundError as error:
    logging.error(error)
    exit(1)


if not user.check_credentials():
    try:
        user.login()
        user.save_credentials()
    except ValueError as error:
        logging.error(error)
        exit(1)

user.load_credentials()
