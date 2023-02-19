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

playlist = []

def play_audio(queue):
    
    # code for initializing and playing audio
    pygame = Playback()
    #pygame.load_file("song.mp3")
    pygame.set_volume(1)
    #pygame.play()
    while True:
        message = queue.get()
        if message == "play/pause":
            if pygame.playing:
                pygame.pause()
            else:
                pygame.resume()
                print(pygame.duration)
                print(type(pygame.duration))
        elif message == "stop":
            pygame.stop()
        elif message == "browse":
            file = browse()
            playlist.append(file)
            #for song in playlist:
                #pygame.load_file(song)
                #pygame.play()
        elif message == "play playlist":
            #play the songs in order
            for song in playlist:
                if song == None:
                    pass
                else:
                    pygame.load_file(song)
                    pygame.play()
                #this plays the whole playlist, but play/pause and stop don't work
                #while pygame.active:
                    #time.sleep(1)
        elif message == "close":
            pygame.stop()
            break

def gui(queue):
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setGeometry(100, 100, 700, 500)

    # make program name in corner
    wavelengthLabel = QtWidgets.QLabel(window)
    wavelengthLabel.setText("Wavelength")
    wavelengthLabel.move(5, 0)

    albumArt = QtWidgets.QLabel(window)
    albumArt.setPixmap(QtGui.QPixmap("Tron_Legacy_Soundtrack.jpg"))
    albumArt.setGeometry(20, 40, 400, 360)

    # create button
    skipBackButton = QtWidgets.QPushButton("", window)
    skipBackButton.move(20, 450)
    skipBackButton.setGeometry(20, 450, 133, 35)
    skipBackButton.setStyleSheet("background-image : url(skipBackButton.png); background-repeat : no-repeat; background-position : center;")
    # code for function
    # TODO

    # code for creating the button
    playPauseButton = QtWidgets.QPushButton("", window)
    playPauseButton.clicked.connect(lambda: queue.put("play/pause"))
    # move the button to the center of the window
    playPauseButton.move(125, 450)
    playPauseButton.setGeometry(153, 450, 134, 35)
    #add image to playpause button and center it
    playPauseButton.setStyleSheet("background-image : url(playPauseButton.png); background-repeat : no-repeat; background-position : center;")

    # create button
    skipForwardButton = QtWidgets.QPushButton("", window)
    skipForwardButton.move(225, 450)
    skipForwardButton.setGeometry(287, 450, 133, 35)
    skipForwardButton.setStyleSheet("background-image : url(skipForwardButton.png); background-repeat : no-repeat; background-position : center;")
    # code for function
    # TODO

    # make song name under art
    songLabel = QtWidgets.QLabel(window)
    songLabel.setGeometry(25, 400, 400, 25)
    songLabel.setText("The Son of Flynn")
    songLabel.setAlignment(QtCore.Qt.AlignCenter)
    songLabel.setFont(QtGui.QFont("Comic Sans MS", 18, QtGui.QFont.Bold))
    #songLabel.move(125, 375)

    # make artist name under song title
    artistLabel = QtWidgets.QLabel(window)
    artistLabel.setGeometry(25, 420, 400, 40)
    artistLabel.setText("Daft Punk")
    artistLabel.setAlignment(QtCore.Qt.AlignCenter)
    artistLabel.setFont(QtGui.QFont("Comic Sans MS", 12))
    #artistLabel.move(125, 390)


    # code for creating the stop button
    stopButton = QtWidgets.QPushButton("Stop", window)
    stopButton.clicked.connect(lambda: queue.put("stop"))
    # move the button below the play/pause button
    stopButton.move(175, 0)


    fileBrowserButton = QtWidgets.QPushButton("Browse", window)
    fileBrowserButton.clicked.connect(lambda: queue.put("browse"))
    # move the button to the top bar
    fileBrowserButton.move(75, 0)

    # Show current song location
    currintPosLabel = QtWidgets.QLabel(window)
    currintPosLabel.setGeometry(550, 50, 30, 30)
    currintPosLabel.setText("0:00")

    # make seek bar
    seekBar = QtWidgets.QSlider(window)
    seekBar.setOrientation(QtCore.Qt.Vertical)
    seekBar.setGeometry(550, 75, 25, 300)
    seekBar.setInvertedAppearance(True)

    # show total song time
    trackLengthLabel = QtWidgets.QLabel(window)
    trackLengthLabel.setGeometry(550, 375, 30, 30)
    trackLengthLabel.setText("1:34")


    # code for creating the button
    #playPauseButton = QtWidgets.QPushButton("Play/Pause", window)
    #playPauseButton.clicked.connect(lambda: queue.put("play/pause"))
    # move the button to the center of the window
    #playPauseButton.move(100, 100)
    # code for creating the stop button
    #stopButton = QtWidgets.QPushButton("Stop", window)
    #stopButton.clicked.connect(lambda: queue.put("stop"))
    # move the button below the play/pause button
    #stopButton.move(100, 150)
    #fileBrowserButton = QtWidgets.QPushButton("Browse", window)
    #fileBrowserButton.clicked.connect(lambda: queue.put("browse"))
    # move the button above the play/pause button
    #fileBrowserButton.move(100, 50)
    #code for the play playlist button
    playPlaylistButton = QtWidgets.QPushButton("Play Playlist", window)
    playPlaylistButton.clicked.connect(lambda: queue.put("play playlist"))
    # move the button above the play/pause button
    playPlaylistButton.move(275, 0)
    # code for the clear playlist button
    clearPlaylistButton = QtWidgets.QPushButton("Clear Playlist", window)
    clearPlaylistButton.clicked.connect(lambda: playlist.clear())
    # move the button above the play/pause button
    clearPlaylistButton.move(375, 0)

    #put a message in the queue to stop the thread when the window is closed
    window.destroyed.connect(lambda: queue.put("close"))

    window.show()
    sys.exit(app.exec_())
    

def browse():
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setGeometry(50, 50, 256, 64)
    file = QFileDialog.getOpenFileName(widget, 'Open file', 'C:\Wavelength', "Audio files (*.mp3 *.wav *.flac)")
    widget.destroy()
    app.shutdown()
    if file[0] == "":
        #don't return anything
        pass
    else:
        return file[0]

queue = Queue()
audio_thread = threading.Thread(target=play_audio, args=(queue,))
gui_thread = threading.Thread(target=gui, args=(queue,))

audio_thread.start()
gui_thread.start()
