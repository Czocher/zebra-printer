import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def p(*x):
    return os.path.join(PROJECT_ROOT, *x)


OUTPUT = {
    # Can be 'printer' or 'file'
    'DESTINATION': 'printer',
    # Absolute path to output directory for file output
    'OUTPUT_DIR': p('output/'),
    # CUPS queue name (lpstat -v)
    'PRINTER_NAME': ''
}

NODE = {
    # Time between HTTP queries
    'QUERY_TIME': 5,
    'TOKEN': 'printerToken',
}

# Supervisor configuration
SUPERVISOR = {
    # The address of the Supervisor REST webservice
    'HOST': 'http://localhost:8000/rest/',
}
