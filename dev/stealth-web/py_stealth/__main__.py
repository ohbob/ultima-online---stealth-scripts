
import os
import sys
import traceback

try:
    from py_stealth import methods, _protocol, utils
except ImportError:
    sys.path.insert(0, os.path.split(os.path.dirname(__file__))[0])
    from py_stealth import methods, _protocol, utils
finally:
    from py_stealth.config import DEBUG, ERROR_FILTER


PY2 = b'' == ''


class SysJournalOut:
    def __init__(self, stream=None):
        self._buffer = str()
        self.stream = stream

    def write(self, line):
        if self.stream is not None:
            self.stream.write(line)
        self._buffer += line
        if '\n' in line:
            self.flush()

    def flush(self):
        if self._buffer:
            methods.AddToSystemJournal(self._buffer)
            self._buffer = str()


def main():
    # check cmd
    try:
        self, script = sys.argv[:2]
    except ValueError:
        error = 'CMD params must be: path_to_script [port] [func] [args]'
        utils.show_error_message(error)
        exit(4)
        return
    # change output to the stealth system journal
    if not DEBUG:
        sys.stdout = sys.stderr = SysJournalOut()
    # modify the python import system
    if sys.version_info < (3, 4):  # 2.6 - 3.3
        import py_stealth.py26 as importer
    else:  # 3.4 and above
        import py_stealth.py34 as importer
    sys.meta_path.insert(0, importer.Finder())
    # run script
    directory, filename = os.path.split(script)
    sys.path.insert(0, directory)
    methods.Wait(1)  # connect and save a port number into the Connection class
    try:
        module = __import__(os.path.splitext(filename)[0])
        if len(sys.argv) >= 4:
            eval("module." + sys.argv[3])
    except Exception as error:
        if error is SystemExit:
            pass
        elif DEBUG or not ERROR_FILTER:
            raise error
        else:
            # clean package files and code from trace
            trace = traceback.format_exc().splitlines()
            skip = False
            for line in trace:
                if skip:
                    skip = False
                elif "\\py_stealth\\" in line or '/py_stealth/' in line:
                    skip = True
                elif "_bootstrap" not in line:
                    sys.stderr.write(line + '\n')


if __name__ == '__main__':
    main()
