from unidecode import unidecode
from six import text_type
import os


def which(program):

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def remove_accents(input_str):
    return unidecode(input_str)

def get_key_or_substitute(dictionary, key, substitute):
    ret = dictionary.get(key)
    if ret is None:
        return substitute
    return ret
