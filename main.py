#!/usr/bin/env python3
from output import Output
from node import Node

import locale
import logging
import sys


# Set the default locale for dates and times in logs
locale.setlocale(locale.LC_ALL, '')

FORMAT = '%(asctime)s - %(levelname)s - [%(module)s.%(funcName)s] %(message)s'

logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT,
    datefmt='%c'
)

if __name__ == '__main__':
    # Test if the output is valid
    with Output.new() as output:
        output.test()

    # Start the Node
    try:
        node = Node()
        node.run()
    except KeyboardInterrupt:
        logging.info("Node successfully terminated.")
        sys.exit(0)
