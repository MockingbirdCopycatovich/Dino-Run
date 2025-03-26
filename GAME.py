from tkinter import *
from PIL import Image, ImageTk
import pygame
from random import randint
import os

DELAY = 50
TITLE = "Dino Run"
points = 0
paused = False
game_st = True
high_score = 0
win = Tk()
win.title(TITLE)

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

win.geometry(f"{screen_width}x{screen_height // 2 + 150}+0+0")

canvas = Canvas(win, width=screen_width, height=screen_height)
canvas.pack()


def load_high_score():
    global high_score
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            high_score = int(file.read().strip())


def save_high_score():
    global high_score
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

class Score:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.canvas_object = canvas.create_text(self.x, self.y, text="Score: " + str(self.score),
                                                font=('Times New Roman', 20), fill='black')

    def update_score(self):
        self.score += 0.5
        canvas.itemconfig(self.canvas_object, text="Score: " + str(int(self.score)))

    def reset(self):
        self.score = 0
        canvas.itemconfig(self.canvas_object, text="Score: " + str(int(self.score)))


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y + 20
        self.image_refs = []


        def load_image(filename, scale):
            img = Image.open(filename)
            img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.image_refs.append(tk_img)
            return tk_img


        self.image_small = load_image("Enemy/Small Enemy.png", 0.4)
        self.image_big = load_image("Enemy/Big Enemy.png", 0.3)

        self.enemy_type = randint(0, 1)
        if self.enemy_type == 0:
            self.enemy_image = self.image_small

        else:
            self.enemy_image = self.image_big
        self.enemy_canvas_object = canvas.create_image(self.x, self.y, image=self.enemy_image)

        self.speed = 20

    def update_enemy(self):
        canvas.move(self.enemy_canvas_object, -self.speed, 0)
        self.x -= self.speed

        if self.x < -100:
            self.reset_position()

    def reset_position(self):
        self.x = screen_width + randint(300, 600)
        self.y = screen_height // 2 + (40 if self.enemy_type == 1 else 80)
        self.enemy_type = randint(0, 1)
        self.enemy_image = self.image_small if self.enemy_type == 0 else self.image_big
        canvas.itemconfig(self.enemy_canvas_object, image=self.enemy_image)
        canvas.coords(self.enemy_canvas_object, self.x, self.y)


class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_refs = []
        self.in_jump = False
        self.scale = 0.2
        self.hearts = []
        self.alive = True
        self.jump_rule = [-50, -40, -35, -30, 0, 25, 30, 35, 40, 25, 0]
        self.dead_rule = [-50, 25, 25, 50, 50, 100, 100]
        self.dead_timer = 0

        def load_image(filename, scale):
            img = Image.open(filename)
            img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.image_refs.append(tk_img)
            return tk_img

        self.run = [load_image(f"DinoSprites/Run ({i}).png", self.scale) for i in range(1, 8)]
        self.run_frame = 1
        self.jump = [load_image(f"DinoSprites/Jump ({i}).png", self.scale) for i in range(1, 12)]
        self.jump_frame = 0
        self.dead = [load_image(f"DinoSprites/Dead ({i}).png", self.scale) for i in range(1, 8)]
        self.dead_frame = 0

        self.dino = canvas.create_image(self.x, self.y, image=self.run[0])

    def dino_update(self):
        if not self.alive:
            global DELAY
            canvas.itemconfig(self.dino, image=self.dead[self.dead_frame])
            self.dead_frame += 1
            if self.dead_frame >= len(self.dead):
                self.dead_frame -= 1
                canvas.move(self.dino, 0, self.dead_rule[self.dead_timer])
                self.dead_timer += 1
                if self.dead_timer == len(self.dead_rule) - 1:
                    canvas.delete(self.dino)
        else:
            if self.in_jump:
                canvas.move(self.dino, 0, self.jump_rule[self.jump_frame])
                self.jump_frame += 1
                if self.jump_frame >= len(self.jump_rule):
                    self.jump_frame = 0
                    self.in_jump = False
            else:
                canvas.itemconfig(self.dino, image=self.run[self.run_frame])
                self.run_frame = (self.run_frame + 1) % len(self.run)

    def start_jump(self):
        if not self.in_jump:
            self.in_jump = True
            self.jump_frame = 0
    def get_damage(self, event=None):
        self.alive = False

    def update(self):
        for canvas_object in self.canvas_objects:
            canvas.move(canvas_object, -self.speed, 0)
            coords = canvas.coords(canvas_object)

            if coords[0] < -screen_width:
                canvas.coords(canvas_object, screen_width * 2, self.y_offset)


bg_image_1 = Image.open("BG/bg.png")
bg_image_1 = bg_image_1.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo_1 = ImageTk.PhotoImage(bg_image_1)
canvas.create_image(0, 0, image=bg_photo_1, anchor=NW)
bg_image_3 = Image.open("BG/montain-far.png")
bg_image_3 = bg_image_3.resize((screen_width, screen_height-400), Image.LANCZOS)
bg_photo_3 = ImageTk.PhotoImage(bg_image_3)
canvas.create_image(0, 0, image=bg_photo_3, anchor=NW)
bg_image_2 = Image.open("BG/trees.png")
bg_image_2 = bg_image_2.resize((screen_width, screen_height-400), Image.LANCZOS)
bg_photo_2 = ImageTk.PhotoImage(bg_image_2)
canvas.create_image(0, 0, image=bg_photo_2, anchor=NW)


s = Score(screen_width - 150, screen_height // 2 + 100, points)
d = Dino(300, screen_height // 2)
e = [Enemy(screen_width + randint(100, 300), screen_height // 2)]

for i in range(1, 4):
    e.append(Enemy(e[i - 1].x + randint(300, 500), screen_height // 2))

def update():
    global high_score, DELAY

    d.dino_update()
    if game_st:
        s.update_score()
        if s.score > high_score:
            high_score = int(s.score)


    if int(s.score) % 500 == 0:
        for enemy in e:
            enemy.speed += 1
        if DELAY > 20:
            DELAY -= 1

    for enemy in e:
        enemy.update_enemy()

    check_collision()

    if not paused:
        win.after(DELAY, update)


def restart(event=None):
    global s, d, points, paused, e, game_st, DELAY

    canvas.delete("all")

    canvas.create_image(0, 0, image=bg_photo_1, anchor=NW)
    canvas.create_image(0, 0, image=bg_photo_3, anchor=NW)
    canvas.create_image(0, 0, image=bg_photo_2, anchor=NW)

    points = 0
    s = Score(screen_width - 150, screen_height // 2 + 100, points)
    d = Dino(300, screen_height // 2)

    e = []
    start_x = screen_width + randint(300, 600)
    for _ in range(4):
        e.append(Enemy(start_x, screen_height // 2))
        start_x += randint(400, 700)

    game_st = True
    paused = False
    DELAY = 50

    pygame.mixer.init()
    pygame.mixer.music.load("Top_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    load_high_score()


    win.bind("<space>", lambda event: d.start_jump())
    win.bind('<r>', restart)
    win.bind('<R>', restart)
    win.bind("<p>", toggle_pause)
    win.bind("<P>", toggle_pause)

    update()


def game_over():
    global game_st
    save_high_score()
    if game_st:
        canvas.create_text(screen_width // 2, screen_height // 2 - 300, text="Game Over", font=('Times New Roman', 50),
                           fill='red')
        canvas.create_text(screen_width // 2, screen_height // 2 - 250, text=f"Your Score: {int(s.score)}",
                           font=('Times New Roman', 30), fill='black')
        canvas.create_text(screen_width // 2, screen_height // 2 - 200, text="Press R to Restart",
                           font=('Times New Roman', 20), fill='black')
        canvas.create_text(screen_width // 2, screen_height // 2 - 150, text=f"High Score: {high_score}",
                           font=('Times New Roman', 20), fill='black')
        game_st = False
        pygame.mixer.music.stop()
        win.unbind("<space>")
        win.unbind("<p>")


def toggle_pause(event=None):
    global paused
    if paused:
        paused = False
        canvas.delete("pause")
        pygame.mixer.music.unpause()
        update()
        win.bind("<space>", lambda event: d.start_jump())
    else:
        paused = True
        canvas.create_text(screen_width // 2, screen_height // 2 - 200, text="PAUSED",
                           font=('Times New Roman', 50), fill='blue', tag="pause")
        pygame.mixer.music.pause()
        win.unbind("<space>")



def check_collision():
    global points
    for enemy in e:
        dino_coords = canvas.coords(d.dino)
        enemy_coords = canvas.coords(enemy.enemy_canvas_object)

        if (abs(dino_coords[0] - enemy_coords[0]) < 50 and abs(dino_coords[1] - enemy_coords[1]) < 50):
            d.get_damage()
            game_over()


pygame.mixer.init()
pygame.mixer.music.load("Top_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
load_high_score()

win.bind("<space>", lambda event: d.start_jump())
win.bind('<r>', lambda event: restart())
win.bind('<R>', lambda event: restart())
win.bind("<p>", lambda event: toggle_pause())
win.bind("<P>", lambda event: toggle_pause())

update()
win.mainloop()