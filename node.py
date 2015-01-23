# -*- coding: utf-8 -*-
from output import Output
from rest import RESTConnection, NotFoundException, UnauthorizedException
from settings import NODE
from time import sleep
import logging


class Node(object):

    def run(self):
        while True:
            try:
                printRequest = self.get_print_request()
            except NotFoundException:
                logging.info("No print request to print. Waiting...")
                sleep(NODE['QUERY_TIME'])
                continue
            except UnauthorizedException:
                logging.warning("Node unauthorized. Waiting...")
                sleep(NODE['QUERY_TIME'])
                continue

            with Output.new() as output:
                try:
                    logging.info("Trying to print the request.")
                    output.printRequest(printRequest)
                except Exception as e:
                    logging.error("There was an error "
                                  "during printing:\n{}".format(e))
                    self.report_failure(printRequest)
                    continue
                logging.info("Succesfully printed the request.")
                self.report_success(printRequest)

            logging.info("Waiting for next request.")
            sleep(NODE['QUERY_TIME'])

    def get_print_request(self):
        """Return a print request for printing."""
        return RESTConnection.get_print_request()

    def report_success(self, printRequest):
        """Report printing success to the Supervisor."""
        return RESTConnection.post_print_request(printRequest['id'],
                                                 {'error': False})

    def report_failure(self, printRequest):
        """Report printing failure to the Supervisor."""
        return RESTConnection.post_print_request(printRequest['id'],
                                                 {'error': True})
