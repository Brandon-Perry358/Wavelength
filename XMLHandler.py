import os
import xml.etree.ElementTree as ET

class XMLHandler:
    # File check takes in the file type of either Theme, OnStart, or Playlist and makes sure the file exists
    def fileCheck(self, fileType):
        match fileType:
            case "Themes":
                if not os.path.isfile("./Themes.xml"):
                    f = open("Themes.xml", "w")
                    f.write("<themes>\n</themes>")
                    f.close()
            case "Playlist":
                if not os.path.isfile("./Playlists.xml"):
                    f = open("Playlists.xml", "w")
                    f.write("<playlists>\n</playlists>")
                    f.close()
            case "OnStart":
                if not os.path.isfile("./OnStart.xml"):
                    f = open("OnStart.xml", "w")
                    f.close()

    def getTracklist(self, previousSongs, currentSongs, nextSongs):
        tracklist = []
        tracklist.extend(previousSongs)
        tracklist.extend(currentSongs)
        tracklist.extend(nextSongs)
        return tracklist

    def playlistWriter(self, playlistName, tracklist):
        self.fileCheck("Playlist")

        tree = ET.parse('Playlists.xml')
        ET.indent(tree, "    ", 0)

        playlists = tree.getroot()
        newPlaylist = ET.SubElement(playlists, "playlist")
        newPlaylistName = ET.SubElement(newPlaylist, "playlistName")
        newPlaylistName.text = str(playlistName)
        newTrackList = ET.SubElement(newPlaylist, "tracks")
        trackNum = 1
        for x in tracklist:
            newTrackX = ET.SubElement(newTrackList, "track"+str(trackNum))
            newTrackX.text = str(x)
            trackNum += 1

        # If successful commit
        tree.write("Playlists.xml")
        return True

    def savePlaylist(self, playlistName, previousSongs, currentSongs, nextSongs):
        self.fileCheck("Playlist")
        # Check if playlist name already exists
        tracklist = self.getTracklist(previousSongs, currentSongs, nextSongs)
        #self.playlistWriter(playlistName, tracklist)
        return self.playlistWriter(playlistName, tracklist)

# Used to figure out structure in xml library
    def getTracks(self):
        tree = ET.parse('Playlists.xml')
        root = tree.getroot()
        # Playlist name
        for playlists in root:
            print(playlists.tag, playlists.attrib, playlists.text)
            # Track list
            for trackList in playlists:
                print(trackList.tag, trackList.attrib, trackList.text)
                # Track location
                for track in trackList:
                    print(track.text)

    def getPlaylistNames(self):
        playlistNames = []
        tree = ET.parse('Playlists.xml')
        root = tree.getroot()
        fillerClear = 0
        for playlists in root:
            for playlistName in playlists:
                if fillerClear % 2 == 0:
                    playlistNames.append(playlistName.text)
                fillerClear += 1
        #print(playlistNames)
        return playlistNames

    def loadPlaylistByName(self, playlistName):
        retPlaylist = []
        tree = ET.parse('Playlists.xml')
        root = tree.getroot()
        for playlists in root:
            for playlistInfo in playlists:
                if playlistInfo.text == playlistName:
                    #print("X")
                    print(playlistInfo.text)
                    for track in playlists[1]:
                        retPlaylist.append(track.text)

                    return retPlaylist
        return retPlaylist

    def saveTheme(self, themeName, themeArray):
        self.fileCheck("Themes")
        # TODO Check if theme exists

        # if theme does not already exist
        tree = ET.parse('Themes.xml')
        ET.indent(tree, "    ", 0)

        themes = tree.getroot()
        newThemeName = ET.SubElement(themes, "themeNames")
        newThemeName.text = str(themeName)
        newElementsList = ET.SubElement(newThemeName, "elementHexValues")
        elementNum = 1
        for x in themeArray:
            newElementX = ET.SubElement(newElementsList, "element" + str(elementNum))
            newElementX.text = str(x)
            elementNum += 1

        # If successful commit
        tree.write("Themes.xml")
        return True



