import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer  # helps play music
import time
from mutagen.mp3 import MP3

root = Tk()  # creates_a_window

statusBar = Label(root, text="Music Player Running", relief=SUNKEN, anchor=W)  # creating statusBar at bottom of window
statusBar.pack(side=BOTTOM, fill=X)

menuBar = Menu(root)  # creating a menu bar
root.config(menu=menuBar)


# creating items of menu bar

def browse_file():
    global filename
    filename = filedialog.askopenfilename()

subMenu = Menu(menuBar, tearoff=0)  # to get rid of the dotted line
menuBar.add_cascade(label="file", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo("About Music Player", "This is a music player built using the Tkinter, Pygame and "
                                                      "Mutagen libraries of python by Epsisri  Potluri, "
                                                      "RA1711003011248.")


subMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About", command=about_us)

mixer.init()  # initialize mixer

# root.geometry('500x500')  # specify the dimensions of the window
root.title("Music Player")  # change the title from Tk to Music Player
# to change icon we downloaded an ico file and pasted it in this directory
root.iconbitmap(r'music_player.ico')  # to change icon


rightFrame = Frame(root)
rightFrame.pack()

topFrame = Frame(rightFrame)
topFrame.pack()

topLabel = Label(topFrame, text='Play the music of your choice!')
topLabel.pack(pady=10)  # to show in window

lengthLabel = Label(topFrame, text="Total duration: 00:00", relief=GROOVE)  # to show length of entire song
lengthLabel.pack()



def show_details():
    topLabel['text'] = "Now Playing -" + os.path.basename(filename)
    fileData = os.path.splitext(filename)
    if fileData[1] == '.mp3':   # finding total duration of song
        audio = MP3(filename)
        totalLength = audio.info.length
    else:
        a = mixer.Sound(filename)
        totalLength = a.get_length()
    mins,secs = divmod(totalLength,60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = "Total duration -" + timeFormat


def play_music():
    try:
        paused
    except NameError:
        try:
            mixer.music.load(filename)  # load the mp3 file we are playing
            mixer.music.play()
            statusBar['text'] = "Now Playing " + os.path.basename(filename)  # os.path.basename() is to remove url
            show_details()
        except:
            tkinter.messagebox.showerror("Song not selected", "Please select a song to continue")
    else:
        mixer.music.unpause()
        statusBar['text'] = "Music Resumed"


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()  # pause the music
    statusBar['text'] = "Music has been paused"


def stop_music():
    mixer.music.stop()  # stop the music
    statusBar['text'] = "Music has stopped"


def set_vol(val):
    volume = int(val) / 100  # mixer takes values from 0 to 1
    mixer.music.set_volume(volume)


muted = FALSE


def mute_music():
    global muted
    if muted:  # un-mute music
        mixer.music.set_volume(0.75)
        volumeBut.configure(image=volumePhoto)
        scale.set(75)
        muted = FALSE
        statusBar['text'] = "Music has been un-muted"
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBut.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE
        statusBar['text'] = "Music has been muted"


middleFrame = Frame(rightFrame)  # create frame to group buttons
middleFrame.pack(padx=10, pady=10)

pausePhoto = PhotoImage(file='pause-button.png')
pauseBut = Button(middleFrame, image=pausePhoto, command=pause_music)  # creating a pause button
pauseBut.grid(row=0, column=0, padx=10)

playPhoto = PhotoImage(file='play.png')
playBut = Button(middleFrame, image=playPhoto, command=play_music)  # creating a play button
playBut.grid(row=0, column=1, padx=10)

stopPhoto = PhotoImage(file='stop.png')
stopBut = Button(middleFrame, image=stopPhoto, command=stop_music)  # creating a stop button
stopBut.grid(row=0, column=2, padx=10)

bottomFrame = Frame(rightFrame)  # create frame for volume
bottomFrame.pack(padx=10, pady=10)

mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='volume.png')
volumeBut = Button(bottomFrame, image=volumePhoto, command=mute_music)  # creating a stop button
volumeBut.grid(row=0, column=0, padx=10)

scale = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)  # creating a volume modulator
scale.set(75)  # setting a default value in the widget
mixer.music.set_volume(0.75)  # set the default volume to 75
scale.grid(row=0, column=1, padx=10)



root.mainloop()  # engage momentary window in infinite loop
