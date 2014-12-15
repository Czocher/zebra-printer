import settings

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
        raise NotImplementedError()

    def test(self):
        raise NotImplementedError()


class PrinterOutput(Output):

    def printRequest(self, printRequest):
        pass

    def test(self):
        pass

