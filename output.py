class Output(object):

    @classmethod
    def new(cls):
        if settings.OUTPUT['DESTINATION'] = 'printer':
            pass
        elif settings.OUTPUT['DESTINATION'] = 'file':
            pass
        else:
            return Output()

    def print(self, printRequest):
        """Print the given print request to the given output."""
        raise NotImplementedError()


class FileOutput(Output):

    def print(self, printRequest):
        raise NotImplementedError()


class PrinterOutput(Output):

    def print(self, printRequest):
        raise NotImplementedError();

