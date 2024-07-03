from tkinter import *

import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

wnd = Tk()
wnd.title("Georgi Horozov MP3 Player")
wnd.geometry("450x550")
wnd_icon = PhotoImage(file="logo/head_phones.png")
wnd.iconphoto(False, wnd_icon)

song_box = Listbox(wnd, width=65, height=18, bg="#333333", fg="white")
song_box.pack(pady=20)

pygame.mixer.init()


song_length = 0


def duration():
    current_time = pygame.mixer.music.get_pos() / 1000

    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))

    song = song_box.get(ACTIVE)
    song = f"C:/Users/Admin/PycharmProjects/MP3_player/audio/{song}.mp3"
    song_mutagen = MP3(song)

    global song_length
    song_length = song_mutagen.info.length

    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))

    time_field.config(text=f"Elapsed time: {converted_current_time} of {converted_song_length}")

    music_slider.config(value=int(current_time))

    time_field.after(1000, duration)


def add_one_song():
    song = filedialog.askopenfilename(initialdir="audio", title="Choose a song from the list",
                                      filetypes=(("mp3 Files", "*.mp3"),))
    song = song.replace("C:/Users/Admin/PycharmProjects/MP3_player/audio", '').lstrip('/')
    song = song.replace(".mp3", "")
    song_box.insert(END, song)


def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="audio", title="Choose a song from the list", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace("C:/Users/Admin/PycharmProjects/MP3_player/audio", '').lstrip('/')
        song = song.replace(".mp3", "")
        song_box.insert(END, song)


def delete_one_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_all_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()


def play():
    song = song_box.get(ACTIVE)
    song = f"C:/Users/Admin/PycharmProjects/MP3_player/audio/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    duration()

    slider_position = int(song_length)
    music_slider.config(to=slider_position, value=0)


def stop():
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)

    time_field.config(text="")


paused = False


def pause():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def next_song():
    current_song = song_box.curselection()

    next_one = current_song[0] + 1

    if next_one >= song_box.size():
        next_one = 0

    next_song_name = song_box.get(next_one)

    song = f"C:/Users/Admin/PycharmProjects/MP3_player/audio/{next_song_name}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(current_song)

    song_box.activate(next_one)

    song_box.selection_set(next_one)


def previous_song():
    current_song = song_box.curselection()

    previous_one = current_song[0] - 1

    if previous_one < 0:
        previous_one = song_box.size() - 1

    previous_song_name = song_box.get(previous_one)

    song = f"C:/Users/Admin/PycharmProjects/MP3_player/audio/{previous_song_name}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(current_song)

    song_box.activate(previous_one)

    song_box.selection_set(previous_one)


def slide(x):
    slider_label.config(text=f"{int(music_slider.get())} of {int(song_length)}")


play_btn_img = PhotoImage(file="buttons/btn_play.png")
stop_btn_img = PhotoImage(file="buttons/btn_stop.png")
forward_btn_img = PhotoImage(file="buttons/btn_forward.png")
back_btn_img = PhotoImage(file="buttons/btn_back.png")
pause_btn_img = PhotoImage(file="buttons/btn_pause.png")

buttons_frame = Frame(wnd)
buttons_frame.pack()

play_button = Button(buttons_frame, image=play_btn_img, bd=0, command=play)
stop_button = Button(buttons_frame, image=stop_btn_img, bd=0, command=stop)
forward_button = Button(buttons_frame, image=forward_btn_img, bd=0, command=next_song)
back_button = Button(buttons_frame, image=back_btn_img, bd=0, command=previous_song)
pause_button = Button(buttons_frame, image=pause_btn_img, bd=0, command=pause)

forward_button.grid(row=0, column=0)
play_button.grid(row=0, column=1)
pause_button.grid(row=0, column=2)
stop_button.grid(row=0, column=3)
back_button.grid(row=0, column=4)

main_menu = Menu(wnd)
wnd.config(menu=main_menu)
add_song_menu = Menu(main_menu)
main_menu.add_cascade(label="Add Song", menu=add_song_menu)
add_song_menu.add_command(label="Add Only One Song", command=add_one_song)
add_song_menu.add_command(label="Add Many Songs", command=add_many_songs)


delete_song_menu = Menu(main_menu)
main_menu.add_cascade(label="Delete Song", menu=delete_song_menu)
delete_song_menu.add_command(label="Delete One Song", command=delete_one_song)
delete_song_menu.add_command(label="Delete All Songs", command=delete_all_songs)

time_field = Label(wnd, text="", bd=1, anchor=W)
time_field.pack(fill=X, side=BOTTOM)


music_slider = ttk.Scale(wnd, from_=0, to=100, orient=HORIZONTAL, value=0, length=360, command=slide)
music_slider.pack(pady=30)

slider_label = Label(wnd, text="0")
slider_label.pack(pady=5)

wnd.mainloop()
