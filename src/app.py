# -*- coding: utf-8 -*-
import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QGroupBox, QVBoxLayout,
                               QListWidget, QPushButton,
                               QLineEdit, QLabel, QComboBox, QSpacerItem, QProgressBar)

from src.custom_widget import FileListWidget
from src.work_thread import UpDateThread


class MainViewWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._mpy_version = [('v1.23.0', '6.3'), ('v1.22.0', '6.2'), ('v1.20.0', '6.1'), ('v1.19', '6'), ('v1.12', '5'),
                             ('v1.11', '4'), ('v1.9.3', '3'), ('v1.9', '2')]
        self._mpy_sys = ["xtensa", "x86", "x64", "armv6", "armv6m", "armv7m", "armv7em", "armv7emsp", "armv7emdp",
                         "xtensawin", "rv32imc", "debug"]

        self._file_path_list = []

        self.initUI()
        self.initData()

    def initUI(self):
        self.setWindowTitle(self.tr("PressureCalibration"))
        self.setMinimumSize(700, 450)
        # self.setWindowIcon(QIcon(f'{os.getcwd()}\\logo.ico'))

        self.status_bar_progress = QProgressBar()
        self.status_bar_progress.setMinimum(0)
        self.status_bar_progress.setMaximum(100)
        self.status_bar_progress.setValue(0)
        self.status_bar_progress.setMaximumHeight(15)
        self.status_bar_progress.setMaximumWidth(150)

        self.status_bar_progress.setStyleSheet("""
        QProgressBar::chunk {
            background-color: #02913a;
            width: 50px;
        }
        """)
        self.status_bar_label = QLabel(self.tr("build"))
        self.statusBar().addPermanentWidget(self.status_bar_label)
        self.statusBar().addPermanentWidget(self.status_bar_progress)
        self.status_bar_progress.show()
        self.status_bar_label.show()

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        file_select_box = QGroupBox(self.tr("Select Files"))
        self.layout.addWidget(file_select_box)

        file_select_layout = QHBoxLayout()
        file_select_box.setLayout(file_select_layout)

        current_file_list_box = QGroupBox(self.tr("Current Files"))
        file_select_layout.addWidget(current_file_list_box)

        current_file_list_lay = QVBoxLayout()
        current_file_list_box.setLayout(current_file_list_lay)

        current_file_select_btn_layout = QHBoxLayout()
        current_file_list_lay.addLayout(current_file_select_btn_layout)

        clear_btn = QPushButton(self.tr("Clear"))
        clear_btn.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: #ff7b72;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            ''')
        select_btn = QPushButton(self.tr("Select"))
        select_btn.setStyleSheet('''
        QPushButton {
            color: white;
            background-color: #0078D7;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 14px;
        }
        ''')

        current_file_select_btn_layout.addWidget(clear_btn)
        current_file_select_btn_layout.addWidget(select_btn)

        self.current_file_select_list = FileListWidget()
        current_file_list_lay.addWidget(self.current_file_select_list)

        mpy_file_list_box = QGroupBox(self.tr("MicroPython Files"))
        file_select_layout.addWidget(mpy_file_list_box)

        mpy_file_list_lay = QVBoxLayout()
        mpy_file_list_box.setLayout(mpy_file_list_lay)

        self.mpy_root_path = QLineEdit()
        self.mpy_root_path.setText("/")
        mpy_file_list_lay.addWidget(self.mpy_root_path)

        self.mpy_file_select_list = FileListWidget()
        self.mpy_file_select_list.setAcceptDrops(False)
        mpy_file_list_lay.addWidget(self.mpy_file_select_list)

        mpy_setup_box = QGroupBox(self.tr("Build"))
        self.layout.addWidget(mpy_setup_box)

        mpy_setup_layout = QHBoxLayout()
        mpy_setup_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mpy_setup_box.setLayout(mpy_setup_layout)

        versions_select_label = QLabel(self.tr("MicroPython Versions"))
        self.versions_select_combo = QComboBox()

        sys_select_label = QLabel(self.tr("System"))
        self.sys_select_combo = QComboBox()

        versions_info_label = QLabel(self.tr("Versions"))
        self.versions_info_edit = QLineEdit()
        # versions_info_edit.setFixedWidth(150)

        setup_btn = QPushButton(self.tr("Build"))
        setup_btn.setStyleSheet('''
        QPushButton {
            color: white;
            background-color: #0078D7;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 14px;
        }
        ''')

        mpy_setup_layout.addWidget(versions_select_label)
        mpy_setup_layout.addWidget(self.versions_select_combo, 1)
        mpy_setup_layout.addSpacerItem(QSpacerItem(20, 0))
        mpy_setup_layout.addWidget(sys_select_label)
        mpy_setup_layout.addWidget(self.sys_select_combo, 1)
        mpy_setup_layout.addSpacerItem(QSpacerItem(20, 0))

        mpy_setup_layout.addWidget(versions_info_label)
        mpy_setup_layout.addWidget(self.versions_info_edit, 1)
        mpy_setup_layout.addWidget(setup_btn, 1)

        setup_btn.clicked.connect(self.on_setup_btn_click_callback)

    def initData(self):
        self.versions_select_combo.addItems([ver[0] for ver in self._mpy_version])
        self.sys_select_combo.addItems(self._mpy_sys)
        self.versions_info_edit.setText("1.0")

    def initSignalCallback(self):
        pass

    def on_setup_btn_click_callback(self):
        if len(self.current_file_select_list.get_list_path()) == 0:
            return
        print([str(s) for s in self.current_file_select_list.get_list_path()])
        mpy_ver = self.versions_select_combo.currentText()
        mpy_sys = self.sys_select_combo.currentText()
        commands = []
        # relatively_path = []
        build_path = []

        for path in self.current_file_select_list.get_list_path():

            if path.is_dir():
                sub_path = [f for f in path.rglob("*") if f.is_file()]
                for sub in sub_path:
                    if sub.suffix != ".py":
                        continue

                    rela_path = self.get_relatively_path(path, sub)
                    build_path.append((sub.with_suffix(".mpy"), rela_path[0].with_suffix(".mpy")))
                    command = (os.path.join(os.environ.get(f"MPY_CROSS_{mpy_ver}"), "mpy-cross"),
                               f"-march={mpy_sys}",
                               str(sub))
                    print(str(sub))
                    commands.append(command)

            elif path.is_file() and path.suffix == ".py":
                rela_path = self.get_relatively_path(path, path)
                build_path.append((path.with_suffix(".mpy"), rela_path[0].with_suffix(".mpy")))
                command = (os.path.join(os.environ.get(f"MPY_CROSS_{mpy_ver}"), "mpy-cross"),
                           f"-march={mpy_sys}",
                           str(path))
                commands.append(command)
                print(str(Path(path)))
            else:
                continue
        # print(commands)
        print(build_path)
        self._thread = UpDateThread(commands,build_path)
        # self._thread.run_result_signal.connect(self.on_read_update_data_callback)
        # self._thread.run_done_signal.connect(self.on_run_done_callback)
        self._thread.run_progress_signal.connect(self.on_thread_progress_callback)
        self._thread.start()

    def on_thread_progress_callback(self,value):
        if value == -1:
            self.status_bar_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #ff0000;
                width: 50px;
            }
            """)
            self.status_bar_label.setText(self.tr("build failed"))

        else:
            self.status_bar_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #02913a;
                width: 50px;
            }
            """)
            self.status_bar_label.setText(self.tr("build ..."))

        if value >= 100:
            self.status_bar_label.setText(self.tr("build done"))


        self.status_bar_progress.setValue(value)
        self.status_bar_progress.show()
        self.status_bar_label.show()



    def get_relatively_path(self, compare_path: Path, absolute_path: Path):
        if absolute_path.is_dir():
            absolute_path = [f for f in absolute_path.rglob("*") if f.is_file()]
        elif absolute_path.is_file() and absolute_path.suffix == ".py":
            absolute_path = [absolute_path]
        else:
            return []

        if compare_path.is_file() and compare_path.suffix == ".py":
            compare_path = compare_path.parent
        elif compare_path.is_dir():
            compare_path = compare_path.parent
        else:
            return []

        paths = []

        for path in absolute_path:
            p = Path(path)
            try:
                p = p.relative_to(compare_path)
                paths.append(p)
            except:
                pass

        return paths


