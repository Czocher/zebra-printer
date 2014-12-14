# -*- coding: utf-8 -*-
from output import Output
from rest import RESTConnection
from settings import QUERY_TIME
from time import sleep

class Node(object):

    def run(self):
        while True:
            try:
                printRequest = RESTConnection.get_print_request()
            except:
                sleep(QUERY_TIME)
                continue

            with Output.new() as output:
                output.print(printRequest)

            sleep(QUERY_TIME)
