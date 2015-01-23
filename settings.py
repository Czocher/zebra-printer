import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
p = lambda *x: os.path.join(PROJECT_ROOT, *x)


OUTPUT = {
    # Can be 'printer' or 'file'
    'DESTINATION': 'file',
    # Absolute path to output directory for file output
    'OUTPUT_DIR': p('output/'),
    # CUPS queue name (lpstat -p)
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
