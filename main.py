import threading
from PyQt5 import QtWidgets, QtGui
import pygame
import sys
import time
import os
from queue import Queue
from just_playback import Playback
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PySide6.QtCore import Slot

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
        elif message == "stop":
            pygame.stop()
        elif message == "browse":
            file = browse()
            pygame.load_file(file)
            pygame.play()

def gui(queue):
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setGeometry(100, 100, 300, 300)
    # code for creating the button
    playPauseButton = QtWidgets.QPushButton("Play/Pause", window)
    playPauseButton.clicked.connect(lambda: queue.put("play/pause"))
    # move the button to the center of the window
    playPauseButton.move(100, 100)
    # code for creating the stop button
    stopButton = QtWidgets.QPushButton("Stop", window)
    stopButton.clicked.connect(lambda: queue.put("stop"))
    # move the button below the play/pause button
    stopButton.move(100, 150)
    fileBrowserButton = QtWidgets.QPushButton("Browse", window)
    fileBrowserButton.clicked.connect(lambda: queue.put("browse"))
    # move the button above the play/pause button
    fileBrowserButton.move(100, 50)

    window.show()
    sys.exit(app.exec_())

def browse():
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setGeometry(50, 50, 256, 64)
    file = QFileDialog.getOpenFileName(widget, 'Open file', 'C:\Wavelength', "Audio files (*.mp3 *.wav *.flac)")
    widget.destroy()
    app.shutdown()
    return file[0]

queue = Queue()
audio_thread = threading.Thread(target=play_audio, args=(queue,))
gui_thread = threading.Thread(target=gui, args=(queue,))

audio_thread.start()
gui_thread.start()
