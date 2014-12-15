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
                printRequest = RESTConnection.get_print_request()
            except NotFoundException:
                logging.info("No submission to judge. Waiting...")
                sleep(NODE['QUERY_TIME'])
                continue
            except UnauthorizedException:
                logging.warning("Node unauthorized. Waiting...")
                sleep(NODE['QUERY_TIME'])
                continue

            with Output.new() as output:
                output.printRequest(printRequest)

            logging.info("Waiting for next request.")
            sleep(NODE['QUERY_TIME'])
