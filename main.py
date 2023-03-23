import threading
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import time
import os
from queue import Queue
from just_playback import Playback
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QListWidget
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPixmap, QFont
from tinytag import tinytag

playlist = []
currently_playing = []
previous_songs = []
temp_playlist = []

def play_audio(queue):
    # code for initializing and playing audio
    player = Playback()
    player.set_volume(1)
    while True:
        message = queue.get()
        if message == "play/pause":
            if player.playing:
                player.pause()
            elif not player.active and not player.playing:
                queue.put("play playlist")
            elif not player.playing and player.active:
                player.resume()
        elif message == "stop":
            player.stop()
            playlist.clear()
            currently_playing.clear()
        elif message == "play playlist":
            if player.active:
                player.stop()
                #read the playlist and place the first song in the currently_playing list
                currently_playing.append(playlist[0])
                #remove the first song from the playlist
                playlist.pop(0)
                #play the song
                player.load_file(currently_playing[0])
                player.play()
            if not player.active:
                #read the playlist and place the first song in the currently_playing list
                currently_playing.append(playlist[0])
                #remove the first song from the playlist
                playlist.pop(0)
                #play the song
                player.load_file(currently_playing[0])
                player.play()
        elif message == "next song":
            #if the next song is the last song in the playlist, stop the player
            if len(playlist) == 0:
                player.stop()
                playlist.clear()
                currently_playing.clear()
                previous_songs.clear()
                temp_playlist.clear()
            #remove the first song from the currently_playing list
            else:
                previous_songs.insert(0, currently_playing[0])
                currently_playing.clear()
                queue.put("play playlist")
        elif message == "previous song":
            if len(previous_songs) == 0:
                pass
            else:
                player.stop()
                temp_playlist.append(currently_playing[0])
                currently_playing.clear()
                currently_playing.append(previous_songs[0])
                previous_songs.pop(0)
                #place the song from the temp_playlist at the beginning of the playlist
                playlist.insert(0, temp_playlist[0])
                temp_playlist.pop(0)
                player.load_file(currently_playing[0])
                player.play()
        elif message == "add to playlist":
            file = browse()
            playlist.append(file)
        elif message.startswith("volume "):
            volume = int(message[7:])
            player.set_volume(volume / 100)
            print("Volume is: " + (volume).__str__())
        elif message == "close":
            player.stop()
            break

def gui(queue):
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setFixedSize(775, 500)
    window.setWindowTitle("Wavelength Audio Player")
    window.setWindowIcon(QtGui.QIcon("WavelengthIcon.png"))
    #change background color to aqua blue
    #window.setStyleSheet("background-color: #00FFFF;")
    window.setGeometry(100, 100, 775, 500)

    # make program name in corner
    wavelengthLabel = QtWidgets.QLabel(window)
    wavelengthLabel.setText("Wavelength")
    wavelengthLabel.move(10, 0)

    albumArt = QtWidgets.QLabel(window)
    albumPixmap = QtGui.QPixmap()
    albumArt.setPixmap(QtGui.QPixmap("WavelengthArt.png"))
    albumArt.setScaledContents(True)
    albumArt.setGeometry(20, 40, 400, 360)

    #make a list widget to display the playlist
    playlistWidget = QtWidgets.QListWidget(window)
    playlistWidget.setGeometry(500, 40, 250, 360)
    #Display the contents of the playlist in the list widget
        

    # create button
    skipBackButton = QtWidgets.QPushButton("", window)
    skipBackButton.clicked.connect(lambda: queue.put("previous song"))
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
    skipForwardButton.clicked.connect(lambda: queue.put("next song"))
    skipForwardButton.move(225, 450)
    skipForwardButton.setGeometry(287, 450, 133, 35)
    skipForwardButton.setStyleSheet("background-image : url(skipForwardButton.png); background-repeat : no-repeat; background-position : center;")
    # code for function
    # TODO

    # make song name under art
    songLabel = QtWidgets.QLabel(window)
    songLabel.setGeometry(25, 400, 400, 25)
    songLabel.setText("Wavelength")
    songLabel.setAlignment(QtCore.Qt.AlignCenter)
    songLabel.setFont(QtGui.QFont("Comic Sans MS", 17, QtGui.QFont.Bold))
    #songLabel.move(125, 375)

    # make artist name under song title
    artistLabel = QtWidgets.QLabel(window)
    artistLabel.setGeometry(25, 415, 400, 40)
    artistLabel.setText("Spack & Brandon P.")
    artistLabel.setAlignment(QtCore.Qt.AlignCenter)
    artistLabel.setFont(QtGui.QFont("Comic Sans MS", 11))
    #artistLabel.move(125, 390)


    # code for creating the stop button
    stopButton = QtWidgets.QPushButton("Stop", window)
    stopButton.clicked.connect(lambda: queue.put("stop"))
    # move the button below the play/pause button
    stopButton.move(175, 0)

    # Show current song location
    currintPosLabel = QtWidgets.QLabel(window)
    currintPosLabel.setGeometry(450, 50, 30, 30)
    currintPosLabel.setText("0:00")

    # make seek bar
    seekBar = QtWidgets.QSlider(window)
    seekBar.setOrientation(QtCore.Qt.Vertical)
    seekBar.setGeometry(450, 75, 25, 300)
    seekBar.setInvertedAppearance(True)

    # show total song time
    trackLengthLabel = QtWidgets.QLabel(window)
    trackLengthLabel.setGeometry(450, 375, 30, 30)
    trackLengthLabel.setText("1:34")

    # make volume bar
    volBar = QtWidgets.QSlider(window)
    volBar.setOrientation(QtCore.Qt.Horizontal)
    volBar.setGeometry(450, 450, 300, 35)
    volBar.setInvertedAppearance(False)
    volBar.setRange(0, 100)
    volBar.setValue(100)
    #control the volume of the player
    volBar.valueChanged.connect(lambda: queue.put("volume " + (volBar.value()).__str__()))

    # code for the add to playlist button
    addToPlaylistButton = QtWidgets.QPushButton("Browse", window)
    addToPlaylistButton.clicked.connect(lambda: queue.put("add to playlist"))
    addToPlaylistButton.move(75, 0)

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: update_playlist(playlistWidget, playlist))
    timer.timeout.connect(lambda: update_song(songLabel, currently_playing))
    timer.timeout.connect(lambda: update_artist(artistLabel, currently_playing))
    timer.timeout.connect(lambda: update_art(albumArt, albumPixmap, currently_playing))
    timer.timeout.connect(lambda: update_end_time(trackLengthLabel, currently_playing))
    timer.start(100)

    #every 100ms, update the song name
    #timer2 = QtCore.QTimer()
    #timer2.timeout.connect(lambda: update_song_name(songLabel, artistLabel, queue))
    #timer2.start(100)

    #every 100ms, call the update_playback function
    

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
    
def update_playlist(playlistWidget, playlist):
    playlistWidget.clear()
    for song in playlist:
        if song == "":
            pass
        else:
            song_tag = tinytag.TinyTag.get(song)
            playlistWidget.addItem(song_tag.title + " - " + song_tag.artist)

def update_song(songLabel, currently_playing):
    if len(currently_playing) == 0:
        pass
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0])
        songLabel.setText(song_tag.title)

def update_artist(artistLabel, currently_playing):
    if len(currently_playing) == 0:
        pass
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0])
        artistLabel.setText(song_tag.artist)

def update_art(albumArt, albumPixmap,  currently_playing):
    if len(currently_playing) == 0:
        pass
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0], image=True)
        albumPixmap.loadFromData(song_tag.get_image())
        albumArt.setPixmap(albumPixmap)

def update_end_time(trackLengthLabel, currently_playing):
    if len(currently_playing) == 0:
        pass
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0])
        min = int(song_tag.duration % 3600 / 60)
        sec = int(song_tag.duration % 3600 % 60)
        trackLengthLabel.setText(str(min) + ":" + str(sec))


queue = Queue()
audio_thread = threading.Thread(target=play_audio, args=(queue,))
gui_thread = threading.Thread(target=gui, args=(queue,))

audio_thread.start()
gui_thread.start()