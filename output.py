import settings
import os
import logging
import errno
from datetime import datetime
from utils import remove_accents, which
from subprocess import Popen, PIPE


class UnsupportedOutputException(Exception):
    """Raised when the system cannot use the given output."""
    pass


class Output(object):

    @classmethod
    def new(cls):
        if settings.OUTPUT['DESTINATION'] == 'printer':
            return PrinterOutput()
        elif settings.OUTPUT['DESTINATION'] == 'file':
            return FileOutput()
        else:
            return Output()

    def printRequest(self, printRequest):
        """Print the given print request to the given output."""
        raise NotImplementedError()

    def test(self):
        """Test the output, raise exceptions if there is an error."""
        raise NotImplementedError()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        return self


class FileOutput(Output):

    def __init__(self):
        try:
            os.mkdir(settings.OUTPUT['OUTPUT_DIR'])
        except OSError as e:
            if e.errno != errno.EEXIST:
                logging.error("Error while creating output directory.")
                raise

    def printRequest(self, printRequest):
        fileName = "{}-{}.ps".format(printRequest['author'],
                                     datetime.now().isoformat())

        command = 'a2ps --output="{}" --pretty-print="{}" --header="{}" \
                --left-footer --footer="{}" --center-title="{}" \
                --line-numbers=1'

        if printRequest['problem'] is not None:
            title = printRequest['problem']
        else:
            title = "Source code"

        path = os.path.join(settings.OUTPUT['OUTPUT_DIR'], fileName)

        command = command.format(
            path,
            printRequest['language'].lower().encode('utf-8'),
            remove_accents(printRequest['contest']),
            printRequest['author'],
            title
        )
        proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        proc.communicate(input=remove_accents(printRequest['source']))
        proc.wait()

    def test(self):
        if which('a2ps') is None:
            raise UnsupportedOutputException("a2ps is required but \
                                             does not exist on path")


class PrinterOutput(Output):

    def printRequest(self, printRequest):
        command = 'a2ps --output="{}" --pretty-print="{}" --header="{}" \
                --left-footer --footer="{}" --center-title="{}" \
                --line-numbers=1'

        if printRequest['problem'] is not None:
            title = printRequest['problem']
        else:
            title = "Source code"

        command = command.format(
            settings.OUTPUT['PRINTER_NAME'],
            printRequest['language'].lower().encode('utf-8'),
            remove_accents(printRequest['contest']),
            printRequest['author'],
            title
        )
        proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        proc.communicate(input=remove_accents(printRequest['source']))
        proc.wait()

    def test(self):
        if which('a2ps') is None:
            raise UnsupportedOutputException("a2ps is required but \
                                             does not exist on path")
