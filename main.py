from just_playback import Playback

selection = 1

def main():
    playback = Playback() # creates an object for managing playback of a single audio file
    playback.load_file('1.mp3') # loads the audio file
    #if the p key is pressed, play the audio file
    playback.set_volume(1) # sets the volume to 50%
    playback.play()
    playback.loop_at_end(True)

    print(playback.curr_pos)

    if (playback.active):
        print('active')

if __name__ == '__main__':
    main()