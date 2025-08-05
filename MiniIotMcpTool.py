import os
import platform
import sys
from pathlib import Path

import qdarktheme
from PySide6.QtCore import QLocale, QTranslator
from PySide6.QtWidgets import QApplication

from src.app import MainViewWindow

if __name__ == '__main__':

    # if platform.system() == "Windows":
    #     path = os.path.join(os.getcwd(),"mpy-cross")
    # elif platform.system() == "Linux":
    #     path = os.path.join(os.getcwd(),"mpy-cross")
    # elif platform.system() == "Darwin":
    #     path = os.path.join(os.getcwd(),"mpy-cross")
    # else:
    #     path = os.path.join(os.getcwd(),"mpy-cross")

    folder = Path(os.path.join(os.getcwd(), "mpy-cross"))
    for name in [f.name for f in folder.iterdir() if f.is_dir()]:
        os.environ[f"MPY_CROSS_{name}"] = os.path.join(os.getcwd(), "mpy-cross", name)

    app = QApplication([])
    qdarktheme.enable_hi_dpi()

    locale = QLocale.system().name()
    translator = QTranslator()
    if translator.load(f"{os.getcwd()}\\translations\\{locale}.qm"):
        app.installTranslator(translator)

    qdarktheme.setup_theme(theme="auto")
    screen = MainViewWindow()
    screen.show()

    sys.exit(app.exec())
