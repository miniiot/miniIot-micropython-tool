# -*- coding: utf-8 -*-
import json


def read_mbin_info(path):
    f = open(path, 'rb')
    info = {"head": 18,
            "sign": 5,
            "version": 4,
            "size": 4,
            "dateTime": 4,
            "info_len": 4}

    read_info = {}
    if f.read(info.get("head")) != b'MiniIotMicroPython':
        raise Exception("MiniIotMicroPython is not a MiniIotMicroPython")
    f.read(1)
    read_info["sign"] = f.read(info.get("sign")).decode()
    f.read(1)
    read_info["version"] = int.from_bytes(f.read(info.get("version")), byteorder='big') / 100
    f.read(1)
    read_info["size"] = int.from_bytes(f.read(info.get("size")), byteorder='big')
    f.read(1)
    read_info["dateTime"] = int.from_bytes(f.read(info.get("dateTime")), byteorder='big')
    f.read(1)
    read_info["info_len"] = int.from_bytes(f.read(info.get("info_len")), byteorder='big')
    f.read(1)
    read_info["mpy_info"] = json.loads(f.read(read_info["info_len"]).decode())

    return read_info


if __name__ == '__main__':
    print(read_mbin_info("3b8b5cae-3683-4c56-a809-1a1390e58e91.mbin"))
