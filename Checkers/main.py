from ai import *
from board import *
import pygame
import sys


pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dame")
pygame.display.set_icon(pygame.image.load("assets/King_checkers.webp"))

FONT = pygame.font.Font(None, 74)
BUTTON_FONT = pygame.font.Font(None, 50)

NON_MANDATORY_TEXT = BUTTON_FONT.render("Opciono da se jede", True, WHITE)
MANDATORY_TEXT = BUTTON_FONT.render("Obavezno da se jede", True, WHITE)

NON_MANDATORY_BUTTON = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 150, 400, 100)
MANDATORY_BUTTON = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 50, 400, 100)

END_GAME_BUTTON = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 100)
END_GAME_FONT = pygame.font.Font(None, 50)


"""
------------------------------------------------------------------------------------------------------------------------
                                                MAIN GAME LOOP:
------------------------------------------------------------------------------------------------------------------------
"""


def main(jumps):
    hashmap = load_hashmap()
    mandatory_jumps = jumps
    board = Board(WINDOW)
    selected_piece = None
    all_valid_moves = board.get_all_valid_moves(WHITE_PIECE, mandatory_jumps)
    valid_moves = None
    red_field = None
    move_counter = 0
    turn = HUMAN
    clock = pygame.time.Clock()

    while True:

        if turn == COMPUTER:

            depth = variable_depth(all_valid_moves)
            optimal_move = (minimax(hashmap, board, depth, float('-inf'), float('inf'),
                                    True, all_valid_moves, mandatory_jumps))[1]
            if optimal_move is None:
                game_over("POBEDILI STE!!!", hashmap)
            red_field = optimal_move[1]

            board.move_piece(optimal_move)
            board.draw_board(WINDOW, red_field)
            move_counter += 1
            turn = HUMAN
            all_valid_moves = board.get_all_valid_moves(WHITE_PIECE, mandatory_jumps)
            print(f"VALID MOVES FOR WHITE: {all_valid_moves}")
            if smothered(all_valid_moves):
                game_over("IZGUBILI STE!!!", hashmap)
            result, notification = check_if_game_over(board, move_counter)
            if result:
                game_over(notification, hashmap)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                save_hashmap(hashmap)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == HUMAN:
                clicked_row, clicked_column = get_row_col_from_mouse(pygame.mouse.get_pos())

                if selected_piece:
                    for move in valid_moves:
                        if (clicked_row, clicked_column) == move[1]:

                            board.move_piece(move)
                            board.draw_board(WINDOW, red_field)
                            move_counter += 1
                            turn = COMPUTER
                            all_valid_moves = board.get_all_valid_moves(BLACK_PIECE, mandatory_jumps)
                            print(f"VALID MOVES FOR BLACK: {all_valid_moves}")
                            if smothered(all_valid_moves):
                                game_over("POBEDILI STE!!!", hashmap)
                            result, notification = check_if_game_over(board, move_counter)
                            if result:
                                game_over(notification, hashmap)

                    selected_piece = None
                    board.draw_board(WINDOW, red_field)

                else:
                    selected_piece = (select_piece(clicked_row, clicked_column, board.matrix))
                    print(f"SELECTED PIECE: {selected_piece}")
                    if selected_piece:
                        valid_moves = valid_moves_for_piece(selected_piece, all_valid_moves)
                        board.draw_board(WINDOW, red_field)
                        print(f"VALID MOVES FOR SELECTED: {valid_moves}")
                        board.draw_valid_moves(valid_moves, WINDOW)

        clock.tick(60)
        pygame.display.update()


def get_row_col_from_mouse(postion):
    return postion[1] // SQUARE_SIZE, postion[0] // SQUARE_SIZE


def valid_moves_for_piece(piece, all_valid_moves):
    res_moves = []
    for move in all_valid_moves:
        if move[0] == piece:
            res_moves += [move]
    return res_moves


"""
------------------------------------------------------------------------------------------------------------------------
                                                GAME ENDING FUNCTIONS
------------------------------------------------------------------------------------------------------------------------
"""


def game_over(notification, hashmap):
    draw_end_menu(notification)
    pygame.display.update()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                save_hashmap(hashmap)
                pygame.quit()
                sys.exit()


def draw_end_menu(notification):
    pygame.draw.rect(WINDOW, GOLD_CROWN, END_GAME_BUTTON)
    end_game_text = END_GAME_FONT.render(notification, True, BLACK)
    end_dest = (END_GAME_BUTTON.x + END_GAME_BUTTON.width // 2 - end_game_text.get_width() // 2,
                END_GAME_BUTTON.y + END_GAME_BUTTON.height // 2 - end_game_text.get_height() // 2)
    WINDOW.blit(end_game_text, end_dest)
    pygame.display.update()


"""
------------------------------------------------------------------------------------------------------------------------
                                                    MAIN MENU:
------------------------------------------------------------------------------------------------------------------------
"""


def main_menu():
    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NON_MANDATORY_BUTTON.collidepoint(event.pos):
                    mandatory_jumps = False
                    main(mandatory_jumps)
                if MANDATORY_BUTTON.collidepoint(event.pos):
                    mandatory_jumps = True
                    main(mandatory_jumps)


def draw_menu():
    draw_fields(WINDOW)

    pygame.draw.rect(WINDOW, BLACK, NON_MANDATORY_BUTTON)
    pygame.draw.rect(WINDOW, BLACK, MANDATORY_BUTTON)

    nm_dest = (NON_MANDATORY_BUTTON.x + NON_MANDATORY_BUTTON.width // 2 -
               NON_MANDATORY_TEXT.get_width() // 2, NON_MANDATORY_BUTTON.y
               + NON_MANDATORY_BUTTON.height // 2 - NON_MANDATORY_TEXT.get_height() // 2)
    WINDOW.blit(NON_MANDATORY_TEXT, nm_dest)

    m_dest = (MANDATORY_BUTTON.x + MANDATORY_BUTTON.width // 2 - MANDATORY_TEXT.get_width() // 2, MANDATORY_BUTTON.y
              + MANDATORY_BUTTON.height // 2 - MANDATORY_TEXT.get_height() // 2)
    WINDOW.blit(MANDATORY_TEXT, m_dest)

    pygame.display.update()


"""
------------------------------------------------------------------------------------------------------------------------
                                                    START GAME:
------------------------------------------------------------------------------------------------------------------------
"""

if __name__ == "__main__":
    main_menu()
