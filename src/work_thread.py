# -*- coding: utf-8 -*-
import os
import subprocess
import time
import traceback

from PySide6.QtCore import QThread, Signal


class UpDateThread(QThread):
    run_result_signal = Signal(int, int, object)
    run_done_signal = Signal()

    def __init__(self, command: list):
        super().__init__()
        self.mode = 0
        self.command = command

    def run(self):
        try:

            self.run_build()

        except Exception as e:
            traceback.print_exc()
            self.run_done_signal.emit()
            pass

    def run_build(self):

        try:

            for index, command in enumerate(self.command):
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True, errors='ignore')

                # if process.stdout.read() == "":
                #     print("123")
                # else:
                #     print("32")

            self.run_done_signal.emit()

        except Exception as e:
            traceback.print_exc()
            self.run_done_signal.emit()

            pass

    def merge_file(self, file_name, version: str, file_path: list):
        """"""

        with open(file_name, "wb") as f:
            f.write(b'MiniIotMicroPython;')
            f.write(b'by:KS;')
            f.write(version.encode())
            f.write(b';')
            size = 0
            for path in file_path:
                with open(path, "rb") as f1:
                    size += f1.seek(0, os.SEEK_END)

            f.write(size.to_bytes(4, byteorder='big'))
            f.write(b';')


            for path in file_path:
                with open(path, "rb") as f2:
                    f.write(f2.read())


