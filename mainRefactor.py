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


def play_audio(queue, mainWindow):
    player = Playback()
    player.set_volume(0.5)

    update_thread = threading.Thread(target=updateSongPos, args=(mainWindow, player))
    update_thread.start()

    while True:
        message = queue.get()
        if message == "play/pause":
            if player.playing:
                currTime = player.curr_pos
                player.pause()
                mainWindow.seekBar.setValue(int(currTime))
                min = int(player.curr_pos % 3600 / 60)
                sec = int(player.curr_pos % 3600 % 60)
                if sec < 10:
                    mainWindow.currintPosLabel.setText(str(min) + ":0" + str(sec))
                else:
                    mainWindow.currintPosLabel.setText(str(min) + ":" + str(sec))
                # print("Time left in song: " + str(int(player.duration) - int(player.curr_pos)))
            elif not player.active and not player.playing:
                queue.put("play playlist")
            elif not player.playing and player.active:
                player.resume()
            else:
                pass
        elif message == "stop":
            player.stop()
            mainWindow.playlist.clear()
            mainWindow.currently_playing.clear()
            mainWindow.previous_songs.clear()
            mainWindow.temp_playlist.clear()
        elif message == "play playlist":
            if player.active:
                #player.stop()
                # read the playlist and place the first song in the currently_playing list
                mainWindow.currently_playing.append(mainWindow.playlist[0])
                # remove the first song from the playlist
                mainWindow.playlist.pop(0)
                # play the song
                player.load_file(mainWindow.currently_playing[0])
                time.sleep(0.2)
                # print("Player duration: " + str(player.duration))
                window.seekBar.setRange(0, int(player.duration))
                # mainWindow.seekBar.setValue(0)
                mainWindow.update_song()
                mainWindow.update_artist()
                mainWindow.update_art()
                mainWindow.update_end_time()
                mainWindow.update_playlist()
                player.play()
            if not player.active:
                # if playlist is empty, do nothing
                if len(mainWindow.playlist) == 0:
                    pass
                elif len(mainWindow.playlist) >= 1:
                    # read the playlist and place the first song in the currently_playing list
                    mainWindow.currently_playing.append(mainWindow.playlist[0])
                    # remove the first song from the playlist
                    mainWindow.playlist.pop(0)
                    # play the song
                    player.load_file(mainWindow.currently_playing[0])
                    # print("Player duration: " + str(player.duration))
                    mainWindow.seekBar.setRange(0, int(player.duration))
                    mainWindow.update_song()
                    mainWindow.update_artist()
                    mainWindow.update_art()
                    mainWindow.update_end_time()
                    mainWindow.update_playlist()
                    player.play()
                else:
                    pass
        elif message == "next song":
            # if the next song is the last song in the playlist, stop the player
            if len(mainWindow.playlist) <= 0:
                player.stop()
                mainWindow.playlist.clear()
                mainWindow.currently_playing.clear()
                mainWindow.previous_songs.clear()
                mainWindow.temp_playlist.clear()
            # remove the first song from the currently_playing list
            else:
                mainWindow.previous_songs.insert(0, mainWindow.currently_playing[0])
                mainWindow.currently_playing.clear()
                #DONT REMOVE SEEK
                mainWindow.seekBar.setValue(0)
                queue.put("play playlist")
        elif message == "previous song":
            if len(mainWindow.previous_songs) <= 0:
                pass
            else:
                player.stop()
                mainWindow.temp_playlist.append(mainWindow.currently_playing[0])
                mainWindow.currently_playing.clear()
                mainWindow.currently_playing.append(mainWindow.previous_songs[0])
                mainWindow.previous_songs.pop(0)
                # place the song from the temp_playlist at the beginning of the playlist
                mainWindow.playlist.insert(0, mainWindow.temp_playlist[0])
                mainWindow.temp_playlist.pop(0)
                player.load_file(mainWindow.currently_playing[0])
                mainWindow.seekBar.setRange(0, int(player.duration))
                time.sleep(0.2)
                mainWindow.update_song()
                mainWindow.update_artist()
                mainWindow.update_art()
                mainWindow.update_end_time()
                mainWindow.update_playlist()
                player.play()
        elif message == "add to playlist":
            file = window.browse()
            if file == None:
                pass
            else:
                mainWindow.playlist.append(file)
                mainWindow.update_playlist()
        elif message.startswith("volume "):
            volume = int(message[7:])
            player.set_volume(volume / 100)
            print("Volume is: " + (volume).__str__())
        elif message.startswith("seek "):
            seek = int(message[5:])
            player.seek(seek)
            print(seek)
        elif message == "close":
            player.stop()
            break
        if (player.curr_pos == 0):
            mainWindow.update_song()
            mainWindow.update_artist()
            mainWindow.update_art()
            mainWindow.update_end_time()
            mainWindow.update_playlist()
        if (player.playing):
            mainWindow.addToPlaylistButton.setEnabled(False)
        if not player.playing:
            mainWindow.addToPlaylistButton.setEnabled(True)

        if player.curr_pos >= int(player.duration) and mainWindow.seekBar.value() >= int(player.duration):
            queue.put("next song")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

        self.playlist = []
        self.currently_playing = []
        self.previous_songs = []
        self.temp_playlist = []

        self.newCurrintPosX = 450
        self.newCurrintPosY = 50
        self.newCurrintPosH = 30
        self.newCurrintPosW = 30

        self.newSeekBarX = 450
        self.newSeekBarY = 75
        self.newSeekBarH = 25
        self.newSeekBarW = 300

        self.newTrackLengthX = 450
        self.newTrackLengthY = 375
        self.newTrackLengthH = 30
        self.newTrackLengthW = 30

        self.newPlaylistX = 500
        self.newPlaylistY = 40
        self.newPlaylistH = 250
        self.newPlaylistW = 360

        self.newPlaylistLabelX = 500
        self.newPlaylistLabelY = 9
        self.newPlaylistLabelH = 250
        self.newPlaylistLabelW = 40

        self.newVolBarX = 450
        self.newVolBarY = 450
        self.newVolBarH = 300
        self.newVolBarW = 35

        self.newVolLabelX = 450
        self.newVolLabelY = 430
        self.newVolLabelH = 300
        self.newVolLabelW = 25

        self.tradCurrintPosX = 425
        self.tradCurrintPosY = 448
        self.tradCurrintPosH = 30
        self.tradCurrintPosW = 30

        self.tradSeekBarX = 450
        self.tradSeekBarY = 450
        self.tradSeekBarH = 275
        self.tradSeekBarW = 25

        self.tradTrackLengthX = 735
        self.tradTrackLengthY = 448
        self.tradTrackLengthH = 30
        self.tradTrackLengthW = 30

        self.tradPlaylistX = 450
        self.tradPlaylistY = 40
        self.tradPlaylistH = 250
        self.tradPlaylistW = 360

        self.tradPlaylistLabelX = 450
        self.tradPlaylistLabelY = 9
        self.tradPlaylistLabelH = 250
        self.tradPlaylistLabelW = 40

        self.tradVolBarX = 720
        self.tradVolBarY = 40
        self.tradVolBarH = 35
        self.tradVolBarW = 355

        self.tradVolLabelX = 710
        self.tradVolLabelY = 10
        self.tradVolLabelH = 300
        self.tradVolLabelW = 25

        self.popup = QtWidgets.QMessageBox()
        self.popup.setText("Options")

        self.layoutNew = True

        self.setFixedSize(QtCore.QSize(775, 500))
        self.setWindowTitle("Wavelength Audio Player")
        self.setWindowIcon(QtGui.QIcon("WavelengthIcon.png"))
        self.setStyleSheet("background-color: black;")
        self.setGeometry(100, 100, 775, 500)

        # code for the add to playlist button
        self.addToPlaylistButton = QtWidgets.QPushButton("Browse", self)
        self.addToPlaylistButton.setStyleSheet("background-color: #39ff14;")
        self.addToPlaylistButton.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))
        self.addToPlaylistButton.clicked.connect(lambda: queue.put("add to playlist"))
        self.addToPlaylistButton.move(0, 0)

        # code for creating the stop button
        self.stopButton = QtWidgets.QPushButton("Stop", self)
        self.stopButton.clicked.connect(lambda: queue.put("stop"))
        self.stopButton.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))
        self.stopButton.setStyleSheet("background-color: #39ff14;")
        self.stopButton.move(100, 0)

        self.layoutSwap = QtWidgets.QPushButton("Swap Layout", self)
        self.layoutSwap.clicked.connect(self.swapLayout)
        self.layoutSwap.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))
        self.layoutSwap.setStyleSheet("background-color: #39ff14;")
        self.layoutSwap.move(200, 0)

        self.optionsButton = QtWidgets.QPushButton("Options", self)
        self.optionsButton.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))
        self.optionsButton.setStyleSheet("background-color: #39ff14;")
        self.optionsButton.clicked.connect(self.popup.show)
        self.optionsButton.move(300, 0)

        self.albumArt = QtWidgets.QLabel(self)
        self.albumPixmap = QtGui.QPixmap()
        self.albumArt.setPixmap(QtGui.QPixmap("WavelengthArt.png"))
        # Make a green border around the album art
        self.albumArt.setStyleSheet("border: 2px solid #39ff14;")
        self.albumArt.setScaledContents(True)
        self.albumArt.setGeometry(20, 40, 400, 360)

        # Show current song location
        self.currintPosLabel = QtWidgets.QLabel(self)
        self.currintPosLabel.setGeometry(450, 50, 30, 30)
        self.currintPosLabel.setText("0:00")
        self.currintPosLabel.setStyleSheet("color: #39ff14;")

        # make seek bar
        self.seekBar = QtWidgets.QSlider(self)
        # self.seekBar.setTracking(False)
        self.seekBar.setOrientation(QtCore.Qt.Vertical)
        self.seekBar.setGeometry(450, 75, 25, 300)
        self.seekBar.setInvertedAppearance(True)
        self.seekBar.setRange(0, 100)
        # print the current bar value to the console
        # print(self.seekBar.value())
        self.seekBar.valueChanged.connect(lambda: queue.put("seek " + (self.seekBar.value()).__str__()))
        # Set the color of the seek bar handle to green and show past progress as green in the bar
        self.seekBar.setStyleSheet("QSlider::handle:vertical {background-color: #39ff14;}")

        # show total song time
        self.trackLengthLabel = QtWidgets.QLabel(self)
        self.trackLengthLabel.setGeometry(450, 375, 30, 30)
        self.trackLengthLabel.setText("0:00")
        self.trackLengthLabel.setStyleSheet("color: #39ff14;")

        # make a list widget to display the playlist
        self.playlistWidget = QtWidgets.QListWidget(self)
        self.playlistWidget.setGeometry(500, 40, 250, 360)
        # set the color of the widget to white
        self.playlistWidget.setStyleSheet("background-color: white;")

        # make a label for the playlist widget above the top left corner
        self.playlistLabel = QtWidgets.QLabel(self)
        self.playlistLabel.setGeometry(500, 9, 250, 40)
        self.playlistLabel.setText("Playing Next:")
        # set the color of the label to neon green
        self.playlistLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14;")
        self.playlistLabel.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold))

        # make song name under art
        self.songLabel = QtWidgets.QLabel(self)
        self.songLabel.setGeometry(20, 400, 400, 25)
        self.songLabel.setText("Wavelength")
        self.songLabel.setAlignment(QtCore.Qt.AlignCenter)
        # set text box color to transparent
        self.songLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14")
        self.songLabel.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))

        # make artist name under song title
        self.artistLabel = QtWidgets.QLabel(self)
        self.artistLabel.setGeometry(20, 415, 400, 40)
        self.artistLabel.setText("Spack & Brandon P.")
        self.artistLabel.setAlignment(QtCore.Qt.AlignCenter)
        # set text box color to transparent
        self.artistLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14")
        self.artistLabel.setFont(QtGui.QFont("Helvetica", 11))

        # create button
        self.skipBackButton = QtWidgets.QPushButton("", self)
        self.skipBackButton.clicked.connect(lambda: queue.put("previous song"))
        self.skipBackButton.move(20, 450)
        self.skipBackButton.setGeometry(20, 450, 133, 35)
        self.skipBackButton.setStyleSheet(
            "background-color: #39ff14;" + "background-image : url(skipBackButton.png); background-repeat : no-repeat; background-position : center;")

        # code for creating the button
        self.playPauseButton = QtWidgets.QPushButton("", self)
        self.playPauseButton.clicked.connect(lambda: queue.put("play/pause"))
        # move the button to the center of the window
        self.playPauseButton.move(125, 450)
        self.playPauseButton.setGeometry(153, 450, 134, 35)
        # add image to playpause button and center it
        self.playPauseButton.setStyleSheet(
            "background-color: #39ff14;" + "background-image : url(playPauseButton.png); background-repeat : no-repeat; background-position : center;")

        # create button
        self.skipForwardButton = QtWidgets.QPushButton("", self)
        self.skipForwardButton.clicked.connect(lambda: queue.put("next song"))
        self.skipForwardButton.move(225, 450)
        self.skipForwardButton.setGeometry(287, 450, 133, 35)
        self.skipForwardButton.setStyleSheet(
            "background-color: #39ff14;" + "background-image : url(skipForwardButton.png); background-repeat : no-repeat; background-position : center;")

        # make volume bar
        self.volBar = QtWidgets.QSlider(self)
        self.volBar.setOrientation(QtCore.Qt.Horizontal)
        self.volBar.setGeometry(450, 450, 300, 35)
        self.volBar.setInvertedAppearance(False)
        self.volBar.setRange(0, 100)
        self.volBar.setValue(50)
        # control the volume of the player
        self.volBar.valueChanged.connect(lambda: queue.put("volume " + (self.volBar.value()).__str__()))
        # set the color of the slider bar to neon green
        self.volBar.setStyleSheet(
            "QSlider::groove:horizontal {border: 1px solid #bbb; background: white; height: 10px; border-radius: 4px;}" + "QSlider::sub-page:horizontal {background: #39ff14; border: 1px solid #777; height: 10px; border-radius: 4px;}" + "QSlider::add-page:horizontal {background: #fff; border: 1px solid #777; height: 10px; border-radius: 4px;}" + "QSlider::handle:horizontal {background: #39ff14; border: 1px solid #777; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}" + "QSlider::handle:horizontal:hover {background: #39ff14; border: 1px solid #444; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}" + "QSlider::sub-page:horizontal:disabled {background: #bbb; border-color: #999;}" + "QSlider::add-page:horizontal:disabled {background: #eee; border-color: #999;}" + "QSlider::handle:horizontal:disabled {background: #eee; border: 1px solid #aaa; border-radius: 4px;}")

        # make a lablel for the volume bar above the top left corner
        self.volLabel = QtWidgets.QLabel(self)
        self.volLabel.setGeometry(450, 430, 300, 25)
        self.volLabel.setText("Volume")
        # set the color of the label to neon green
        self.volLabel.setStyleSheet("background-color: transparent;" + "color: #39ff14")
        self.volLabel.setFont(QtGui.QFont("Helvetica", 11, QtGui.QFont.Bold))




        self.destroyed.connect(lambda: queue.put("close"))


    def showWindow(self):
        self.show()

    def browse(self):
        browseWidget = QtWidgets.QFileDialog(self)
        file = browseWidget.getOpenFileName(browseWidget, 'Open file', 'C:\Wavelength', "Audio files (*.mp3 *.wav *.flac)")
        browseWidget.destroy()
        if file[0] == "":
            # don't return anything
            pass
        else:
            return file[0]

    def update_song(self):
        if len(self.currently_playing) == 0:
            self.songLabel.setText("Wavelength")
            # pass
        else:
            song_tag = tinytag.TinyTag.get(self.currently_playing[0])
            if song_tag.title == None:
                self.songLabel.setText("Unknown Title")
            else:
                self.songLabel.setText(song_tag.title)

    def update_artist(self):
        if len(self.currently_playing) == 0:
            self.artistLabel.setText("Spack & Brandon P.")
            # pass
        else:
            song_tag = tinytag.TinyTag.get(self.currently_playing[0])
            if song_tag.artist == None:
                self.artistLabel.setText("Unknown Artist")
            else:
                self.artistLabel.setText(song_tag.artist)

    def update_playlist(self):
        self.playlistWidget.clear()
        for song in self.playlist:
            if song == "":
                pass
            else:
                song_tag = tinytag.TinyTag.get(song)
                if song_tag.title == None and song_tag.artist == None:
                    self.playlistWidget.addItem("Unknown Title - Unknown Artist")
                elif song_tag.title == None:
                    self.playlistWidget.addItem("Unknown Title - " + song_tag.artist)
                elif song_tag.artist == None:
                    self.playlistWidget.addItem(song_tag.title + " - Unknown Artist")
                else:
                    self.playlistWidget.addItem(song_tag.title + " - " + song_tag.artist)

    def update_art(self):
        if len(self.currently_playing) == 0:
            self.albumArt.setPixmap(QtGui.QPixmap("WavelengthArt.png"))
            # pass
        else:
            song_tag = tinytag.TinyTag.get(self.currently_playing[0], image=True)
            self.albumPixmap.loadFromData(song_tag.get_image())
            if self.albumPixmap.isNull():
                self.albumArt.setPixmap(QtGui.QPixmap("WavelengthArt.png"))
            else:
                self.albumArt.setPixmap(self.albumPixmap)

    def update_end_time(self):
        if len(self.currently_playing) == 0:
            self.trackLengthLabel.setText("0:00")
        else:
            song_tag = tinytag.TinyTag.get(self.currently_playing[0])
            # print("song tag duration: " + str(song_tag.duration))
            min = int(song_tag.duration % 3600 / 60)
            sec = int(song_tag.duration % 3600 % 60)
            if sec < 10:
                self.trackLengthLabel.setText(str(min) + ":0" + str(sec))
            else:
                self.trackLengthLabel.setText(str(min) + ":" + str(sec))


    def swapLayout(self):
        if (self.layoutNew):
            self.currintPosLabel.setGeometry(self.tradCurrintPosX, self.tradCurrintPosY, self.tradCurrintPosH, self.tradCurrintPosW)
            self.seekBar.setGeometry(self.tradSeekBarX, self.tradSeekBarY, self.tradSeekBarH, self.tradSeekBarW)
            self.seekBar.setOrientation(QtCore.Qt.Horizontal)
            self.seekBar.setInvertedAppearance(False)
            self.trackLengthLabel.setGeometry(self.tradTrackLengthX, self.tradTrackLengthY, self.tradTrackLengthH, self.tradTrackLengthW)
            self.playlistWidget.setGeometry(self.tradPlaylistX, self.tradPlaylistY, self.tradPlaylistH, self.tradPlaylistW)
            self.playlistLabel.setGeometry(self.tradPlaylistLabelX, self.tradPlaylistLabelY, self.tradPlaylistLabelH, self.tradPlaylistLabelW)
            self.volBar.setGeometry(self.tradVolBarX, self.tradVolBarY, self.tradVolBarH, self.tradVolBarW)
            self.volBar.setOrientation(QtCore.Qt.Vertical)
            self.volBar.setStyleSheet(
                "QSlider::groove:vertical {border: 1px solid #bbb; background: white; width: 10px; border-radius: 4px;}" + "QSlider::sub-page:vertical {background: #fff; border: 1px solid #777; width: 10px; border-radius: 4px;}" + "QSlider::add-page:vertical {background: #39ff14; border: 1px solid #777; width: 10px; border-radius: 4px;}" + "QSlider::handle:vertical {background: #39ff14; border: 1px solid #777; height: 13px; margin-left: -2px; margin-right: -2px; border-radius: 4px;}" + "QSlider::handle:vertical:hover {background: #39ff14; border: 1px solid #444; height: 13px; margin-left: -2px; margin-right: -2px; border-radius: 4px;}" + "QSlider::sub-page:vertical:disabled {background: #bbb; border-color: #999;}" + "QSlider::add-page:vertical:disabled {background: #eee; border-color: #999;}" + "QSlider::handle:vertical:disabled {background: #eee; border: 1px solid #aaa; border-radius: 4px;}")
            self.volLabel.setGeometry(self.tradVolLabelX, self.tradVolLabelY, self.tradVolLabelH, self.tradVolLabelW)
            self.seekBar.setStyleSheet("QSlider::handle:horizontal {background-color: #39ff14;}")
            self.layoutNew = False
        else:
            self.currintPosLabel.setGeometry(self.newCurrintPosX, self.newCurrintPosY, self.newCurrintPosH, self.newCurrintPosW)
            self.seekBar.setGeometry(self.newSeekBarX, self.newSeekBarY, self.newSeekBarH, self.newSeekBarW)
            self.seekBar.setOrientation(QtCore.Qt.Vertical)
            self.seekBar.setInvertedAppearance(True)
            self.seekBar.setStyleSheet("QSlider::handle:vertical {background-color: #39ff14;}")
            self.trackLengthLabel.setGeometry(self.newTrackLengthX, self.newTrackLengthY, self.newTrackLengthH, self.newTrackLengthW)
            self.playlistWidget.setGeometry(self.newPlaylistX, self.newPlaylistY, self.newPlaylistH, self.newPlaylistW)
            self.playlistLabel.setGeometry(self.newPlaylistLabelX, self.newPlaylistLabelY, self.newPlaylistLabelH, self.newPlaylistLabelW)
            self.volBar.setGeometry(self.newVolBarX, self.newVolBarY, self.newVolBarH, self.newVolBarW)
            self.volBar.setStyleSheet(
                "QSlider::groove:horizontal {border: 1px solid #bbb; background: white; height: 10px; border-radius: 4px;}" + "QSlider::sub-page:horizontal {background: #39ff14; border: 1px solid #777; height: 10px; border-radius: 4px;}" + "QSlider::add-page:horizontal {background: #fff; border: 1px solid #777; height: 10px; border-radius: 4px;}" + "QSlider::handle:horizontal {background: #39ff14; border: 1px solid #777; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}" + "QSlider::handle:horizontal:hover {background: #39ff14; border: 1px solid #444; width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;}" + "QSlider::sub-page:horizontal:disabled {background: #bbb; border-color: #999;}" + "QSlider::add-page:horizontal:disabled {background: #eee; border-color: #999;}" + "QSlider::handle:horizontal:disabled {background: #eee; border: 1px solid #aaa; border-radius: 4px;}")
            self.volBar.setOrientation(QtCore.Qt.Horizontal)
            self.volLabel.setGeometry(self.newVolLabelX, self.newVolLabelY, self.newVolLabelH, self.newVolLabelW)
            self.layoutNew = True

def updateSongPos(window, player):
    while True:
        if player.playing:
            min = int(player.curr_pos % 3600 / 60)
            sec = int(player.curr_pos % 3600 % 60)
            if sec < 10:
                window.currintPosLabel.setText(str(min) + ":0" + str(sec))
            else:
                window.currintPosLabel.setText(str(min) + ":" + str(sec))

            currentSeekPlace = getSeekPos(player)
            if not window.seekBar.isSliderDown():
                window.seekBar.setValue(int((currentSeekPlace)))
            else:
                pass


def getSeekPos(player):
    return (int((player.curr_pos)))

queue = Queue()
app = QtWidgets.QApplication(sys.argv)
window = MainWindow(queue)

audio_thread = threading.Thread(target=play_audio, args=(queue, window))
gui_thread = threading.Thread(target=window.show(), args=())

audio_thread.start()
gui_thread.start()

sys.exit(app.exec_())
