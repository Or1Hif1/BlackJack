import time

import pygame, sys, random
from pygame.locals import *


def to_num(card_name):
    try:
        if card_name[0] == "T":
            return 10
        elif card_name[0] == "J":
            return 11
        elif card_name[0] == "Q":
            return 12
        elif card_name[0] == "K":
            return 13
        elif card_name[0] == "A":
            return 14
        else:
            return int(card_name[0])
    except IndexError:
        return 99


def bust():
    screen.blit(bust_img, (WINDOW_WIDTH / 2 - bust_img.get_width() / 2, WINDOW_HEIGHT / 2 - bust_img.get_height() / 2))

def win():
    screen.blit(win_img, (WINDOW_WIDTH / 2 - win_img.get_width() / 2, WINDOW_HEIGHT / 2 - win_img.get_height() / 2))

def draw():
    screen.blit(draw_img, (WINDOW_WIDTH / 2 - draw_img.get_width() / 2, WINDOW_HEIGHT / 2 - draw_img.get_height() / 2))

pygame.init()
# Colours
BACKGROUND = (255, 255, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

bg = pygame.image.load("Images/BJ Background.png")
input_box = pygame.image.load("Images/InputBox.png")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hifi Black Jack')

font = pygame.font.SysFont("Barlow", 60, True)
txtsurf = font.render("Enter Your Name", True, (255, 255, 255))
# The main function that controls the game
Input_Text = ""

win_img = pygame.image.load("Images/WIN.png")
bust_img = pygame.image.load("Images/BUST.png")
draw_img = pygame.image.load("Images/DRAW.png")

is_enter = False
gap = 600
f = open("names", "r")
card_names = str(f.read())
f.close()

cards = card_names.split("\n")
card = pygame.image.load("Cards/clear.png")
hit_stand = pygame.image.load("Images/hitstand.png")
rematch = False


def play():
    looping = True
    # The main game loop
    global rematch
    global Input_Text
    global is_enter
    global cards
    global card
    global hit_stand
    is_stand = False
    print(cards)
    total_hand = 0
    dealer_count = 0
    dealer_turn = False
    i = 0
    dealer_stand = False
    d_win = False
    p_win = False
    hands = []
    dealer_hands = []
    fix = False
    while looping:
        #   print("player stand status: "+str(is_stand))
        #   print("dealer stand status: "+str(dealer_stand))

        screen.blit(bg, (0, 0))

        if not fix:
            if is_stand and dealer_stand:
                if total_hand < dealer_count <= 21:
                    print("dealer win")
                    d_win = True
                elif dealer_count == total_hand:
                    print("draw")
                    d_win = True
                    p_win = True
                else:
                    print("player win")
                    p_win = True
            if dealer_count > 21:
                p_win = True
                print("player win")
            if total_hand > 21:
                d_win = True
                print("dealer win")
            if total_hand == 21 and not dealer_stand and dealer_count != 21:
                p_win = True
                print("player win")
            if dealer_hands == 21 and not is_stand and total_hand != 21:
                d_win = True
                print("dealer win")
            if total_hand == 21:
                is_stand = True
            if is_stand and total_hand < dealer_count <= 21:
                d_win = True
                print("dealer wins")

        if not is_enter:
            screen.blit(txtsurf,
                        (WINDOW_WIDTH / 2 - txtsurf.get_width() / 2, WINDOW_HEIGHT / 2 - txtsurf.get_height() / 2 - 100))
            screen.blit(input_box,
                        (WINDOW_WIDTH / 2 - input_box.get_width() / 2, WINDOW_HEIGHT / 2 - input_box.get_height() / 2))
            input_txt = font.render(Input_Text, True, (87, 197, 69))
            screen.blit(input_txt,
                        (WINDOW_WIDTH / 2 - input_txt.get_width() / 2, WINDOW_HEIGHT / 2 - input_txt.get_height() / 2))
        else:
            input_txt = font.render(Input_Text, True, (255, 255, 255))
            dealer_txt = font.render("DEALER", True, (255, 255, 255))
            hand_count = font.render("HAND: "+str(total_hand), True, (255, 255, 255))
            d_hand_count = font.render("D HAND: "+ str(dealer_count), True, (255, 255, 255))
            screen.blit(dealer_txt, (WINDOW_WIDTH / 2 - dealer_txt.get_width() / 2, WINDOW_HEIGHT / 2 - dealer_txt.get_height() / 2 - gap / 2))
            screen.blit(input_txt,
                        (WINDOW_WIDTH / 2 - input_txt.get_width() / 2, WINDOW_HEIGHT / 2 - input_txt.get_height() / 2 + gap / 2))
            screen.blit(hand_count, (WINDOW_WIDTH / 2 - hand_count.get_width() / 2 - 450, WINDOW_HEIGHT / 2 - hand_count.get_height() / 2 - 300))
            screen.blit(d_hand_count, (WINDOW_WIDTH / 2 - d_hand_count.get_width() / 2 - 450 , WINDOW_HEIGHT / 2 - d_hand_count.get_height() / 2 -250))

            if i == 0:
                if len(hands) <= 6 and is_enter:
                    #   print("randoming card")
                    name = cards[random.randint(0, len(cards) - 1)]
                    cards.remove(name)
                    total_hand += to_num(name)
                    print("player: " + str(total_hand))
                    hands.append(pygame.image.load("Cards/" + name))
                    dealer_turn = True
                i += 1
            elif dealer_turn:
                if not dealer_stand and not d_win:
                    if dealer_count < 17:
                        if len(dealer_hands) <= 6 and is_enter and not dealer_stand:
                            if dealer_count < total_hand and is_stand:
                                name = cards[random.randint(0, len(cards) - 1)]
                                cards.remove(name)
                                dealer_count += to_num(name)
                                print("dealer: " + str(dealer_count))
                                dealer_hands.append(pygame.image.load("Cards/" + name))
                                dealer_turn = False
                            elif not is_stand:
                                #   print("randoming card")
                                name = cards[random.randint(0, len(cards) - 1)]
                                cards.remove(name)
                                dealer_count += to_num(name)
                                print("dealer: "+str(dealer_count))
                                dealer_hands.append(pygame.image.load("Cards/" + name))
                                dealer_turn = False
                    elif total_hand < dealer_count:
                        print("dealer stand")
                        dealer_stand = True
                    elif is_stand and dealer_count < total_hand:
                        name = cards[random.randint(0, len(cards) - 1)]
                        cards.remove(name)
                        dealer_count += to_num(name)
                        print("dealer: " + str(dealer_count))
                        dealer_hands.append(pygame.image.load("Cards/" + name))
                        dealer_turn = False
                    elif is_stand and dealer_count == total_hand:
                        dealer_stand = True
            k = 0
            j = 0
            for x in hands:
                k += 31
                x = pygame.transform.scale(x, (147, 207))
                screen.blit(x, (WINDOW_WIDTH/2 - 302*0.65 + k, WINDOW_HEIGHT/2 - card.get_height() / 2+225/16))
            for y in dealer_hands:
                j += 31
                y = pygame.transform.scale(y, (147, 207))
                screen.blit(y, (WINDOW_WIDTH/2 - 302*0.65 + j, WINDOW_HEIGHT/2 - card.get_height() / 2 - 225))
            screen.blit(hit_stand, (35, WINDOW_HEIGHT/2 - hit_stand.get_height()/2))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not is_enter:
                    try:
                        if event.key == pygame.K_RETURN:
                            print("enter")
                            is_enter = True
                        elif event.key == pygame.K_BACKSPACE:
                            print("backspace")
                            if len(Input_Text) > 0:
                                Input_Text = Input_Text[0:len(Input_Text) - 1]
                        elif len(Input_Text) < 11:
                            Input_Text += str(chr(event.key)).upper()
                        print(Input_Text)
                    except ValueError:
                        print("not a regular key")
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not is_stand:
                    if 35 < x < hit_stand.get_width() + 35 and 262 < y < 262 + 197/2:
                        #   print("mouse pressed")
                        if len(hands) <= 6 and is_enter:
                            name = cards[random.randint(0, len(cards)-1)]
                            cards.remove(name)
                            total_hand += to_num(name)
                            print("player: " + str(total_hand))
                            hands.append(pygame.image.load("Cards/"+name))
                            dealer_turn = True
                    if 35 < x < hit_stand.get_width() + 35 and 262 + 197/2 < y < 262 + 197:
                        print("player stand")
                        is_stand = True
                if p_win or d_win:
                    if 258 < y < 204 + 258 and 258 < x < 258 + 763:
                        print("rematch")
                        return True
            if is_stand:
                dealer_turn = True
        # Processing
        # This section will be built out later

        # Render elements of the game
        if d_win or p_win:
            dealer_stand = True
            is_stand = True
            fix = True
            if p_win == d_win:
                draw()
            elif p_win:
                win()
            elif d_win:
                bust()
        pygame.display.update()
        fpsClock.tick(FPS)


def main():
    while True:
        try:
            rematch2 = play()
            if not rematch2:
                break
        except ValueError:
            continue


main()


