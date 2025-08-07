# -*- coding: utf-8 -*-
import json
import os
import subprocess
import time
import traceback
import uuid

from PySide6.QtCore import QThread, Signal


class UpDateThread(QThread):
    run_result_signal = Signal(int, int, object)
    run_done_signal = Signal()
    run_progress_signal = Signal(int)

    def __init__(self, command: list, mpy_file_list:list, version=10):
        super().__init__()
        self.mode = 0
        self.command = command
        self.mpy_file_list = mpy_file_list
        self.version:int = version
        self.file_name = str(uuid.uuid4()) + ".mbin"
        self._is_done = True
        self._progress = 0
        self._command_process = (100- len(self.mpy_file_list)) / len(self.command)

    def run(self):
        try:

            is_done = self.run_build()
            if is_done:
                self.merge_file()

        except Exception as e:
            traceback.print_exc()
            self.run_done_signal.emit()
            pass

    def run_build(self):
        is_done = True


        try:

            for index, command in enumerate(self.command):
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True, errors='ignore')

                if process.stdout.read() == "":
                    self._progress += self._command_process
                    # print("build:",self._progress)
                    self.run_progress_signal.emit(self._progress)
                else:
                    is_done = False
                    self.run_progress_signal.emit(-1)


        except Exception as e:
            self._is_done = False
            traceback.print_exc()
            self.run_progress_signal.emit(-1)
            is_done = False

        return is_done

    def merge_file(self):
        """"""
        info = {"head": 19,
                "sign": 6,
                "version": 5,
                "size": 5,
                "dateTime": 5,
                "info_len": 5}

        with open(self.file_name, "wb") as f:
            f.write(b'MiniIotMicroPython;')
            f.write(b'by:KS;')
            f.write(self.version.to_bytes(4, byteorder='big'))
            f.write(b';')
            size = 0
            for path in self.mpy_file_list:

                with open(path[0], "rb") as f1:
                    size += f1.seek(0, os.SEEK_END)

            f.write(size.to_bytes(4, byteorder='big'))
            f.write(b';')

            unix_time = int(time.time())
            f.write(unix_time.to_bytes(4, byteorder='big'))
            # print(unix_time, unix_time.to_bytes(4, byteorder='big'))
            f.write(b';')

            mpy_info = {}

            for index, path in enumerate(self.mpy_file_list):
                with open(path[0], "rb") as f2:
                    mpy_info[str(path[1])] = f2.seek(0, os.SEEK_END)
            # print(mpy_info)
            mpy_info_str = json.dumps(mpy_info)
            mpy_info_byte = mpy_info_str.encode()


            f.write(len(mpy_info_byte).to_bytes(4, byteorder='big'))
            f.write(b';')
            f.write(mpy_info_byte)
            f.write(b';')

            for index, path in enumerate(self.mpy_file_list):
                with open(path[0], "rb") as f3:
                    # print(f3.read())
                    f.write(f3.read())
                    self._progress +=1
                    self.run_progress_signal.emit(self._progress)



