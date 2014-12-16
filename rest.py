#! /usr/bin/env python
#-*- coding: utf8 -*-

from settings import NODE, SUPERVISOR
from httplib import FORBIDDEN, NOT_FOUND, OK
from sys import exit
from requests import ConnectionError

import logging
import os
import requests
import json


class NotFoundException(Exception):
    """Raised when there is no print request."""
    pass


class UnauthorizedException(Exception):
    """Raised when the Node is unauthorised."""
    pass


class UnknownErrorException(Exception):
    """Raised when an unknown error occured."""
    pass


class RESTConnection(object):
    """Class gathering all the REST queries and requests."""

    @classmethod
    def __get(cls, url):
        """Perform a GET request on the given URL."""
        try:
            return requests.get(
                SUPERVISOR['HOST'] + url + '?format=json',
                verify=True,
                headers={'x_token': NODE['TOKEN']}
            )
        except ConnectionError as e:
            logging.critical("Connection failed: {}".format(e))
            exit(1)

    @classmethod
    def __put(cls, url, *args, **kwargs):
        """Perform a POST request on the given URL."""
        headers = {'x_token': NODE['TOKEN']}
        headers.update(kwargs.get('headers', {}))
        del kwargs['headers']
        try:
            return requests.put(
                SUPERVISOR['HOST'] + url + '?format=json',
                verify=True,
                headers=headers,
                *args, **kwargs
            )

        except ConnectionError as e:
            logging.critical("Connection failed: {}".format(e))
            exit(1)

    @classmethod
    def get_print_request(cls):
        """Get a new print request for printing."""

        # Prepare the URL
        url = 'printrequest/'

        response = cls.__get(url)

        if response.status_code == OK:
            # If everything is okay then parse the data and return it
            try:
                data = json.loads(response.text)
            except Exception as e:
                logging.error(
                    "Error while parsing response: {}\n{}.".format(data, e)
                )
                raise

            logging.info(
                "Recived print request id {}.".format(data['id'])
            )
            return data

        elif response.status_code == NOT_FOUND:
            logging.info("No print request recived.")
            raise NotFoundException()
        elif response.status_code == FORBIDDEN:
            logging.warning("Node unauthorized.")
            raise UnauthorizedException()
        else:
            logging.error("Unknown error status code: {}".format(
                response.status_code))
            raise UnknownErrorException()

    @classmethod
    def post_print_request(cls, printRequestId, printRequest):
        """Post a printed print request to the Supervisor."""

        url = 'printrequest/{}/'.format(printRequestId)

        # Prepare the print request
        try:
            data = json.dumps(printRequest)
        except:
            logging.critical("Data malformed {}.".format(printRequest))
            raise

        response = cls.__put(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == OK and not printRequest['error']:
            logging.info("The results have been sent.")
        elif response.status_code == OK and printRequest['error']:
            logging.info("Supervisor has been notified about the failure.")
        elif response.status_code == FORBIDDEN:
            logging.warning("Node unauthorized.")
            raise UnauthorizedException()
        else:
            logging.error("Unknown error status code: {}".format(
                response.status_code))
            raise UnknownErrorException()
