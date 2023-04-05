import io
import logging
import sys

from PyQt5.QtCore import QThread


class OutputLog(QThread):

    def run(self) -> None:
        print("start loger")
        stdout = io.StringIO()
        sys.stdout = stdout
        while True:
            try:
                if not stdout.readable():
                    print("不可达")
                    continue
                res = stdout.readline()
                logging.debug(res)
                print("output logs", res)
            except Exception as ret:
                print(ret)
