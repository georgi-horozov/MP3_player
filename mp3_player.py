from tkinter import *

import pygame
from tkinter import filedialog

wnd = Tk()
wnd.title("Georgi Horozov MP3 Player")
wnd.geometry("450x500")
wnd_icon = PhotoImage(file="logo/head_phones.png")
wnd.iconphoto(False, wnd_icon)

song_box = Listbox(wnd, width=65, height=18, bg="#FFE4C4", fg="black")
song_box.pack(pady=20)

pygame.mixer.init()


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


def stop():
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)


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

wnd.mainloop()
