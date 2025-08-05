# -*- coding: utf-8 -*-
import os

import qdarktheme
from PySide6.QtGui import QPainter, QFont, QColor
from PySide6.QtCore import QRectF, QSize,Signal
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QListWidget, QAbstractItemView, QGroupBox, QWidget, QListWidgetItem


class FileListWidget(QListWidget):


    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent=parent)
        self.setAcceptDrops(True)
        self._file_path_list = []
        # self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)

    def dragEnterEvent(self, event, /):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, e, /):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
        else:
            e.ignore()

    def dropEvent(self, event, /):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                path = url.toLocalFile()
                if not path:
                    continue
                item = QListWidgetItem()
                item.setSizeHint(QSize(100, 35))
                if os.path.isdir(path):
                    widget = CustomListItemWidget(str(path), "folder.svg")
                elif os.path.isfile(path) and path.endswith(".py"):
                    widget = CustomListItemWidget(str(path), "python.svg")
                else:
                    widget = CustomListItemWidget(str(path), "file.svg")
                self._file_path_list.append(path)

                self.addItem(item)
                self.setItemWidget(item, widget)

            event.acceptProposedAction()

        else:
            event.ignore()

    def clear_items(self):
        self._file_path_list.clear()
        for row in range(self.count()):
            # self.removeItemWidget()
            self.takeItem(row)

    def get_list_path(self):
        return self._file_path_list


class CustomListItemWidget(QWidget):
    """自定义组件，包含一个 QLabel 和一个 QPushButton"""

    def __init__(self, text, icon, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.text = text
        self.fontColor = qdarktheme.load_palette(theme="auto").text().color()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        size = event.rect()
        QSvgRenderer(f"{os.getcwd()}\\res\\{self.icon}").render(painter,
                                                                QRectF(5, 5, 25, 25))

        label_font = QFont()
        font_size = 10
        label_font.setPointSize(font_size)
        painter.setPen(qdarktheme.load_palette(theme="auto").text().color())
        painter.setFont(label_font)
        painter.drawText(size.height() + 10 + 5 + 10, (size.height() + font_size) // 2, self.text)

        painter.end()

    def setColor(self, value):
        self.color = value
        self.update()

    def setText(self, value):
        self.text = value
        self.update()
