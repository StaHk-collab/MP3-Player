from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

# initialising pygame
pygame.mixer.init()

# function for getting son time
def play_time():
    # check to see if song is stopped
    if stopped:
        return 
    # grab current song time
    current_time = pygame.mixer.music.get_pos( )/1000 # returns in miliseconds
    # convert song time to time format
    converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))
    # reconstruct song with directory structure
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio/{song}.mp3'
    # find current song length
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length # my_label.config(text=song_length) // to check what time format it is
    # convert to time format
    converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
    # check to see if song is over
    if int(song_slider.get()) == int(song_length):
        stop()

    elif paused:
        # check to see if paused, if so -> pass
        pass
    else:
        # move slider along 1 sec at a time
        next_time = int(song_slider.get()) + 1
        # output new time value to slider, and to length of song
        song_slider.config(to=song_length, value=next_time)
        # convert slider position to time format
        converted_current_time = time.strftime('%M:%S',time.gmtime(int(song_slider.get())))
        # output slider
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}    ')

    # add curerent time to status bar
    if current_time >= 1:
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}    ')
    # create loop to check time every second
    status_bar.after(1000, play_time)

# function to add one song
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))
    # strip out dir structure 
    song = song.replace("C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio/", "")
    song = song.replace(".mp3", "")
    playlist_box.insert(END, song)
# function to add many songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))
    # loop through song list and replace dir name 
    for song in songs:
        # strip out dir structure 
        song = song.replace("C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio/", "")
        song = song.replace(".mp3", "")
        playlist_box.insert(END, song)
# del highlighted song from playlist         
def delete_song():
    playlist_box.delete(ANCHOR)
# del all songs 
def delete_songs():
    playlist_box.delete(0, END)

# play function
def play():
    # set stop to false since a song is playing
    global stopped
    stopped = False
    # reconstruct song directory
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio/{song}.mp3'
    # load song with pygame mixer
    pygame.mixer.music.load(song)
    # play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    # get song time
    play_time()

# create stopped variable
global stopped 
stopped = False
def stop():
    # stop song
    pygame.mixer.music.stop()
    # clear playlist bar
    playlist_box.selection_clear(ACTIVE)
    status_bar.config(text='')

    # set our slider to zero
    song_slider.config(value=0)
    
    # set stop variable to 
    global stopped
    stopped = True

# create paused variable
global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
        
    else:
        pygame.mixer.music.pause()
        paused = True
    
def forward():
    # reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    # get current song no.
    next_one=playlist_box.curselection()
    # my_label.config(text=next_one) -> to check what no. r we getting
    next_one = next_one[0] + 1 # next_one is a tuple (add one to the current song no. Tuple/list)
    # grab song title from playlist
    song = playlist_box.get(next_one)
    # add dir structure to get the song
    song = f'C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio/{song}.mp3'
    # load song with pygame mixer
    pygame.mixer.music.load(song)
    # play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    # clear active bar in playlist
    playlist_box.selection_clear(0, END)
    # move active bar to next song
    playlist_box.activate(next_one)
    # set the active bar to next song
    playlist_box.selection_set(next_one, last=None)

def back():
    # reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    # get current song no.
    next_one=playlist_box.curselection()
    # my_label.config(text=next_one) -> to check what no. r we getting
    next_one = next_one[0] - 1 # next_one is a tuple (add one to the current song no. Tuple/list)
    # grab song title from playlist
    song = playlist_box.get(next_one)
    # add dir structure to get the song
    song = f'C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio/{song}.mp3'
    # load song with pygame mixer
    pygame.mixer.music.load(song)
    # play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    # clear active bar in playlist
    playlist_box.selection_clear(0, END)
    # move active bar to next song
    playlist_box.activate(next_one)
    # set the active bar to next song
    playlist_box.selection_set(next_one, last=None)

# volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

# slider function for song positioning
def slide(x):
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/WELCOME/Documents/PROJECTS/Python Projects/MP3 player/audio/{song}.mp3'
    # load song with pygame mixer
    pygame.mixer.music.load(song)
    # play song with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())

# create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# playlist box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground='black')
playlist_box.grid(row=0, column=0)

# create volume slider frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

# create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=125, value=0.5, command=volume)
volume_slider.pack(pady=10)

# song slider
song_slider=ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

# define button images
back_btn_img = PhotoImage(file='images\\back50.png')
forward_btn_img = PhotoImage(file='images\\forward50.png')
play_btn_img = PhotoImage(file='images\\play50.png')
pause_btn_img = PhotoImage(file='images\\pause50.png')
stop_btn_img =PhotoImage(file='images\\stop50.png')

# button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# buttons
back_button = Button(control_frame, image =back_btn_img, borderwidth =0, command=back)
forward_button = Button(control_frame, image =forward_btn_img, borderwidth =0, command=forward)
play_button = Button(control_frame, image =play_btn_img, borderwidth =0, command=play)
pause_button = Button(control_frame, image =pause_btn_img, borderwidth =0, command=lambda: pause(paused))
stop_button = Button(control_frame, image =stop_btn_img, borderwidth =0, command=stop)

back_button.grid(row=0, column=0,padx=10)
forward_button.grid(row=0, column=1,padx=10)
play_button.grid(row=0, column=2,padx=10)
pause_button.grid(row=0, column=3,padx=10)
stop_button.grid(row=0, column=4,padx=10)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create Add song menu dropdown
add_song_menu = Menu(my_menu, tearoff=0) # tearoff=0 removes the dotted line from dropdown
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
# Add one song to playlist
add_song_menu.add_command(label="Add one song to Playlist", command =add_song)
# Add many songs to Playlist
add_song_menu.add_command(label="Add Many songs to Playlist", command =add_many_songs)

# delete song menu
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist", command=delete_songs)

# status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)




# temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)




root.mainloop()