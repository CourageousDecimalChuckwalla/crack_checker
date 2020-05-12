# https://crackwatch.com/api
import datetime

import requests
import time
from win10toast import ToastNotifier
import tkinter as tk
from dateutil.relativedelta import *
from datetime import *
from PIL import ImageTk, Image


# base api url = "https://api.crackwatch.com/api/games"
cracked_games_url = "https://api.crackwatch.com/api/games?&sort_by=crack_date&is_cracked=true"
uncracked_games_url = "https://api.crackwatch.com/api/games?sort_by=release_date&is_released=true&is_cracked=false"
pages = 5


def get_responses():
    uncracked_games_list = []
    x = 0
    while x < pages:
        uncracked_games_list.append(requests.get(uncracked_games_url + "&page=" + str(x)).json())
        time.sleep(1.1)
        x += 1

    return uncracked_games_list


def get_responses_generic(games_url):
    games_list = []
    x = 0
    while x < pages:
        games_list.append(requests.get(games_url + "&page=" + str(x)).json())
        x += 1

    return games_list


def check_if_uncracked(games_list, uncrackedgui_canvas, uncrackedgui_text):
    for a_list in games_list:
        for item in a_list:
            try:
                if item["title"] == "Trials of Mana":
                    uncrackedgui_canvas.itemconfig(uncrackedgui_text, text="Trials of mana is not cracked")
                    print("Trials of mana is not cracked")
                    return 1
            except (TypeError, KeyError):
                return 2
                pass

    print("Trials of mana is not in uncracked list.")
    print("The first 5 pages may have not have been retrieved correctly.")
    print("Trials of mana may be cracked.")


def check_if_cracked(cracked_data):
    for a_list in cracked_data:
        for item in a_list:
            try:
                if item["title"] == "Trials of Mana":
                    print("TRIALS OF MANA IS CRACKED")
                    return 0
            except (TypeError, KeyError):
                return 2
                pass


def toast(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=5, icon_path="N:\\downloads\\v8azkccfg.ico")


def gui_stuff():
    root = tk.Tk()
    root.title(" Gay aids from space")
    canvas = tk.Canvas(root, height=192, width=346, bg='pink')
    canvas.pack()

    # img = tk.PhotoImage(file=r'images\1585500200333.png') confirmed working with return thing in the main function
    img = ImageTk.PhotoImage(Image.open('images\\1588601713866.jpg'))
    background_image = canvas.create_image(0, 0, image=img, anchor='nw')
    print(canvas.winfo_reqwidth(), canvas.winfo_reqheight())
    text_id = canvas.create_text(root.winfo_reqwidth()*.5, root.winfo_reqheight()*.5, text='send nudes', anchor='nw')

    return root, canvas, background_image, img, text_id


if __name__ == "__main__":
    last_time = now_time = datetime.now()  # for timing the gui update
    gui_root, gui_canvas, gui_background_image, gui_image, gui_text = gui_stuff()
    while True:
        try:
            gui_root.update()
        except tk._tkinter.TclError:
            exit()
        if relativedelta(last_time, now_time).seconds > 30:
            now_time = datetime.now()
            try:
                uncracked_list = get_responses_generic(uncracked_games_url)
                cracked_list = get_responses_generic(cracked_games_url)

                check_if_uncracked(uncracked_list, gui_canvas, gui_text)
                if check_if_cracked(cracked_list) == 0:
                    toast("TRIALS OF MANA IS CRACKED", "Trials of mana is cracked!")
            except KeyboardInterrupt:
                exit()
                break
        else:
            last_time = datetime.now()
            pass
