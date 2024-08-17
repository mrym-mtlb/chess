import pygame as py
import sys
from button import Buttons

 

py.init()
width = 720
height = 532
sq_size = 512 // 8 #dimention of chess board is 8x8
max_FPS = 60 #for animations
small_font = py.font.Font("freesansbold.ttf", 12)
big_Font = py.font.Font(None, 32)








def load_images():
    images = {}
    pieces = ['K', 'k', 'B', 'b', 'P', 'p', 'R', 'r', 'N', 'n', 'Q', 'q'] 
    num = 0
    for piece in pieces:
        images[piece] = py.image.load(f"chess pieces images/{num}.png")
        images[piece] = py.transform.scale(images[piece], (sq_size,sq_size))
        num += 1
    return images



class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def match(self,list_pos):
        pass
    


class Piece:
    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False 
        self.position = position
    def possible_moves(self):
        pass
    def move(self,end_pos):
        pos_list = []
        for move_object in self.possible_moves():
            pos_list.append((move_object.row , move_object.col))
        return (end_pos.row, end_pos.col) in pos_list
    def __str__(self):
        pass
        




class King(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "king"
    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        # Castling
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check kingside castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(self.position.col + 1, 7)):
                    moves.append(Position(self.position.row, self.position.col + 2))
            # Check queenside castling
            if  self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(Position(self.position.row, self.position.col - 2))
        return moves
    def __str__(self):
        if self.color == "White":
            return "K"
        return "k"



class Bishop(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "bishop"
    def possible_moves(self):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in directions:
            for i in range(1,8):
                new_pos = Position(self.position.row + (dr * i), self.position.col + (dc * i))
                if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
                    moves.append(new_pos)
                elif self.board.is_inside_board(new_pos) and self.board.is_enemy_piece(new_pos, self.color):
                    moves.append(new_pos)
                    break
                else:
                    break     
        return moves
    def __str__(self):
        if self.color == "White":
            return "B"
        return "b" 



class Pawn(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "pawn"
        self.enpassant_moved = False
    def possible_moves(self):
        moves = []
        direction = -1 if self.color == "White" else 1
        start_row = 6 if self.color == "White" else 1
        # Moves for regular pawn advance
        new_pos = Position(self.position.row + direction, self.position.col)
        if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
            moves.append(new_pos)
            # 2_square moves for pawn pieces that hasn't moved
            new_pos = Position(self.position.row + 2 * direction, self.position.col)
            if self.position.row == start_row and self.board.is_square_empty(new_pos):
                moves.append(new_pos)
        # Moves for capturing diagonally
        for i in [1,-1]:
            new_pos = Position(self.position.row + direction, self.position.col + i)
            if self.board.is_inside_board(new_pos) and self.board.is_enemy_piece(new_pos, self.color): 
                moves.append(new_pos)
            # Capturing in enpassant
            if self.board.enpassant_sq_possible and abs(self.position.row - self.board.enpassant_sq_possible.row) == 1 \
                  and abs(self.board.enpassant_sq_possible.col - self.position.col) == 1:
                moves.append(self.board.enpassant_sq_possible)
                self.enpassant_moved = True
        return moves         
    def __str__(self):
        if self.color == "White":
            return "P"
        return "p" 
    


class Rook(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "rook"
    def possible_moves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            for i in range(1,8):
                new_pos = Position(self.position.row + (dr * i), self.position.col + (dc * i))
                if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
                    moves.append(new_pos)
                elif self.board.is_inside_board(new_pos) and self.board.is_enemy_piece(new_pos, self.color):
                    moves.append(new_pos)
                    break
                else:
                    break     
        return moves
    def __str__(self):
        if self.color == "White":
            return "R"
        return "r" 



class Knight(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "knight"
    def possible_moves(self):
        moves = []
        directions = [(2,1),(-2,1), (2,-1), (-2,-1), (1,2), (-1,2), (1,-2), (-1,-2)]
        for dr , dc in directions:
            new_pos = Position(self.position.row + dr , self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves
    def __str__(self):
        if self.color == "White":
            return "N"
        return "n" 
            


class Queen(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "queen"
    def possible_moves(self):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            for i in range(1,8):
                new_pos = Position(self.position.row + (dr * i), self.position.col + (dc * i))
                if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
                    moves.append(new_pos)
                elif self.board.is_inside_board(new_pos) and self.board.is_enemy_piece(new_pos, self.color):
                    moves.append(new_pos)
                    break
                else:
                    break
        return moves
    def __str__(self):
        if self.color == "White":
            return "Q"
        return "q"  
    




class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)] #initialize the board
        self.enpassant_sq_possible = None
        self.captured_pieces = []
        self.promoting_piece = None

    def place_piece(self, piece, position):
        # Put the piece in the board at the given position
        piece.position = position
        self.board[piece.position.row][piece.position.col] = piece


    def remove_piece(self, piece):
        self.board[piece.position.row][piece.position.col] = None

    def move_piece(self, start_pos, end_pos, current_player):
        piece = self.board[start_pos.row][start_pos.col]
        if piece:
            if piece.move(end_pos):
                
                # Pawn promotion
                if self.promoting_piece and piece.piece_type == 'pawn' and (end_pos.row == 7 or end_pos.row == 0):
                    board = piece.board
                    position = piece.position
                    if self.promoting_piece == 'Queen':
                        piece = Queen(current_player, board, position)
                    elif self.promoting_piece == 'Bishop':
                        piece = Bishop(current_player, board, position)
                    elif self.promoting_piece == 'Rook':
                        piece = Rook(current_player, board, position)
                    else:
                        piece = Knight(current_player, board, position)

                # Captured Pieces 
                capture_piece = self.board[end_pos.row][end_pos.col]
                if capture_piece:
                    self.captured_pieces.append(str(capture_piece))

                self.remove_piece(piece)
                self.place_piece(piece, end_pos)
                piece.has_moved = True

                # Enpassant
                if piece.piece_type == "pawn" and abs(start_pos.row - end_pos.row)== 2:
                    self.enpassant_sq_possible = Position((start_pos.row + end_pos.row)//2 , start_pos.col)
                else:
                    self.enpassant_sq_possible = None

                # Casteing
                if piece.piece_type == "king" and int(start_pos.col - end_pos.col) == 2: #queen side casteling
                    rook = self.board[start_pos.row][0]
                    self.remove_piece(rook)
                    self.place_piece(rook, Position(start_pos.row, 3))
                elif piece.piece_type == "king" and int(start_pos.col - end_pos.col) == -2: #king side casteling
                    rook = self.board[start_pos.row][7]
                    self.remove_piece(rook)
                    self.place_piece(rook, Position(start_pos.row, 5))

                return True
        else:
            print("No piece at the starting position.")
            return False

    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None

    def is_enemy_piece(self, position, color):
        piece = self.board[position.row][position.col]
        if piece:
            return piece.color != color

    def is_inside_board(self, position):
        return (0 <= position.row < 8) and (0 <= position.col < 8)

    def print_board(self):
        print(" | a b c d e f g h")
        print("------------------")
        for i, row in enumerate(self.board):
            row_str = str(i) + "| "
            for piece in row:
                if piece:
                    row_str += f"{piece} "
                else:
                    row_str += ". "
            print(row_str)
        print("\n")




class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()

    def setup_board(self):
        # Place white pieces
        self.board.place_piece(Rook("White",self.board), Position(7, 0))
        self.board.place_piece(Knight("White",self.board), Position(7, 1))
        self.board.place_piece(Bishop("White",self.board), Position(7, 2))
        self.board.place_piece(Queen("White",self.board), Position(7, 3))
        self.board.place_piece(King("White",self.board), Position(7, 4))
        self.board.place_piece(Bishop("White",self.board), Position(7, 5))
        self.board.place_piece(Knight("White",self.board), Position(7, 6))
        self.board.place_piece(Rook("White",self.board), Position(7, 7))
        for i in range(8):
            self.board.place_piece(Pawn("White",self.board), Position(6, i))

        # Place black pieces
        self.board.place_piece(Rook("Black",self.board), Position(0, 0))
        self.board.place_piece(Knight("Black",self.board), Position(0, 1))
        self.board.place_piece(Bishop("Black",self.board), Position(0, 2))
        self.board.place_piece(Queen("Black",self.board), Position(0, 3))
        self.board.place_piece(King("Black",self.board), Position(0, 4))
        self.board.place_piece(Bishop("Black",self.board), Position(0, 5))
        self.board.place_piece(Knight("Black",self.board), Position(0, 6))
        self.board.place_piece(Rook("Black",self.board), Position(0, 7))
        for i in range(8):
            self.board.place_piece(Pawn("Black",self.board), Position(1, i))

    def print_board(self):
        self.board.print_board()




class Chess:
    def __init__(self):
        self.chess_set = ChessSet()
        self.start_pos = None
        self.end_pos = None


    def game_over(self, current_player):
        window = py.display.set_mode((width, height))
        py.display.set_caption("game over!")
        winner = "Black" if current_player == "White" else "White"

        run = True
        while run:
            massage = big_Font.render(f"{winner} has won :)))", True, py.Color("White"))
            window.blit(massage, py.Rect(250, 200, 100, 30))
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False

            py.display.flip() 



    def pawn_promotion_menu(self):
        menu = py.display.set_mode((width, height))
        py.display.set_caption("Pawn Promotion")
        position = py.mouse.get_pos()


        run = True
        while run:
                    
            menu_text = big_Font.render("Choose a piece to promote the pawn", True, py.Color("White"))
            menu.blit(menu_text, py.Rect(170, 100, 100, 30))

            queen_promoted = Buttons(image=None, x_pos=350, y_pos=200, text_input="Queen", font=big_Font, 
                                    base_color=py.Color("White"), hovering_color=py.Color("Orange"))
            knight_promoted = Buttons(image=None, x_pos=350, y_pos=250, text_input="Knight", font=big_Font, 
                                    base_color=py.Color("White"), hovering_color=py.Color("Orange"))
            rook_promoted = Buttons(image=None, x_pos=350, y_pos=300, text_input="Rook", font=big_Font, 
                                    base_color=py.Color("White"), hovering_color=py.Color("Orange"))
            bishop_promoted = Buttons(image=None, x_pos=350, y_pos=350, text_input="Bishop", font=big_Font, 
                                    base_color=py.Color("White"), hovering_color=py.Color("Orange"))
            
            for button in [queen_promoted, knight_promoted, rook_promoted, bishop_promoted]:
                button.change_color(position)
                button.update(menu)
            
            # Mouse handlers
            events = py.event.get()
            for event in events:
                if event.type == py.QUIT:
                    run = False
                elif event.type == py.MOUSEBUTTONDOWN:
                    position = py.mouse.get_pos()
                    if queen_promoted.check_for_input(position):
                        self.chess_set.board.promoting_piece = "Queen"
                        run = False
                    elif knight_promoted.check_for_input(position):
                        self.chess_set.board.promoting_piece = "Knight"
                        run = False
                    elif bishop_promoted.check_for_input(position):
                        self.chess_set.board.promoting_piece = "Bishop"
                        run = False
                    elif rook_promoted.check_for_input(position):
                        self.chess_set.board.promoting_piece = "Rook"
                        run = False


            py.display.flip()   

    def start_game(self):
        current_player = "White" 

        screen = py.display.set_mode((width, height))
        py.display.set_caption("Welcome to Chess :)")    
        
        run = True
        sq_selected = ()
        player_clicks = [] #to save start_pos & end_pos of each move
        while run:
            # Mouse handlers
            events = py.event.get()
            for event in events:
                if event.type == py.QUIT:
                    py.display.quit()
                    py.quit()
                    sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN:
                    location = py.mouse.get_pos() #(x,y)
                    row = (location[1] - 20) // sq_size 
                    col = (location[0] - 20) // sq_size 
                    if sq_selected == (row, col): #double click to undo action
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                        self.start_pos = self.move_touple(player_clicks[0])
                
                    if len(player_clicks) == 2: #after second click
                        self.end_pos = self.move_touple(player_clicks[1])
                        piece = self.chess_set.board.board[self.start_pos.row][self.start_pos.col]
                        if piece and piece.color == current_player:
                            if piece.move(self.end_pos):
                                # Deleting enpassant pawn piece
                                if piece.piece_type == "pawn" and self.start_pos.col != self.end_pos.col and self.chess_set.board.board[self.end_pos.row][self.end_pos.col] is None:
                                    enemy = self.chess_set.board.board[self.start_pos.row][self.end_pos.col]
                                    if enemy and enemy.color != current_player:
                                        self.chess_set.board.remove_piece(enemy)
                                        self.chess_set.board.captured_pieces.append(str(enemy))
                                # Pawn Promotion
                                if piece.piece_type == 'pawn' and (self.end_pos.row == 7 or self.end_pos.row == 0):
                                    self.pawn_promotion_menu()                                   
                                self.chess_set.board.move_piece(self.start_pos, self.end_pos, current_player)
                                sq_selected = ()
                                player_clicks = []
                                # Switch the turns
                                current_player = "Black" if current_player == "White" else "White"

                            else:
                                print('Your choice is not possible, please choose another piece and move again!')
                                sq_selected = ()
                                player_clicks = []
                        else:
                            # print(f"it's {current_player} turn, please choose the correct piece and then move")
                            sq_selected = ()
                            player_clicks = []
                
                        
            # self.chess_set.print_board()
            # print(f"\n{current_player}'s turn:")
            # start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            # end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ") 

            # # Check if the input is according to the expected format
            # while not self.is_valid_input(start_pos, end_pos):
            #     print("Be careful what you are entering")
            #     start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            #     end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")
                
            # # Move the piece if it is possible, otherwise notify the user to select other moves
            # while True:
            #     start_pos = self.from_algebraic(start_pos)
            #     end_pos = self.from_algebraic(end_pos)
            #     piece = self.chess_set.board.board[start_pos.row][start_pos.col]
            #     if piece and piece.color == current_player:
            #         if piece.move(end_pos):
            #             self.chess_set.board.move_piece(start_pos, end_pos)
            #             break
            #         else:
            #             print('Your choice is not possible, please choose another move again!')
            #             start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            #             end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")
            #     else:
            #         print(f"it's {current_player} turn, please choose the correct piece and then move")
            #         start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            #         end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")

            # Print the board
            # self.chess_set.print_board()


            # Check if the king is in checkmate (much simpler than real-world chess)
            if self.is_checkmate(current_player):
                self.game_over(current_player)
                run = False

                
            screen.fill(py.Color("light gray"))
            self.draw_game_state(screen, current_player)
            py.display.flip()



            # Check the king is in check (in draw_game_state function)


    # def is_valid_input(self, start_pos, end_pos): 
    #     if len(start_pos) == 2 and len(end_pos) == 2:
    #         if start_pos[0].lower() in 'abcdefgh' and start_pos[1] in '01234567':
    #             if end_pos[0].lower() in 'abcdefgh' and end_pos[1] in '01234567':
    #                 return True
    #             else:
    #                 return False
    #         else:
    #             return False
    #     else:
    #         return False
        

    def is_check(self, current_player):
        # Find current_player's king on the board, check if the king is in check
        king = None
        enemy_pieces = []
        enemy = "Black" if current_player == "White" else "White"
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece and piece.piece_type == "king" and piece.color == current_player:
                    king = piece
                if piece and piece.color == enemy:
                    enemy_pieces.append(piece)
        for piece in enemy_pieces:
            for position in piece.possible_moves():
                if king and (king.position.row , king.position.col) == (position.row , position.col):
                    return True
        return False
            

    def is_checkmate(self, current_player):
        # The previous code has been changed
        # We got possible moves of enemy pieces if our king were not existed

        item_deleted = []
        enemy_pieces = []
        enemy_possible_moves = []
        enemy_pieces_types = []
        ally_pieces = []
        ally_possible_moves = []
        king_possible_moves = []
        enemy = "Black" if current_player == "White" else "White"

        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece and piece.piece_type == "king" and piece.color == current_player:
                    king_position = (piece.position.row, piece.position.col)
                    king_board = piece.board
                    king_possible_moves.append(king_position)
                    for position in piece.possible_moves():
                        king_possible_moves.append((position.row, position.col))
                    self.chess_set.board.remove_piece(piece)
                if piece and piece.color == enemy:
                    enemy_pieces.append(piece)
                    enemy_pieces_types.append(piece.piece_type)
                if piece and piece.color == current_player and piece.piece_type != "king":
                    ally_pieces.append(piece)
             

        for piece in enemy_pieces:
            for position in piece.possible_moves():
                enemy_possible_moves.append((position.row, position.col))

        for piece in ally_pieces:
            for position in piece.possible_moves():
                ally_possible_moves.append((position.row, position.col))

        for item in enemy_possible_moves:
            if item in king_possible_moves:
                king_possible_moves.remove(item)
                if item != king_position:
                    item_deleted.append(item)

        self.chess_set.board.place_piece(King(current_player, king_board), Position(king_position[0], king_position[1]))
         
        # Check if an ally piece can be pinned or not 
        if len(king_possible_moves) == 0:
            if len(item_deleted) == 1 and item_deleted[0] in ally_possible_moves:
                return False
            return True
        return False


    

    def draw_game_state(self, screen, current_player):
              
        # Number Image on pygame surface
        nums = [8, 7, 6, 5, 4, 3, 2, 1]
        for num in nums:
            for c in range(8):
                number_image = small_font.render(str(num), True, py.Color("black"))
                screen.blit(number_image, py.Rect(c*sq_size + 5, abs(8-num)*sq_size + 47, sq_size, sq_size))

        # Font Image on pygame surface
        alphas = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
        for i in range(8):
            for j in range(8):
                alphas_image = small_font.render(alphas[j], True, py.Color("black"))
                screen.blit(alphas_image, py.Rect(j*sq_size + 47, i*sq_size + 5, sq_size, sq_size))
        self.draw_board(screen, current_player)
        self.draw_pieces(screen)

        # Showing turn in GUI
        turn = big_Font.render(f"{current_player}'s Turn", True, py.Color("black"))
        screen.blit(turn, py.Rect(560, 30, 100, 30))
        line = small_font.render("________________", True, py.Color("dark gray"))
        screen.blit(line, py.Rect(570, 50, 100, 30))

        # Check the king is in check
        if self.is_check(current_player):
            # print(f"Move your {current_player} king")
            check_warn = small_font.render(f"{current_player} is in check !!!", True, py.Color("Red"))
            screen.blit(check_warn, py.Rect(570, 70, 100, 30))


        # Showing captured pieces
        self.show_captured(screen)


    def show_captured(self, screen):
        py.draw.rect(screen, py.Color("black"), py.Rect(553, 230, 66, 280), 1)
        py.draw.rect(screen, py.Color("black"), py.Rect(635, 230, 66, 280), 1)
        captured_pieces = self.chess_set.board.captured_pieces
        images = load_images()
        num_w , num_b = 0 , 0
        counter_w , counter_b = 0 , 0
        for piece in captured_pieces:
            piece2 = py.transform.scale(images[piece], (33,33))
            if num_w % 2 == 0 and piece.isupper():
                screen.blit(piece2, py.Rect(553, 230 + (counter_w // 2)*33, 33, 33))
                num_w += 35
                counter_w += 1
            elif num_w % 2 == 1 and piece.isupper():
                screen.blit(piece2, py.Rect(586, 230 + (counter_w // 2)*33, 33, 33))
                num_w += 35
                counter_w += 1
            if num_b % 2 == 0 and piece.islower():
                screen.blit(piece2, py.Rect(635, 230 + (counter_b // 2)*33, 33, 33))
                num_b += 35
                counter_b += 1
            elif num_b % 2 == 1 and piece.islower():
                screen.blit(piece2, py.Rect(668, 230 + (counter_b // 2)*33, 33, 33))
                num_b += 35
                counter_b += 1



    def draw_board(self, screen, current_player):
        colors = [py.Color("white"), py.Color("dark gray")]
        for r in range(8):
            for c in range(8):
                color = colors[(r+c) % 2]
                # Identifying selected piece
                if self.start_pos:
                    selected_piece = self.chess_set.board.board[self.start_pos.row][self.start_pos.col]
                    if selected_piece and selected_piece.color == current_player:
                        if self.start_pos.row == r and self.start_pos.col == c:
                            py.draw.rect(screen, (203, 195, 227), py.Rect(c*sq_size + 20, r*sq_size + 20, sq_size, sq_size))
                            py.draw.rect(screen, "black", py.Rect(c*sq_size + 20, r*sq_size + 20, sq_size, sq_size), 1)
                        else:
                            py.draw.rect(screen, color, py.Rect(c*sq_size + 20, r*sq_size + 20, sq_size, sq_size))
                        # Identifying possible moves of selected piece
                        for position in selected_piece.possible_moves():
                                py.draw.rect(screen, "purple", py.Rect((position.col)*sq_size + 20, (position.row)*sq_size + 20, sq_size, sq_size))
                                py.draw.rect(screen, "black", py.Rect((position.col)*sq_size + 20, (position.row)*sq_size + 20, sq_size, sq_size), 1)
                    else:
                        py.draw.rect(screen, color, py.Rect(c*sq_size + 20, r*sq_size + 20, sq_size, sq_size))
                else:
                    py.draw.rect(screen, color, py.Rect(c*sq_size + 20, r*sq_size + 20, sq_size, sq_size))

                    
    
    def draw_pieces(self, screen):
        images = load_images()
        for r in range(8):
            for c in range(8):
                piece = self.chess_set.board.board[r][c]
                if piece:
                    screen.blit(images[str(piece)], py.Rect(c*sq_size + 20, r*sq_size + 20, sq_size, sq_size))
                    

    # def from_algebraic(self,algebraic_notation):
    #     col = ord(algebraic_notation[0]) - ord('a')
    #     row = int(algebraic_notation[1])
    #     return Position(row,col)
    

    def move_touple(self, touple):
        row = int(touple[0])
        col = int(touple[1])
        return Position(row, col)



if __name__ == "__main__":
    chess_game = Chess()
    chess_game.start_game()
    