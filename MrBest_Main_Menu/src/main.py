import pygame, sys
import sprite
from button import Button
import time

from const import *
from game import Game   
from square import Square
from move import Move
from board import Board

pygame.init()
SCREEN = pygame.display.set_mode((600, 600))
pygame.display.set_caption("MrBEST CHESS")

clock = pygame.time.Clock()

py_icon = pygame.image.load('assets/assets/icon.png')
pygame.display.set_icon(py_icon)

BG = pygame.image.load("assets/assets/Background.png")

intro = pygame.image.load("assets/assets/intro_max.png")
sprite_intro = sprite.SpriteSheet(intro)

mrbest_sprite_image = pygame.image.load("assets/assets/mrbeest.png").convert_alpha()
sprite_sheet = sprite.SpriteSheet(mrbest_sprite_image)

#music and sounds
button_sound = pygame.mixer.Sound("assets/assets/mouse_button1.ogg")
sound = pygame.mixer.Sound("assets/assets/phonk-beast_fade.wav")
volume1 = 0.5
sound.set_volume(volume1)
mute_sound = 0

#animation
animation_list1 = []
animation_beast = 3

animation_list2 = []
animation_intro = 56

last_update = pygame.time.get_ticks()
animation_cooldown1 = 50

new_update = pygame.time.get_ticks()
animation_cooldown2 = 100
frame1 = 0
frame2 = 0

run = True

for x in range(animation_intro):
    animation_list1.append(sprite_intro.get_image(x, 750, 420, "black"))

for x in range(animation_beast):
    animation_list2.append(sprite_sheet.get_image(x, 600, 600, "black"))



class runchess:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.board = Board()
        self.game = Game()
        self.volume = 0.1

        self.sound = pygame.mixer.Sound('assets/sounds/final_bgm.wav')
        
        self.sound.set_volume(self.volume)
        
        self.sound.play(-1)
    
    def mainloop(self):
        self.volume = 0.5
        self.sound.set_volume(self.volume)
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger


        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.unicode == "+":
                            self.volume = min(self.volume + 0.01, 1.0)
                            self.sound.set_volume(self.volume)
                        elif event.unicode == "-":
                            self.volume = max(self.volume - 0.01, 0.0)
                            self.sound.set_volume(self.volume)
                        elif event.unicode == "v":
                            self.volume = 0
                            self.sound.set_volume(self.volume)
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            volume1 = 0.5
                            sound.set_volume(volume1)
                            main_menu()
                                                    
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)                            

                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                    
                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()
                        

                     # changing themes
                    if event.key == pygame.K_r:
                        self.volume = 0.5
                        self.sound.set_volume(self.volume)
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            
def revolume():
    volume1 = 0.5
    sound.set_volume(volume1)

def get_font(size):
    return pygame.font.Font("assets/assets/mrbest.ttf", size)

def get_font1(size):
    return pygame.font.Font("assets/assets/mrbest1.ttf", size)

def play():
    sound.set_volume(mute_sound)
    main = runchess()
    main.mainloop()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Music", True, "Black")

        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 250))

        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        #buttons
        OPTIONS_BACK = Button(image=None, pos=(280, 400), text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")
        OPTIONS_MUTE = Button(image=None, pos=(150, 320), text_input="Mute", font=get_font(45), base_color="Black",hovering_color="Red")
        OPTIONS_UNMUTE = Button(image=None, pos=(430, 320), text_input="Unmute", font=get_font(45), base_color="Black",hovering_color="Green")

        OPTIONS_UNMUTE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_UNMUTE.update(SCREEN)

        OPTIONS_MUTE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MUTE.update(SCREEN)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_MUTE.checkForInput(OPTIONS_MOUSE_POS):
                    sound.set_volume(mute_sound)
                if OPTIONS_UNMUTE.checkForInput(OPTIONS_MOUSE_POS):
                    sound.set_volume(volume1)
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    main_menu()

        pygame.display.update()

def main_menu():

    global new_update, frame2
    
    while True:

        text_pos = (190, 100)
        dt = clock.tick(60) / 1000
        text_pos = (text_pos[0] + dt, text_pos[1])
        
        SCREEN.fill("black")

        #update animation
        current_time = pygame.time.get_ticks()
        if current_time - new_update >= animation_cooldown2:
            frame2 += 1
            new_update = current_time
            if frame2 >= len(animation_list2):
                frame2 = 0

        #show frame image
        SCREEN.blit(animation_list2[frame2], (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(55).render("MrBest ", True, "#08b0d5")
        MENU_TEXT1 = get_font(55).render("Chess ", True, "#e3447c")
        
        

        MENU_RECT = MENU_TEXT.get_rect(center=(180, 50))
        MENU_RECT1 = MENU_TEXT.get_rect(center=(505, 50))
        
        #buttons
        PLAY_BUTTON = Button(image=None, pos=(100, 200), text_input="PLAY", font=get_font1(45), base_color="white", hovering_color="#009966")
        OPTIONS_BUTTON = Button(image=None, pos=(110, 255), text_input="OPTIONS", font=get_font1(30), base_color="white", hovering_color="#eeee66")
        QUIT_BUTTON = Button(image=None, pos=(70, 305), text_input="QUIT", font=get_font1(28), base_color="white", hovering_color="#990000")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(MENU_TEXT1, MENU_RECT1)
        
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def intro_beast():
    global last_update, frame1, sound

    time.sleep(1)

    while True:

        SCREEN.fill("black")
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown1:
            frame1 += 1
            last_update = current_time
            if frame1 >= len(animation_list1):

                time.sleep(2)

                sound.play(-1)
                main_menu()


        SCREEN.blit(animation_list1[frame1], (-65, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
intro_beast()