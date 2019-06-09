#!/usr/bin/env python3

import sys
import enum

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QSizePolicy,
    QPushButton,
    QAction,
    QLineEdit,
    QFrame,
)
from PyQt5.QtGui import (
    QIcon,
)
from PyQt5.QtCore import (
    pyqtSignal,
)

from backend import TaskList
from settings import Settings


class Sorts(enum.Enum):
    TIME = 1
    ALPH = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Work Times'
        self.width = 300
        self.hight = 500
        self.setUI()

        # style sheets
        with open("stylesheets/main.stylesheet", "r") as ss:
            self.setStyleSheet(ss.read())


        #self.setWindowIcon(QIcon(svg_path('icon.ico')))

        self.saved = True

        self.taskList = TaskList()
        self.settings = Settings()

        menubar = self.menuBar()
        filebar = menubar.addMenu('&File')
        editbar = menubar.addMenu('&Edit')
        aboutbar = menubar.addMenu('&About')

        quitter = QAction('&Exit', self)
        quitter.setShortcut('Ctrl+Q')
        quitter.triggered.connect(self.quit)

        saver = QAction('&Save', self)
        saver.setShortcut('Ctrl+S')
        saver.triggered.connect(self.save)

        settingser = QAction('&Settings', self)
        settingser.triggered.connect(self.open_settings)

        abouter = QAction('About', self)
        abouter.triggered.connect(self.open_about)

        filebar.addAction(saver)
        filebar.addAction(quitter)
        editbar.addAction(settingser)
        aboutbar.addAction(abouter)

        main = QWidget(self)
        self.setCentralWidget(main)

        self.top_bar = ControllerWidget(self)

        adder = lambda: self.add(self.top_bar.entry_field.text())
        self.top_bar.entry_field.returnPressed.connect(adder)

        self.top_bar.save_button.pressed.connect(self.save)
        self.top_bar.sort_button_time.pressed.connect(lambda: self.sort(Sorts.TIME))
        self.top_bar.sort_button_alph.pressed.connect(lambda: self.sort(Sorts.ALPH))
        self.top_bar.start_stop_button.pressed.connect(self.toggle_running)
        self.top_bar.settings_button.pressed.connect(self.open_settings)
        self.top_bar.add_button.pressed.connect(adder)

        self.ongoing = TaskListerWidget(self, '#006cb2')
        self.paused = TaskListerWidget(self, '#006cb2')

        layout = QVBoxLayout(main)
        #layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.top_bar)
        layout.addWidget(self.ongoing)
        layout.addWidget(self.paused)


    def setUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.hight)
        #self.setFixedSize(self.width, self.hight)
        self.show()

    def save(self):
        if not self.saved:
            self.settings.save()
            print('saved')
            self.saved = True
            self.update()

    def quit(self):
        self.save()
        qApp.quit()

    def update(self):
        pass

    def sort(self, sort):
        if sort == Sorts.ALPH:
            print('sorting alphabetically')
        elif sort == Sorts.TIME:
            print('sorting chonologically')
        self.top_bar.toggle_sort(sort)

    def add(self, title):
        print('added task: {}'.format(title))

    def toggle_running(self):
        print('starting task timer')
        self.top_bar.toggle_start_stop()

    def open_settings(self):
        print('opened settings')

    def open_about(self):
        print('opened about')


class ButtonState(enum.Enum):
    PLAY = '⏸'
    PAUSE = '▶'
    DOWN = '▼'
    UP = '▲'
    NONE = '   '

    __TOGGLE__ = {
        PLAY: PAUSE,
        PAUSE: PLAY,
        DOWN: UP,
        UP: DOWN,
        NONE: DOWN,
    }

    def next(self):
        return ButtonState(self.__TOGGLE__[self.value])


class ControllerWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.playing = ButtonState.PAUSE
        self.sorting = {
            Sorts.TIME: ButtonState.NONE,
            Sorts.ALPH: ButtonState.NONE,
        }

        self.entry_field = QLineEdit(self)
        self.entry_field.setPlaceholderText('New Task')

        self.save_button = QPushButton('Save', self)
        self.sort_button_time = QPushButton('', self)  # 🔤 🔠 🔡
        self.sort_button_alph = QPushButton(' ', self)
        self.start_stop_button = QPushButton('', self)  # ▶ / ⏸ / ⏹
        self.settings_button = QPushButton('⚙', self)
        self.add_button = QPushButton('Add', self)

        self.update_buttons()

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.save_button, 0, 0)
        layout.addWidget(self.sort_button_time, 0, 1)
        layout.addWidget(self.sort_button_alph, 0, 2)
        layout.addWidget(self.start_stop_button, 0, 3)
        layout.addWidget(self.settings_button, 0, 5)
        layout.addWidget(self.entry_field, 1, 0, 2, 4)
        layout.addWidget(self.add_button, 1, 5)

        self.setFixedHeight(self.save_button.height()*2)
        #self.setFixedHeight(self.entry_field.height()*2 + 5)
        #layout.setSizePolicy(QSizePolicy.Minimum)

    def toggle_start_stop(self, state=None):
        if state:
            self.playing = state
        else:
            self.playing = self.playing.next()

        self.update_buttons()

    def toggle_sort(self, sort, state=None):
        if state:
            self.sorting[sort] = state
        else:
            self.sorting[sort] = self.sorting[sort].next()

        other_sorts = set(Sorts)
        other_sorts.remove(sort)
        for other in other_sorts:
            self.sorting[other] = ButtonState.NONE

        self.update_buttons()

    def update_buttons(self):
        self.start_stop_button.setText(self.playing.value)
        self.sort_button_time.setText('🕒 ' + self.sorting[Sorts.TIME].value)
        self.sort_button_alph.setText('🔤 ' + self.sorting[Sorts.ALPH].value)


class TaskListerWidget(QFrame):
    def __init__(self, parent, color):
        super().__init__(parent)

        self.setStyleSheet("background-color:{};".format(color))
        self.setGeometry(10, 10, 300, 100)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

