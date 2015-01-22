import settings
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

    def printRequest(self, printRequest):
        # TODO: Chdir?
        fileName = "{}-{}-{}.ps".format(printRequest['author'],
                                        printRequest['problem'],
                                        datetime.now().isoformat())
        command = 'a2ps --output="{}" --pretty-print="{}" --header="{}" \
                --left-footer --footer --center-title="{}"'
        command = command.format(
            fileName,
            printRequest['language'].lower().encode('utf-8'),
            remove_accents(printRequest['contest'])
        )
        proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        proc.communicate(input=remove_accents(printRequest['source']))
        proc.wait()

    def test(self):
        if which('a2ps') is None:
            raise UnsupportedOutputException("a2ps is requred but \
                                             does not exist on path")


class PrinterOutput(Output):

    def printRequest(self, printRequest):
        pass

    def test(self):
        pass
