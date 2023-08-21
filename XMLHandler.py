import os
import xml.etree.ElementTree as ET

class XMLHandler:
    # File check takes in the file type of either Theme, OnStart, or Playlist and makes sure the file exists
    def fileCheck(self, fileType):
        match fileType:
            case "Themes":
                if not os.path.isfile("./Themes.xml"):
                    f = open("Themes.xml", "w")
                    f.write("<themeRoot>\n</themeRoot>")
                    f.close()
            case "Playlist":
                if not os.path.isfile("./Playlists.xml"):
                    f = open("Playlists.xml", "w")
                    f.write("<playlists>\n</playlists>")
                    f.close()
            case "Startup":
                if not os.path.isfile("./Startup.xml"):
                    self.fileCheck("Themes")
                    self.fileCheck("Playlist")
                    f = open("Startup.xml", "w")
                    f.write("<startupRoot>\n   <playlist>None</playlist>\n   <theme>None</theme>\n</startupRoot>")
                    f.close()

    def getTracklist(self, previousSongs, currentSongs, nextSongs):
        tracklist = []
        tracklist.extend(previousSongs)
        tracklist.extend(currentSongs)
        tracklist.extend(nextSongs)
        return tracklist

    def playlistWriter(self, playlistName, tracklist):
        self.fileCheck("Playlist")
        if self.nameValidation("Playlist", playlistName):

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
        else:
            return False

    def savePlaylist(self, playlistName, previousSongs, currentSongs, nextSongs):
        self.fileCheck("Playlist")
        tracklist = self.getTracklist(previousSongs, currentSongs, nextSongs)
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
        if self.nameValidation("Theme", themeName):
            tree = ET.parse('Themes.xml')
            ET.indent(tree, "    ", 0)

            themes = tree.getroot()
            newThemes = ET.SubElement(themes, "Themes")
            newThemeName = ET.SubElement(newThemes, "themeName")
            newThemeName.text = str(themeName)
            newElementsList = ET.SubElement(newThemes, "elementHexValues")
            elementNum = 1
            for x in themeArray:
                newElementX = ET.SubElement(newElementsList, "element" + str(elementNum))
                newElementX.text = str(x)
                elementNum += 1

            # If successful commit
            tree.write("Themes.xml")
            return True
        else:
            return False

    def getThemeNames(self):
        retNames = []
        tree = ET.parse("Themes.xml")
        fillerClear = 0
        themeRoot = tree.getroot()
        for themes in themeRoot:
            for themeNames in themes:
                if fillerClear % 2 == 0:
                    retNames.append(themeNames.text)
                fillerClear += 1
        return retNames

    def loadThemeByName(self, themeName):
        colorList = []
        tree = ET.parse("Themes.xml")
        themeRoot = tree.getroot()
        for themes in themeRoot:
            for themeNames in themes:
                if themeNames.text == themeName:
                    for colors in themes[1]:
                        colorList.append(colors.text)

        return colorList


    def changeStartupPlaylist(self, playlistName):
        self.fileCheck("Startup")

        tree = ET.parse('Startup.xml')
        ET.indent(tree,  "    ", 0)

        startupRoot = tree.getroot()
        startupRoot[0].text = playlistName.text()
        tree.write("Startup.xml")
        # print(startupRoot[0].text)
        # print(startupRoot[0].tag)
        # print(startupRoot[0].attrib)

    def changeStartupTheme(self, themeName):
        self.fileCheck("Startup")

        tree = ET.parse('Startup.xml')
        ET.indent(tree,  "    ", 0)

        startupRoot = tree.getroot()
        startupRoot[1].text = themeName.text()
        tree.write("Startup.xml")
        # print(startupRoot[1].text)
        # print(startupRoot[1].tag)
        # print(startupRoot[1].attrib)

    def readStartup(self):
        self.fileCheck("Startup")

        retData = []

        tree = ET.parse('Startup.xml')
        ET.indent(tree, "    ", 0)

        startupRoot = tree.getroot()
        retData.append(startupRoot[0].text)
        retData.append(startupRoot[1].text)

        return retData

    def nameValidation(self, nameType, name):
        if nameType == "Theme":
            themeList = self.getThemeNames()
            for x in themeList:
                if name == x:
                    return False
            return True
        elif nameType == "Playlist":
            playlistList = self.getPlaylistNames()
            for x in playlistList:
                if name == x:
                    return False
            return True
