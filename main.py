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
    player.set_volume(0.5)
    while True:
        message = queue.get()
        if message == "play/pause":
            if player.playing:
                player.pause()
            elif not player.active and not player.playing:
                queue.put("play playlist")
            elif not player.playing and player.active:
                player.resume()
            else:
                pass
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
                time.sleep(0.25)
                player.play()
            if not player.active:
                #if playlist is empty, do nothing
                if len(playlist) == 0:
                    pass
                elif len(playlist) >= 1:
                    #read the playlist and place the first song in the currently_playing list
                    currently_playing.append(playlist[0])
                    #remove the first song from the playlist
                    playlist.pop(0)
                    #play the song
                    player.load_file(currently_playing[0])
                    player.play()
                else:
                    pass
        elif message == "next song":
            #if the next song is the last song in the playlist, stop the player
            if len(playlist) <= 0:
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
                time.sleep(0.25)
                player.play()
        elif message == "add to playlist":
            file = browse()
            if file == None:
                pass
            else:
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
    window.setStyleSheet("background-color: black;")
    window.setGeometry(100, 100, 775, 500)

    # make program name in corner
    wavelengthLabel = QtWidgets.QLabel(window)
    wavelengthLabel.setText("Wavelength")
    #set text color to red
    wavelengthLabel.setStyleSheet("color: #39ff14;")
    wavelengthLabel.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))
    wavelengthLabel.move(10, 0)

    # code for the add to playlist button
    addToPlaylistButton = QtWidgets.QPushButton("Browse", window)
    #set the color of the button to red
    addToPlaylistButton.setStyleSheet("background-color: #39ff14;")
    addToPlaylistButton.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))
    addToPlaylistButton.clicked.connect(lambda: queue.put("add to playlist"))
    addToPlaylistButton.move(100, 0)

    # code for creating the stop button
    stopButton = QtWidgets.QPushButton("Stop", window)
    stopButton.clicked.connect(lambda: queue.put("stop"))
    stopButton.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))
    # set the color of the button to red
    stopButton.setStyleSheet("background-color: #39ff14;")
    stopButton.move(200, 0)

    albumArt = QtWidgets.QLabel(window)
    albumPixmap = QtGui.QPixmap()
    albumArt.setPixmap(QtGui.QPixmap("WavelengthArt.png"))
    #Make a green border around the album art
    albumArt.setStyleSheet("border: 2px solid #39ff14;")
    albumArt.setScaledContents(True)
    albumArt.setGeometry(20, 40, 400, 360)

    # Show current song location
    currintPosLabel = QtWidgets.QLabel(window)
    currintPosLabel.setGeometry(450, 50, 30, 30)
    currintPosLabel.setText("0:00")
    #set text color to red
    currintPosLabel.setStyleSheet("color: #39ff14;")

    # make seek bar
    seekBar = QtWidgets.QSlider(window)
    seekBar.setOrientation(QtCore.Qt.Vertical)
    seekBar.setGeometry(450, 75, 25, 300)
    seekBar.setInvertedAppearance(True)
    #Set the color of the seek bar handle to green and show past progress as green in the bar
    seekBar.setStyleSheet("QSlider::handle:vertical {background-color: #39ff14;}")
    #seekBar.valueChanged.connect(lambda: queue.put("seek " + (seekBar.value()).__str__()))

    # show total song time
    trackLengthLabel = QtWidgets.QLabel(window)
    trackLengthLabel.setGeometry(450, 375, 30, 30)
    trackLengthLabel.setText("0:00")
    #set text color to red
    trackLengthLabel.setStyleSheet("color: #39ff14;")

    #make a list widget to display the playlist
    playlistWidget = QtWidgets.QListWidget(window)
    playlistWidget.setGeometry(500, 40, 250, 360)
    #set the color of the widget to white
    playlistWidget.setStyleSheet("background-color: white;")
    # make a label for the playlist widget above the top left corner
    playlistLabel = QtWidgets.QLabel(window)
    playlistLabel.setGeometry(500, 9, 250, 40)
    playlistLabel.setText("Playing Next:")
    # set the color of the label to neon green
    playlistLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14;")
    playlistLabel.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))

    # make song name under art
    songLabel = QtWidgets.QLabel(window)
    songLabel.setGeometry(20, 400, 400, 25)
    songLabel.setText("Wavelength")
    songLabel.setAlignment(QtCore.Qt.AlignCenter)
    #set text box color to transparent
    songLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14")
    #set text color to red
    #songLabel.setStyleSheet("color: red;")
    songLabel.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))

    # make artist name under song title
    artistLabel = QtWidgets.QLabel(window)
    artistLabel.setGeometry(20, 415, 400, 40)
    artistLabel.setText("Spack & Brandon P.")
    artistLabel.setAlignment(QtCore.Qt.AlignCenter)
    #set text box color to transparent
    artistLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14")
    #set text color to red
    #artistLabel.setStyleSheet("color: red;")
    artistLabel.setFont(QtGui.QFont("Helvetica", 11))

    # create button
    skipBackButton = QtWidgets.QPushButton("", window)
    skipBackButton.clicked.connect(lambda: queue.put("previous song"))
    skipBackButton.move(20, 450)
    skipBackButton.setGeometry(20, 450, 133, 35)
    skipBackButton.setStyleSheet("background-color: #39ff14;" + "background-image : url(skipBackButton.png); background-repeat : no-repeat; background-position : center;")
    # set the color of the button to red
    #skipBackButton.setStyleSheet("background-color: red;")

    # code for creating the button
    playPauseButton = QtWidgets.QPushButton("", window)
    playPauseButton.clicked.connect(lambda: queue.put("play/pause"))
    # move the button to the center of the window
    playPauseButton.move(125, 450)
    playPauseButton.setGeometry(153, 450, 134, 35)
    #add image to playpause button and center it
    playPauseButton.setStyleSheet("background-color: #39ff14;" + "background-image : url(playPauseButton.png); background-repeat : no-repeat; background-position : center;")
    # set the color of the button to red
    #playPauseButton.setStyleSheet("background-color: red;")

    # create button
    skipForwardButton = QtWidgets.QPushButton("", window)
    skipForwardButton.clicked.connect(lambda: queue.put("next song"))
    skipForwardButton.move(225, 450)
    skipForwardButton.setGeometry(287, 450, 133, 35)
    skipForwardButton.setStyleSheet("background-color: #39ff14;" + "background-image : url(skipForwardButton.png); background-repeat : no-repeat; background-position : center;")
    # set the color of the button to red
    #skipForwardButton.setStyleSheet("background-color: red;")
    #set the color of the button to neon green
    #skipForwardButton.setStyleSheet("background-color: #39ff14;")

    # make volume bar
    volBar = QtWidgets.QSlider(window)
    volBar.setOrientation(QtCore.Qt.Horizontal)
    volBar.setGeometry(450, 450, 300, 35)
    volBar.setInvertedAppearance(False)
    volBar.setRange(0, 100)
    volBar.setValue(50)
    #control the volume of the player
    volBar.valueChanged.connect(lambda: queue.put("volume " + (volBar.value()).__str__()))
    #set the color of the slider bar to neon green
    volBar.setStyleSheet("QSlider::groove:horizontal {border: 1px solid #bbb; background: white; height: 10px; border-radius: 4px;}" + "QSlider::sub-page:horizontal {background: #39ff14; border: 1px solid #777; height: 10px; border-radius: 4px;}" + "QSlider::add-page:horizontal {background: #fff; border: 1px solid #777; height: 10px; border-radius: 4px;}" + "QSlider::handle:horizontal {background: #39ff14; border: 1px solid #777; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}" + "QSlider::handle:horizontal:hover {background: #39ff14; border: 1px solid #444; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}" + "QSlider::sub-page:horizontal:disabled {background: #bbb; border-color: #999;}" + "QSlider::add-page:horizontal:disabled {background: #eee; border-color: #999;}" + "QSlider::handle:horizontal:disabled {background: #eee; border: 1px solid #aaa; border-radius: 4px;}")
    #make a lablel for the volume bar above the top left corner
    volLabel = QtWidgets.QLabel(window)
    volLabel.setGeometry(450, 430, 300, 25)
    volLabel.setText("Volume")
    #set the color of the label to neon green
    volLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14")
    volLabel.setFont(QtGui.QFont("Helvetica", 11, QtGui.QFont.Bold))

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: update_playlist(playlistWidget, playlist))
    timer.timeout.connect(lambda: update_song(songLabel, currently_playing))
    timer.timeout.connect(lambda: update_artist(artistLabel, currently_playing))
    timer.timeout.connect(lambda: update_art(albumArt, albumPixmap, currently_playing))
    timer.timeout.connect(lambda: update_end_time(trackLengthLabel, currently_playing))
    timer.start(500)

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
            if song_tag.title == None and song_tag.artist == None:
                playlistWidget.addItem("Unknown Title - Unknown Artist")
            elif song_tag.title == None:
                playlistWidget.addItem("Unknown Title - " + song_tag.artist)
            elif song_tag.artist == None:
                playlistWidget.addItem(song_tag.title + " - Unknown Artist")
            else:
                playlistWidget.addItem(song_tag.title + " - " + song_tag.artist)

def update_song(songLabel, currently_playing):
    if len(currently_playing) == 0:
        songLabel.setText("Wavelength")
        #pass
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0])
        if song_tag.title == None:
            songLabel.setText("Unknown Title")
        else:
            songLabel.setText(song_tag.title)

def update_artist(artistLabel, currently_playing):
    if len(currently_playing) == 0:
        artistLabel.setText("Spack & Brandon P.")
        #pass
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0])
        if song_tag.artist == None:
            artistLabel.setText("Unknown Artist")
        else:
            artistLabel.setText(song_tag.artist)

def update_art(albumArt, albumPixmap,  currently_playing):
    if len(currently_playing) == 0:
        albumArt.setPixmap(QtGui.QPixmap("WavelengthArt.png"))
        #pass
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0], image=True)
        albumPixmap.loadFromData(song_tag.get_image())
        if albumPixmap.isNull():
            albumArt.setPixmap(QtGui.QPixmap("WavelengthArt.png"))
        else:
            albumArt.setPixmap(albumPixmap)

def update_end_time(trackLengthLabel, currently_playing):
    if len(currently_playing) == 0:
        trackLengthLabel.setText("0:00")
    else:
        song_tag = tinytag.TinyTag.get(currently_playing[0])
        min = int(song_tag.duration % 3600 / 60)
        sec = int(song_tag.duration % 3600 % 60)
        if sec < 10:
            trackLengthLabel.setText(str(min) + ":0" + str(sec))
        else:
            trackLengthLabel.setText(str(min) + ":" + str(sec))

queue = Queue()
audio_thread = threading.Thread(target=play_audio, args=(queue,))
gui_thread = threading.Thread(target=gui, args=(queue,))

audio_thread.start()
gui_thread.start()