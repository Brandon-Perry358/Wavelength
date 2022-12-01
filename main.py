from just_playback import Playback
import keyboard
import time
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import Slot

is_running = True

@Slot()
def play():
    print("Play button clicked, Rock on!")
    playback = Playback()
    playback.load_file('music/03 - The Son of Flynn.flac')
    playback.set_volume(1)
    playback.play()
    time.sleep(100)
    #while playback.active:
        #playback.resume()

def pause():
    print("Pause button clicked, Rock off!")
    #while playback.active:
        #playback.pause()
    

def window():
    #print('Welcome to the Wavelength Music Player! Press "q" to quit.')
    
    app = QApplication(sys.argv)
    widget = QWidget()

    playButton = QPushButton(widget)
    playButton.setText("Play")
    playButton.move(32, 16)
    playButton.clicked.connect(play)  # put play function name hear

    pauseButton = QPushButton(widget)
    pauseButton.setText("Pause")
    pauseButton.move(128, 16)
    pauseButton.clicked.connect(pause)  # put play function name hear

    widget.setGeometry(50, 50, 256, 64)
    widget.setWindowTitle("PyQt5 Button Click Example")
    widget.show()
    sys.exit(app.exec())

"""def main():
    print('Welcome to the Wavelength Music Player!')
    print('Please select an option:')
    print('1. Play a song')
    print('2. Exit Program')
    if input('Enter your choice: ') == '1':
        playback = Playback() # creates an object for managing playback of a single audio file
        playback.load_file('music/03 - The Son of Flynn.flac') # loads the audio file
        #if the p key is pressed, play the audio file
        playback.set_volume(1) # sets the volume to 50%
        playback.play()
        playback.loop_at_end(False)
        playback.pause()
        if input('Song Loaded. Press 1 to play the song: ') == '1':
            playback.play()
        while playback.active:
            playing = playback.playing
            if keyboard.is_pressed('2'):
                if playing:
                    #playing = False
                    playback.pause()
                    print('Song paused at ' + str(playback.curr_pos) + ' seconds. Press 1 to resume.')
            if keyboard.is_pressed('1'):
                if not playing:
                    #playing = True
                    playback.resume()
            if keyboard.is_pressed('3'):
                playback.seek(-5)
                print('Skipped to: ' + str(playback.curr_pos))
                time.sleep(0.5)
            if keyboard.is_pressed('4'):
                playback.seek(5)
                print('Skipped to: ' + str(playback.curr_pos))
                time.sleep(0.5)
            if keyboard.is_pressed('5'):
                print('Song ended at ' + str(playback.curr_pos) + ' seconds.')
                playback.stop()
                exit()
            
            # sets the audio file to not loop at the end

            #print(playback.curr_pos)

            #if (playback.active):
                #print('active')
            #time.sleep(300)

    else:
        exit()"""

def exit():
    print('Thank you for using the Wavelength Music Player! Goodbye!')

if __name__ == '__main__':
    window()
    #main()