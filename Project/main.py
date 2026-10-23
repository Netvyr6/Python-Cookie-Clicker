from tkinter import *
import time
import random
import pygame
import json

cookiesPerSecond = 0
cookie_count = 0
highestScore = 0
upgrade_cost = 50

try:
    with open("mydata.json", "r") as file:
        loaded_data = json.load(file)
        cookie_count = loaded_data["cookie_count"]
        highestScore = loaded_data["highestScore"]
        cookiesPerSecond = loaded_data["cookiesPerSecond"]
except (FileNotFoundError, json.JSONDecodeError, KeyError):
    cookie_count = 0
    highestScore = 0

root = Tk()
root.title("Cookie clicker")
root.geometry('1920x1080')
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.destroy())

my_frame = Frame(root, bg="lightblue", bd=3, relief=RAISED, borderwidth=0)
my_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)



def sound_effect():
    pygame.mixer.init()
    try:
        click_sound = pygame.mixer.Sound("click.wav")
        click_sound.play()
    except (FileNotFoundError, pygame.error):
        print("Sound file not found! Make sure 'click.wav' is in the same directory.")

def save_game_data():
    gamedata = {
        "cookie_count": cookie_count,
        "highestScore": highestScore,
        "cookiesPerSecond": cookiesPerSecond
    }
    with open("mydata.json", "w") as f:
        json.dump(gamedata, f, indent=4)

def click_cookie():
    global cookie_count, highestScore
    cookie_count += 1
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
    else:
        print("You need ",upgrade_cost," cookies to upgrade!")

def update_cookie_tick():
    global cookie_count, highestScore
    cookie_count += cookiesPerSecond

    if cookie_count > highestScore:
        highestScore = cookie_count
        highScoreLabel.config(text=f"Highest Score: {highestScore}")

    cookiePoints.config(text=f"Total cookies: {cookie_count}")
    save_game_data()
    root.after(1000, update_cookie_tick)

upgrade_cost_label = Label(my_frame, text=f"Upgrade Cost: {upgrade_cost} cookies", font=("Arial", 20), bg="lightblue")
upgrade_cost_label.place(x=1150, y=10)

UpgradeButton1 = Button(my_frame, text="Upgrade", font=("Arial", 20), command=upgrade_cookie, bg="lightblue", borderwidth=0)
UpgradeButton1.place(x=10, y=90)

cookie = Button(my_frame, text="🍪", font=("Arial", 100), command=click_cookie, bg="lightblue", borderwidth=0)
cookie.pack(pady=180)

cookiePoints = Label(my_frame, text=f"Total cookies: {cookie_count}", font=("Arial", 20), bg="lightblue")
cookiePoints.place(x=10, y=10)

highScoreLabel = Label(my_frame, text=f"Highest Score: {highestScore}", font=("Arial", 20), bg="lightblue")
highScoreLabel.place(x=10, y=50)

reset_button = Button(my_frame, text="Reset", font=("Arial", 20), command=reset_cookie_count, bg="lightblue", borderwidth=0)
reset_button.place(x=10, y=750)

root.after(1000, update_cookie_tick)
root.mainloop()
