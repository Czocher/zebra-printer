OUTPUT = {
    # Can be 'printer' or 'file'
    'DESTINATION': 'printer',
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
