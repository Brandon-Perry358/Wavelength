from PyQt5 import QtWidgets, QtGui, QtCore


class ThemeDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change and save theme")
        self.setGeometry(100, 100, 300, 500)

        self.labelLabel = QtWidgets.QLabel(self)
        self.labelLabel.setGeometry(5, 0, 100, 25)
        self.labelLabel.setText("Element")

        self.hexLabel = QtWidgets.QLabel(self)
        self.hexLabel.setGeometry(100, 0, 100, 25)
        self.hexLabel.setText("Current Hex Value")

        self.newLabel = QtWidgets.QLabel(self)
        self.newLabel.setGeometry(200, 0, 100, 25)
        self.newLabel.setText("New Hex Value")

        self.curBackgroundColorLabel = QtWidgets.QLabel(self)
        self.curBackgroundColorLabel.setGeometry(5, 30, 100, 25)
        self.curBackgroundColorLabel.setText("Background")

        self.curBackgroundColor = QtWidgets.QLabel(self)
        self.curBackgroundColor.setGeometry(100, 30, 100, 25)

        self.newBackgroundColor = QtWidgets.QLineEdit(self)
        self.newBackgroundColor.setGeometry(200, 30, 80, 25)

        self.curButtonColorLabel = QtWidgets.QLabel(self)
        self.curButtonColorLabel.setGeometry(5, 60, 100, 25)
        self.curButtonColorLabel.setText("Buttons color")

        self.curButtonColor = QtWidgets.QLabel(self)
        self.curButtonColor.setGeometry(100, 60, 100, 25)

        self.newButtonColor = QtWidgets.QLineEdit(self)
        self.newButtonColor.setGeometry(200, 60, 80, 25)

        self.curButtonTextLabel = QtWidgets.QLabel(self)
        self.curButtonTextLabel.setGeometry(5, 90, 100, 25)
        self.curButtonTextLabel.setText("Button Text")

        self.curButtonTextColor = QtWidgets.QLabel(self)
        self.curButtonTextColor.setGeometry(100, 90, 100, 25)

        self.newButtonTextColor = QtWidgets.QLineEdit(self)
        self.newButtonTextColor.setGeometry(200, 90, 80, 25)

        self.curArtBorderColorLabel = QtWidgets.QLabel(self)
        self.curArtBorderColorLabel.setGeometry(5, 120, 100, 25)
        self.curArtBorderColorLabel.setText("Art Border")

        self.curArtBorderColor = QtWidgets.QLabel(self)
        self.curArtBorderColor.setGeometry(100, 120, 100, 25)

        self.newArtBorderColor = QtWidgets.QLineEdit(self)
        self.newArtBorderColor.setGeometry(200, 120, 80, 25)

        self.PosLabel = QtWidgets.QLabel(self)
        self.PosLabel.setGeometry(5, 150, 100, 25)
        self.PosLabel.setText("Current Position")

        self.curPosLabelColor = QtWidgets.QLabel(self)
        self.curPosLabelColor.setGeometry(100, 150, 100, 25)

        self.newPosColor = QtWidgets.QLineEdit(self)
        self.newPosColor.setGeometry(200, 150, 80, 25)

        self.seekHandleLabel = QtWidgets.QLabel(self)
        self.seekHandleLabel.setGeometry(5, 180, 100, 25)
        self.seekHandleLabel.setText("Seek Handle")

        self.curSeekHandleColor = QtWidgets.QLabel(self)
        self.curSeekHandleColor.setGeometry(100, 180, 100, 25)

        self.newSeekHandleColor = QtWidgets.QLineEdit(self)
        self.newSeekHandleColor.setGeometry(200, 180, 80, 25)

        self.trackLengthLabel = QtWidgets.QLabel(self)
        self.trackLengthLabel.setGeometry(5, 210, 100, 25)
        self.trackLengthLabel.setText("Track Length")

        self.curTrackLengthColor = QtWidgets.QLabel(self)
        self.curTrackLengthColor.setGeometry(100, 210, 100, 25)

        self.newTrackLengthColor = QtWidgets.QLineEdit(self)
        self.newTrackLengthColor.setGeometry(200, 210, 80, 25)

        self.artistLabel = QtWidgets.QLabel(self)
        self.artistLabel.setGeometry(5, 240, 100, 25)
        self.artistLabel.setText("Artist Text")

        self.curArtistColor = QtWidgets.QLabel(self)
        self.curArtistColor.setGeometry(100, 240, 100, 25)

        self.newArtistColor = QtWidgets.QLineEdit(self)
        self.newArtistColor.setGeometry(200, 240, 80, 25)

        self.trackLabel = QtWidgets.QLabel(self)
        self.trackLabel.setGeometry(5, 270, 100, 25)
        self.trackLabel.setText("Track Text")

        self.curTrackColor = QtWidgets.QLabel(self)
        self.curTrackColor.setGeometry(100, 270, 100, 25)

        self.newTrackColor = QtWidgets.QLineEdit(self)
        self.newTrackColor.setGeometry(200, 270, 80, 25)

        self.volumeBarLabel = QtWidgets.QLabel(self)
        self.volumeBarLabel.setGeometry(5, 300, 100, 25)
        self.volumeBarLabel.setText("Volume Bar")

        self.curVolumeBarColor = QtWidgets.QLabel(self)
        self.curVolumeBarColor.setGeometry(100, 300, 100, 25)

        self.newVolumeBarColor = QtWidgets.QLineEdit(self)
        self.newVolumeBarColor.setGeometry(200, 300, 80, 25)

        self.volumeHandleLabel = QtWidgets.QLabel(self)
        self.volumeHandleLabel.setGeometry(5, 330, 100, 25)
        self.volumeHandleLabel.setText("Volume Handle")

        self.curVolumeHandleColor = QtWidgets.QLabel(self)
        self.curVolumeHandleColor.setGeometry(100, 330, 100, 25)

        self.newVolumeHandleColor = QtWidgets.QLineEdit(self)
        self.newVolumeHandleColor.setGeometry(200, 330, 80, 25)

        self.volumeTextLabel = QtWidgets.QLabel(self)
        self.volumeTextLabel.setGeometry(5, 360, 100, 25)
        self.volumeTextLabel.setText("Volume Text")

        self.curVolumeTextColor = QtWidgets.QLabel(self)
        self.curVolumeTextColor.setGeometry(100, 360, 100, 25)

        self.newVolumeTextColor = QtWidgets.QLineEdit(self)
        self.newVolumeTextColor.setGeometry(200, 360, 80, 25)

        self.playlistTextLabel = QtWidgets.QLabel(self)
        self.playlistTextLabel.setGeometry(5, 390, 100, 25)
        self.playlistTextLabel.setText("Playlist Label")

        self.curPlaylistTextColor = QtWidgets.QLabel(self)
        self.curPlaylistTextColor.setGeometry(100, 390, 100, 25)

        self.newPlaylistTextColor = QtWidgets.QLineEdit(self)
        self.newPlaylistTextColor.setGeometry(200, 390, 80, 25)

        self.applyButton = QtWidgets.QPushButton("Apply", self)
        self.applyButton.setGeometry(0, 435, 95, 50)

        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setGeometry(100, 435, 95, 50)

        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.cancelButton.setGeometry(200, 435, 95, 50)
        self.cancelButton.clicked.connect(self.cancel)


    def getResponse(self):
        newColorList = [self.newBackgroundColor.text(),
                        self.newButtonColor.text(),
                        self.newButtonTextColor.text(),
                        self.newArtBorderColor.text(),
                        self.newPosColor.text(),
                        self.newSeekHandleColor.text(),
                        self.newTrackLengthColor.text(),
                        self.newArtistColor.text(),
                        self.newTrackColor.text(),
                        self.newVolumeBarColor.text(),
                        self.newVolumeHandleColor.text(),
                        self.newVolumeTextColor.text(),
                        self.newPlaylistTextColor.text()]
        return newColorList


    def cancel(self):
        self.close()



