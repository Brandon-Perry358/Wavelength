import threading
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import time
import os
from queue import Queue
from just_playback import Playback
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPixmap, QFont

from tinytag import tinytag

playlist = []
queue = Queue()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wavelength Audio Player")
        self.setWindowIcon(QtGui.QIcon("WavelengthIcon.png"))
        self.setGeometry(100, 100, 700, 500)

        wavelengthLabel = QtWidgets.QLabel(self)
        wavelengthLabel.setText("Wavelength")
        wavelengthLabel.move(5, 0)


        song = tinytag.TinyTag.get("music/03 - The Son of Flynn.flac", image=True)

        albumArt = QtWidgets.QLabel(self)
        albumArt.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(song.get_image())
        albumArt.setPixmap(pixmap)
        albumArt.setGeometry(20, 40, 400, 360)

        # create button
        skipBackButton = QtWidgets.QPushButton("", self)
        skipBackButton.move(20, 450)
        skipBackButton.setGeometry(20, 450, 133, 35)
        skipBackButton.setStyleSheet(
            "background-image : url(skipBackButton.png); background-repeat : no-repeat; background-position : center;")
        # code for function
        # TODO

        # code for creating the button
        playPauseButton = QtWidgets.QPushButton("", self)
        # TODO Use Thread here
        playPauseButton.clicked.connect(lambda: queue.put("play/pause"))

        # move the button to the center of the window
        playPauseButton.move(125, 450)
        playPauseButton.setGeometry(153, 450, 134, 35)
        # add image to playpause button and center it
        playPauseButton.setStyleSheet(
            "background-image : url(playPauseButton.png); background-repeat : no-repeat; background-position : center;")

        # create button
        skipForwardButton = QtWidgets.QPushButton("", self)
        skipForwardButton.move(225, 450)
        skipForwardButton.setGeometry(287, 450, 133, 35)
        skipForwardButton.setStyleSheet(
            "background-image : url(skipForwardButton.png); background-repeat : no-repeat; background-position : center;")
        # code for function
        # TODO

        # make song name under art
        songLabel = QtWidgets.QLabel(self)
        songLabel.setGeometry(25, 400, 400, 25)
        songLabel.setText(self.setSongTitle())
        songLabel.setAlignment(QtCore.Qt.AlignCenter)
        songLabel.setFont(QtGui.QFont("Comic Sans MS", 18, QtGui.QFont.Bold))
        #songLabel.move(125, 375)

        # make artist name under song title
        artistLabel = QtWidgets.QLabel(self)
        artistLabel.setGeometry(25, 420, 400, 40)
        artistLabel.setText(self.setArtist())
        artistLabel.setAlignment(QtCore.Qt.AlignCenter)
        artistLabel.setFont(QtGui.QFont("Comic Sans MS", 12))
        #artistLabel.move(125, 390)


        # code for creating the stop button
        stopButton = QtWidgets.QPushButton("Stop", self)
        stopButton.clicked.connect(lambda: queue.put("stop"))
        # move the button below the play/pause button
        stopButton.move(175, 0)

        fileBrowserButton = QtWidgets.QPushButton("Select Song", self)
        fileBrowserButton.clicked.connect(lambda: queue.put("browse"))
        # move the button to the top bar
        fileBrowserButton.move(75, 0)

        # Show current song location
        currintPosLabel = QtWidgets.QLabel(self)
        currintPosLabel.setGeometry(550, 50, 30, 30)
        currintPosLabel.setText("0:00")

        # make seek bar
        seekBar = QtWidgets.QSlider(self)
        seekBar.setOrientation(QtCore.Qt.Vertical)
        seekBar.setGeometry(550, 75, 25, 300)
        seekBar.setInvertedAppearance(True)



        # show total song time
        trackLengthLabel = QtWidgets.QLabel(self)
        trackLengthLabel.setGeometry(550, 375, 30, 30)
        trackLengthLabel.setText(self.setTimeLeft())



        playPlaylistButton = QtWidgets.QPushButton("Play Playlist", self)
        playPlaylistButton.clicked.connect(lambda: queue.put("play playlist"))
        # move the button above the play/pause button
        playPlaylistButton.move(275, 0)
        # code for the clear playlist button
        clearPlaylistButton = QtWidgets.QPushButton("Clear Playlist", self)
        clearPlaylistButton.clicked.connect(lambda: playlist.clear())
        # move the button above the play/pause button
        clearPlaylistButton.move(375, 0)
        # code for the add to playlist button
        addToPlaylistButton = QtWidgets.QPushButton("Add to Playlist", self)
        addToPlaylistButton.clicked.connect(lambda: queue.put("add to playlist"))
        addToPlaylistButton.move(475, 0)
        printPlaylistButton = QtWidgets.QPushButton("Print Playlist", self)
        printPlaylistButton.clicked.connect(lambda: queue.put("print"))
        printPlaylistButton.move(575, 0)

        # put a message in the queue to stop the thread when the window is closed
        self.destroyed.connect(lambda: queue.put("close"))

    def browse(self):
        widget = QWidget(self)
        widget.setGeometry(50, 50, 256, 64)
        file = QFileDialog.getOpenFileName(widget, 'Open file', 'C:\Wavelength', "Audio files (*.mp3 *.wav *.flac)")
        widget.destroy()
        if file[0] == "":
            # don't return anything
            pass
        else:
            return file[0]

    def play_audio(self, queue):
        # code for initializing and playing audio
        player = Playback()
        player.set_volume(1)
        while True:
            message = queue.get()
            if message == "play/pause":
                if player.playing:
                    player.pause()
                else:
                    player.resume()
                    # print(player.duration)
                    # print(type(player.duration))
            elif message == "stop":
                player.stop()
            elif message == "browse":
                file = self.browse()
                player.load_file(file)
                player.play()
            elif message == "play playlist":
                # play the songs in order
                for song in playlist:
                    if song == None:
                        pass
                    else:
                        player.load_file(song)
                        player.play()
                        # this plays the whole playlist, but play/pause and stop don't work
                        while player.active:
                            time.sleep(1)
            elif message == "add to playlist":
                file = self.browse()
                playlist.append(file)
            elif message == "print":
                for song in playlist:
                    print(song)
            elif message == "close":
                player.stop()
                break

    def setTimeLeft(self):
        min = 0
        sec = 0
        metadata = tinytag.TinyTag.get("music/03 - The Son of Flynn.flac")
        min = int(metadata.duration % 3600 / 60)
        sec = int(metadata.duration % 3600 % 60)
        retString = str(min) + ":" + str(sec)
        return retString

    def setSongTitle(self):
        metadata = tinytag.TinyTag.get("music/03 - The Son of Flynn.flac")
        return str(metadata.title)

    def setArtist(self):
        metadata =tinytag.TinyTag.get("music/03 - The Son of Flynn.flac")
        return str(metadata.artist)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())