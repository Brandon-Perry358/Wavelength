from PyQt5 import QtWidgets, QtGui, QtCore
import XMLHandler


class startupDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.XMLHandler = XMLHandler.XMLHandler()
        self.setWindowTitle("Startup Settings")
        self.setGeometry(100, 100, 340, 250)

        self.startupData = self.XMLHandler.readStartup()

        self.curPlaylistLabel = QtWidgets.QLabel(self)
        self.curPlaylistLabel.setText("Current Startup Playlist: " + self.startupData[0])
        self.curPlaylistLabel.setGeometry(25, 20, 200, 25)

        self.curThemeLabel = QtWidgets.QLabel(self)
        self.curThemeLabel.setText("Current Startup Theme: " + self.startupData[1])
        self.curThemeLabel.setGeometry(25, 70, 200, 25)


        self.changePlaylistButton = QtWidgets.QPushButton("Change Playlist", self)
        self.changePlaylistButton.setGeometry(10, 220, 100, 25)
        self.changePlaylistButton.clicked.connect(self.changePlaylist)

        self.changeThemeButton = QtWidgets.QPushButton("Change Theme", self)
        self.changeThemeButton.setGeometry(120, 220, 100, 25)
        self.changeThemeButton.clicked.connect(self.changeTheme)

        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.cancelButton.setGeometry(230, 220, 100, 25)
        self.cancelButton.clicked.connect(self.close)


    def changePlaylist(self):
        self.playlistList = QtWidgets.QListWidget()
        self.playlistNames = self.XMLHandler.getPlaylistNames()
        self.playlistList.setWindowTitle("Double click to choose Playlist")
        for playlist in self.playlistNames:
            self.playlistList.addItem(playlist)

        self.playlistList.addItem("None")
        self.playlistList.setGeometry(100, 100, 400, 250)
        self.playlistList.show()
        self.playlistList.itemDoubleClicked.connect(self.changePlaylistXML)

    def changePlaylistXML(self, playlist):
        self.XMLHandler.changeStartupPlaylist(playlist)
        self.curPlaylistLabel.setText("Current Startup Playlist: " + playlist.text())
        self.playlistList.close()

    def changeTheme(self):
        self.themeList = QtWidgets.QListWidget()
        self.themeNames = self.XMLHandler.getThemeNames()
        self.themeList.setWindowTitle("Double click to choose Theme")
        for theme in self.themeNames:
            self.themeList.addItem(theme)

        self.themeList.addItem("None")
        self.themeList.setGeometry(100, 100, 400, 250)
        self.themeList.show()
        self.themeList.itemDoubleClicked.connect(self.changeThemeXML)

    def changeThemeXML(self, theme):
        self.XMLHandler.changeStartupTheme(theme)
        self.curThemeLabel.setText("Current Startup Theme: " + theme.text())
        self.themeList.close()

