import math
import random
import sys
import time

import pygame
from pygame.math import Vector2

from button import Button


# font stuff
def get_font(s):
    return pygame.font.Font("fonts/Cuprum-SemiBold.ttf", s)


# auto convert func
def load_con(image_to_convert):
    return pygame.image.load(image_to_convert).convert_alpha()


# game initialization
# pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Яндекс.Такси')
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# music list
music_list = ["music/Чёрные глаза.mp3", "music/Раньше в твоих глазах....mp3", "music/Траблы, дым, адреналин.mp3", "music/Калым.mp3",
              "music/Chill.mp3", "music/Вите надо выйти.mp3", "music/А горький вкус твоей любви.mp3", "music/Ангелы.mp3",
              "music/Suzume Nocturne 2.mp3", "music/Малинки-Малинки.mp3"]
random.shuffle(music_list)
pygame.mixer.music.load(music_list[0])
current_music = 0
# loading images

# background image
image = load_con('images/map2.png')
info_image = load_con('images/in.png')

# car image
car = load_con('images/car_image.png')

# traffic light image
red_light = load_con('images/red_light.png')
yellow_light = load_con('images/yellow_light.png')
green_light = load_con('images/green light.png')

# child image
child_good = load_con('images/child_good.png')
child_scream = load_con('images/child_scream.png')

# other images
menu_image = load_con('images/menu.png')
menu_background_image = load_con('images/menu_background_image.png')
victory = load_con('images/victory.png')
im1 = load_con('images/1.png')
im2 = load_con('images/2.png')
im_near = load_con('images/near.png')
im3 = load_con('images/3.png')
im4 = load_con('images/4.png')
im5 = load_con('images/5.png')
im6 = load_con('images/6.png')

# background stuff
image = pygame.transform.smoothscale(image, (4320, 7680))
image_width, image_height = image.get_size()
image_center = Vector2(image_width / 2 - 400, (image_height / 9) * 8)

# car stuff
car = pygame.transform.smoothscale(car, (128, 257))

# child stuff
child_good = pygame.transform.scale(child_good, (88, 266))
child_scream = pygame.transform.scale(child_scream, (180, 266))

fl = True
mus_fl = True


def play():
    # map box to rotate the image
    box = [pygame.math.Vector2(p) for p in [(0, 0), (image_width, 0), (image_width, -image_height), (0, -image_height)]]

    # box_coord rotation
    def box_rotation(p):
        return p.rotate(angle)

    # map rotation func
    def blit_rotate(surf, im, pos_to_use, origin_pos, angle_to_use):

        # new position
        origin_pos[0] += x
        origin_pos[1] -= y

        # box coordinates
        box_rotate = list(map(box_rotation, box))

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
        pivot_move = pivot.rotate(angle_to_use) + v - pivot
        # calculate the upper left origin of the rotated image
        move = [-origin_pos[0] + min(box_rotate, key=lambda p: p[0])[0] - pivot_move[0],
                -origin_pos[1] - max(box_rotate, key=lambda p: p[1])[1] + pivot_move[1]]

        # blit rotated image
        surf.blit(pygame.transform.rotate(im, angle_to_use), (pos_to_use[0] + move[0], pos_to_use[1] + move[1]))

    # exit button func
    def rect_button_mouse(mx, my, bx, by, b_width, b_height):
        if bx < mx < bx + b_width:
            if by < my < by + b_height:
                return True
        return False

    # all buttons' clicked event
    def clicked(events_to_use, mx, my, bx, by, b_width, b_height):
        for event_to_use in events_to_use:
            if event_to_use.type == pygame.MOUSEBUTTONDOWN:
                if rect_button_mouse(mx, my, bx, by, b_width, b_height):
                    return True
        return False

    # all buttons func
    def button(events_to_use, mx, my):
        pygame.draw.rect(screen, (233, 195, 0), (30, 30, 200, 60), 0, 10)
        screen.blit(menu_image, (60, 33))
        if clicked(events_to_use, mx, my, 30, 30, 200, 60):
            main_menu()

    def chort(phrase):
        options_text = get_font(40).render(phrase, True, "White")
        options_rect = options_text.get_rect(center=(1700, 200))
        screen.blit(options_text, options_rect)

    def pictures(num_picture):
        screen.blit(num_picture, (0, 0))
        pygame.display.flip()

    # flags
    inf = False

    # params
    angle, m, n = 0, 0, 0
    speed, speed_back = 0, 0
    pos = (screen.get_width() / 2, screen.get_height() / 1.5)
    money = 13.3

    # top obstacle
    obs1 = pygame.Rect(0, 0, 4320, 20)

    # left obstacle
    obs2 = pygame.Rect(0, 0, 20, 7680)

    # right obstacle
    obs3 = pygame.Rect(4300, 0, 20, 7680)

    # bottom obstacle
    obs4 = pygame.Rect(0, 7660, 4320, 20)

    car_rect = car.get_rect()
    target_rect = pygame.Rect(0, 0, 1000, 300)

    pygame.display.update()
    if fl:
        pictures(im1)
        time.sleep(5)

        pictures(im2)
        time.sleep(3)

        pictures(im_near)
        time.sleep(3)

        pictures(im3)
        time.sleep(2)

        pictures(im4)
        time.sleep(3)

        pictures(im5)
        time.sleep(6)

        pictures(im6)
        time.sleep(3)

    pygame.mixer.music.set_volume(0.5)
    if mus_fl:
        pygame.mixer.music.play()

    # main loop
    while True:
        global current_music
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((120, 154, 76))

        # keys events:
        keys = pygame.key.get_pressed()

        # straight
        if keys[pygame.K_w]:
            m += 5 + speed
            n += 5
            if speed < 10:
                speed += 0.01

        # back
        if keys[pygame.K_s]:
            m -= 5 + speed_back
            n -= 5
            if speed_back < 10:
                speed_back += 0.01

        # left
        if keys[pygame.K_a]:
            angle -= 10

        # right
        if keys[pygame.K_d]:
            angle += 10

        # info about taxi activation
        if keys[pygame.K_SPACE]:
            inf = not inf

        elif keys[pygame.K_f]:
            current_music += 1
            if current_music >= len(music_list):
                current_music = 0
            pygame.mixer.music.load(music_list[current_music])
            if mus_fl:
                pygame.mixer.music.play()

        # coordinates calculation
        radians = math.radians(angle)
        x = m * math.sin(radians)
        y = n * math.cos(radians)
        car_rect.topleft = image_center + Vector2(x, y)

        if target_rect.colliderect(car_rect):
            m, n = 0, 0
            x, y = 0, 0
            car_rect = car_rect

            victory_win()
        if car_rect.colliderect(obs1):
            m = 0
            n = 0
            chort('Уффффф')

        if car_rect.colliderect(obs2):
            m = 0
            n = 0
            chort('Вот это разгон!')

        if car_rect.colliderect(obs3):
            m = 0
            n = 0
            chort('Ай')

        if car_rect.colliderect(obs4):
            m = 0
            n = 0
            chort('Эээээ')

        # rotation func activating
        v = Vector2(x, y)

        blit_rotate(screen, image, pos, image_center, angle)
        pygame.draw.rect(image, (120, 154, 76), obs1)
        pygame.draw.rect(image, (120, 154, 76), obs2)
        pygame.draw.rect(image, (120, 154, 76), obs3)
        pygame.draw.rect(image, (120, 154, 76), obs4)

        screen.blit(car, (pos[0], pos[1] - 80))
        image.blit(child_good, (3010, 1000))
        image.blit(red_light, (2400, 1000))

        # info about taxi
        if inf:
            pygame.draw.rect(screen, (233, 195, 0), (30, 630, 510, 310), 0, 10)
            screen.blit(info_image, (40, 640))
            options_text = get_font(40).render(str(money), True, "Black")
            options_rect = options_text.get_rect(center=(190, 225))
            info_image.blit(options_text, options_rect)

        # exit button
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        button(events, mouse_pos[0], mouse_pos[1])

        # updating
        pygame.display.update()


def options():
    global fl, mus_fl
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        screen.fill("white")

        options_text = get_font(60).render("Настройки", True, "Black")
        options_rect = options_text.get_rect(center=(width / 2, height / 7))
        screen.blit(options_text, options_rect)

        pic_text = get_font(40).render("Воспроизведение вступительного ролика:", True, "Black")
        pic_rect = pic_text.get_rect(center=(width / 2 - 150, height / 2 - 100))
        screen.blit(pic_text, pic_rect)

        change_fl = Button(image=None, pos=(width / 2 + 280, height / 2 - 100), text_input="Вкл" if fl else 'Выкл',
                           font=get_font(40),
                           base_color="Black", hovering_color="#789A4C")

        change_fl.change_color(options_mouse_pos)
        change_fl.update(screen)

        mus_text = get_font(40).render("Звуковое сопровождение:", True, "Black")
        mus_rect = pic_text.get_rect(center=(width / 2 - 150, height / 2))
        screen.blit(mus_text, mus_rect)

        change_mus = Button(image=None, pos=(width / 2 + 280, height / 2), text_input="Вкл" if mus_fl else 'Выкл',
                            font=get_font(40),
                            base_color="Black", hovering_color="#789A4C")

        change_mus.change_color(options_mouse_pos)
        change_mus.update(screen)

        options_back = Button(image=None, pos=(width / 2, 800),
                              text_input="Назад", font=get_font(75), base_color="Black", hovering_color="#789A4C")

        options_back.change_color(options_mouse_pos)
        options_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.check_for_input(options_mouse_pos):
                    main_menu()
                if change_fl.check_for_input(options_mouse_pos):
                    fl = not fl
                if change_mus.check_for_input(options_mouse_pos):
                    mus_fl = not mus_fl

        pygame.display.update()


def victory_win():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(0)
        screen.blit(victory, (0, 0))

        victory_back = Button(image=None, pos=(1700, 900),
                              text_input="Выйти", font=get_font(75), base_color="Black", hovering_color="#789A4C")
        victory_back.change_color(mouse_pos)
        victory_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if victory_back.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def main_menu():
    while True:
        screen.blit(menu_background_image, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        play_button = Button(image=None, pos=(1450, 400),
                             text_input="Играть", font=get_font(70), base_color="#4D6431", hovering_color="#789A4C")
        options_button = Button(image=None, pos=(1450, 530),
                                text_input="Настройки", font=get_font(70), base_color="#4D6431",
                                hovering_color="#789A4C")
        quit_button = Button(image=None, pos=(1450, 660),
                             text_input="Выход", font=get_font(70), base_color="#4D6431", hovering_color="#789A4C")

        for button in [play_button, options_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if options_button.check_for_input(menu_mouse_pos):
                    options()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
