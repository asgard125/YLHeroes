import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from MapGenerator import run_mapgenerator
from SrategicView import run_map
from PyQt5.QtWidgets import QInputDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)
        self.startGameButton.clicked.connect(self.run_game)
        self.mapGenButton.clicked.connect(self.run_mapgenerator)
        self.exitButton.clicked.connect(self.exit_window)

    def run_game(self):
        f = open(f"maps/maplist.txt", 'r', encoding='utf8')
        maplist = list(map(lambda x: x.strip('\n'), f.readlines()))
        f.close()
        mapname, OkPressed = QInputDialog.getItem(self, "Выберите",
                                                  "Выберите карту для игры",
                                                  maplist,
                                                  1, False)
        if OkPressed:
           run_map(mapname)

    def run_mapgenerator(self):
        run_mapgenerator()

    def exit_window(self):
        sys.exit(app.exec_())


app = QApplication(sys.argv)
ex = MyWidget()
ex.setFixedSize(851, 738)
ex.show()
sys.exit(app.exec_())

