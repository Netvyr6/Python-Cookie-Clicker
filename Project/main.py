from tkinter import *
import time
import random
import pygame
import json
import tkinter as tk
import math
from tkinter.ttk import *

presscountF= 0
presscountM = 0
cookiesPerSecond = 0
cookie_count = 0
highestScore = 0
upgrade_cost = 50
loading_value = 0
clicks = 0
level = 1
clickStrength = 1


try:
    with open("mydata.json", "r") as file:
        loaded_data = json.load(file)
        cookie_count = loaded_data["cookie_count"]
        highestScore = loaded_data["highestScore"]
        cookiesPerSecond = loaded_data["cookiesPerSecond"]
        upgrade_cost = loaded_data["upgrade_cost"]
        level = loaded_data["level"]
        loading_value = loaded_data["loading_value"]
        clickStrength = loaded_data["clickStrength"]
        
except (FileNotFoundError, json.JSONDecodeError, KeyError):
    cookiesPerSecond = 0
    cookie_count = 0
    highestScore = 0
    upgrade_cost = 50




root = Tk()
root.title("Cookie clicker")
root.geometry('1920x1080')
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.destroy())

loading_frame = tk.Frame(root, bg="lightblue")
loading_frame.pack(fill="both", expand=True)

tk.Label(loading_frame, text="Loading game...", bg="lightblue").pack(pady=20)

loading_bar = Progressbar(loading_frame, mode="indeterminate", length=300)
loading_bar.pack()
loading_bar.start(10)

def fullscreenS():
    global presscountF
    odd=0
    presscountF +=1
    if presscountF % 2 ==odd:
        root.attributes("-fullscreen", True)

    elif presscountF % 2 !=odd:                          
        root.attributes("-fullscreen", False)
    

def stopMusicS():
    global presscountM
    odd=0
    presscountM +=1
    if presscountM % 2 ==odd:
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
    elif presscountM % 2 !=odd:                          
        pygame.mixer.music.stop()

def settings():
    global settings_frame
    my_frame.pack_forget()
    settings_frame = tk.Frame(root, bg="lightblue")
    settings_frame.pack(fill="both", expand=True)

    tk.Label(settings_frame, text="settings", font=("Arial", 30), bg="lightblue").pack(pady=20)
    stopMusic = tk.Button(settings_frame, text="Music", font=("Arial", 20), command=stopMusicS)
    stopMusic.pack(pady=20)

    saveSettings = tk.Button(settings_frame, text="Back", font=("Arial", 20), command=reload_game)
    saveSettings.place(x=10, y=10)

    fullscreen = tk.Button(settings_frame, text="Fullscreen",font=("Arial", 20), command=fullscreenS)
    fullscreen.pack(pady=30)








def sound_effect():
    pygame.mixer.init()
    try:
        click_sound = pygame.mixer.Sound("click.wav")
        click_sound.set_volume(0.3)
        click_sound.play()
    except (FileNotFoundError, pygame.error):
        print("Sound file not found! Make sure 'click.wav' is in the same directory.")

def level_up_system():
    global loading_value, clicks, level, clickStrength
    clicks += 1
    if loading_value >= 100:
        level += 1
        loading_value = 0
        levelBar.configure(value=loading_value)
        levelLabel.config(text=f"level: {level}")
        print(f"Level Up! You are now level {level}.")
        clickStrength = level
    else:
        loading_value += 10/level 
        levelBar.configure(value=loading_value)


def click_cookie():
    global cookie_count, highestScore, clickStrength
    cookie_count += clickStrength
    level_up_system()
    sound_effect()

    if cookie_count > highestScore:
        highestScore = cookie_count
        
    print(f"Total cookies: {cookie_count} | High Score: {highestScore}")
    

    cookiePoints.config(text=f"Total cookies: {cookie_count}")
    highScoreLabel.config(text=f"Highest Score: {highestScore}")
    
    save_game_data()

def reset_cookie_count():
    global cookie_count
    cookie_count = 0
    cookiePoints.config(text=f"Total cookies: {cookie_count}")
    save_game_data()

def upgrade_cookie():
    global cookiesPerSecond, cookie_count, upgrade_cost
    if cookie_count >= upgrade_cost:
        cookie_count= cookie_count - upgrade_cost
        cookiesPerSecond += 1
        print(f"Cookies per second: {cookiesPerSecond}")
        upgrade_cost = upgrade_cost * 2
        upgrade_cost_label.config(text=f"Upgrade Cost: {upgrade_cost} cookies")
        save_game_data()
    else:
        print("You need ",upgrade_cost," cookies to upgrade!")


def save_game_data():
    global cookie_count, highestScore, cookiesPerSecond, upgrade_cost
    gamedata = {
        "cookie_count": cookie_count,
        "highestScore": highestScore,
        "cookiesPerSecond": cookiesPerSecond,
        "upgrade_cost": upgrade_cost,
        "level": level,
        "loading_value": loading_value,
        "clickStrength": clickStrength

    }
    with open("mydata.json", "w") as f:
        json.dump(gamedata, f, indent=4)

def update_cookie_tick():
    global cookie_count, highestScore
    cookie_count += cookiesPerSecond

    if cookie_count > highestScore:
        highestScore = cookie_count
        highScoreLabel.config(text=f"Highest Score: {highestScore}")

    cookiePoints.config(text=f"Total cookies: {cookie_count}")
    save_game_data()
    root.after(1000, update_cookie_tick)

def checkClick(event):
    print(event.x, event.y)
    distance = math.sqrt((event.x - CENTER_X) ** 2 + (event.y - CENTER_Y) ** 2)
    if distance <= radius:
        click_cookie()
    print(f"Distance equation: sqrt(({event.x} - {CENTER_X})^2 + ({event.y} - {CENTER_Y})^2) = {distance:.2f}")
    print(f"Hitbox check: {distance:.2f} <= {radius} -> {distance <= radius}")


def start_game():
    global my_frame, cookieimage, IMG_WIDTH, IMG_HEIGHT
    global CENTER_X, CENTER_Y, radius, cookie_canvas
    global upgrade_cost_label, UpgradeButton1, levelBar, levelLabel
    global cookiePoints, highScoreLabel
    
    loading_bar.stop()
    loading_frame.destroy()
    
    pygame.mixer.init()
    pygame.mixer.music.load("backgroundMusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    my_frame = tk.Frame(root, bg="lightblue", bd=3, relief=RAISED, borderwidth=0)
    my_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

    cookieimage = tk.PhotoImage(file="cookieimage.png").subsample(5, 5)
    IMG_WIDTH = cookieimage.width()
    IMG_HEIGHT = cookieimage.height()
    CENTER_X = IMG_WIDTH // 2
    CENTER_Y = IMG_HEIGHT // 2
    radius = CENTER_X

    cookie_canvas = tk.Canvas(
        my_frame,
        width=IMG_WIDTH,
        height=IMG_HEIGHT,
        bg="lightblue",
        highlightthickness=0
    )
    cookie_canvas.pack(pady=240)
    cookie_canvas.create_image(CENTER_X, CENTER_Y, image=cookieimage)

    cookie_canvas.bind("<Button-1>", checkClick)

    upgrade_cost_label = tk.Label(
        my_frame,
        text=f"Upgrade Cost: {upgrade_cost} cookies",
        font=("Arial", 20),
        bg="lightblue"
    )
    upgrade_cost_label.place(x=1150, y=10)

    UpgradeButton1 = tk.Button(
        my_frame,
        text="Upgrade",
        font=("Arial", 20),
        command=upgrade_cookie,
        bg="lightblue",
        borderwidth=0
    )
    UpgradeButton1.place(x=10, y=90)

    levelBar = Progressbar(
        my_frame,
        orient=HORIZONTAL,
        length=300,
        mode="determinate",
        maximum=100,
        value=loading_value
    )

    levelLabel = tk.Label(
        my_frame,
        text=f"level: {level}",
        font=("Arial", 20),
        bg="lightblue",
        anchor="n",
        justify="center"
    )
    levelLabel.place(x=700, y=40)
    levelBar.place(x=600, y=10)

    cookiePoints = tk.Label(
        my_frame,
        text=f"Total cookies: {cookie_count}",
        font=("Arial", 20),
        bg="lightblue",
        justify="center"
    )
    cookiePoints.place(x=10, y=10)

    highScoreLabel = tk.Label(
        my_frame,
        text=f"Highest Score: {highestScore}",
        font=("Arial", 20),
        bg="lightblue"
    )
    highScoreLabel.place(x=10, y=50)

    settings_button = tk.Button(
        my_frame,
        text="settings",
        font=("Arial", 20),
        command=settings,
        bg="lightblue",
        borderwidth=0
    )
    settings_button.place(x=10, y=750)

    root.after(1000, update_cookie_tick)






def reload_game():
    global my_frame, cookieimage, IMG_WIDTH, IMG_HEIGHT
    global CENTER_X, CENTER_Y, radius, cookie_canvas
    global upgrade_cost_label, UpgradeButton1, levelBar, levelLabel
    global cookiePoints, highScoreLabel
    
    settings_frame.destroy()


    my_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

   
    IMG_WIDTH = cookieimage.width()
    IMG_HEIGHT = cookieimage.height()
    CENTER_X = IMG_WIDTH // 2
    CENTER_Y = IMG_HEIGHT // 2
    radius = CENTER_X

    cookie_canvas = tk.Canvas(
        my_frame,
        width=IMG_WIDTH,
        height=IMG_HEIGHT,
        bg="lightblue",
        highlightthickness=0
    )
    cookie_canvas.pack(pady=240)
    cookie_canvas.create_image(CENTER_X, CENTER_Y, image=cookieimage)
    cookie_canvas.bind("<Button-1>", checkClick)


    upgrade_cost_label = tk.Label(
        my_frame,
        text=f"Upgrade Cost: {upgrade_cost} cookies",
        font=("Arial", 20),
        bg="lightblue"
    )
    upgrade_cost_label.place(x=1150, y=10)

    UpgradeButton1 = tk.Button(
        my_frame,
        text="Upgrade",
        font=("Arial", 20),
        command=upgrade_cookie,
        bg="lightblue",
        borderwidth=0
    )
    UpgradeButton1.place(x=10, y=90)

    levelBar = Progressbar(
        my_frame,
        orient=HORIZONTAL,
        length=300,
        mode="determinate",
        maximum=100,
        value=loading_value
    )

    levelLabel = tk.Label(
        my_frame,
        text=f"level: {level}",
        font=("Arial", 20),
        bg="lightblue",
        anchor="n",
        justify="center"
    )
    levelLabel.place(x=700, y=40)
    levelBar.place(x=600, y=10)

    cookiePoints = tk.Label(
        my_frame,
        text=f"Total cookies: {cookie_count}",
        font=("Arial", 20),
        bg="lightblue",
        justify="center"
    )
    cookiePoints.place(x=10, y=10)

    highScoreLabel = tk.Label(
        my_frame,
        text=f"Highest Score: {highestScore}",
        font=("Arial", 20),
        bg="lightblue"
    )
    highScoreLabel.place(x=10, y=50)

    settings_button = tk.Button(
        my_frame,
        text="settings",
        font=("Arial", 20),
        command=settings,
        bg="lightblue",
        borderwidth=0
    )
    settings_button.place(x=10, y=750)

  


root.after(random.randint(1000, 3000), start_game)
root.mainloop()
