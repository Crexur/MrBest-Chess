import pygame
import sys

from const import *
from game import Game   
from square import Square
from move import Move
from board import Board


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
        
        
        
    
    def flip_board(self):
            new_squares = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            for row in range(ROWS):
                for col in range(COLS):
                    new_row = ROWS - 1 - row
                    new_col = COLS - 1 - col
                    new_squares[new_row][new_col] = self.board.squares[row][col]
            self.board.squares = new_squares

    
    
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
                            import main
                            main.volume1 = 0.5
                            main.sound.set_volume(main.volume1)
                            main.main_menu()
                        
                            
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
            

main = runchess()
main.mainloop()