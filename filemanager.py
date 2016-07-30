import sys
import time


class FileManager:

    def __init__(self, file):
        self.file = file

    def log(self, traces_out):

        if not isinstance(traces_out, list):
            traces = [traces_out]
        else:
            traces = traces_out

        f = open(self.file, "a")

        try:
            f.write("Log time: " + time.asctime(time.localtime(time.time())) + '\n')
            f.writelines(traces)

        except Exception:
            f.write('Error logging the traces: ' + traces_out + '\n')
            f.write('Sys info: ' + str(sys.exc_info()[0]) + '\n')

        f.close()
