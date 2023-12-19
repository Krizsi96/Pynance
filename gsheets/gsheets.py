#!/usr/bin/env python3
from authentication.authentication import Authentication

user = Authentication("/home/kristof/Pynance/gsheets")

if not user.check_credentials():
    try:
        user.login()
        user.save_credentials()
    except ValueError as error:
        print(error)
        exit(1)

user.load_credentials()
