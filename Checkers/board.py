from constants import *
import pygame


def draw_fields(window, red_field=None):
    window.fill(LIGHT_BG)
    for row in range(ROWS):
        for column in range(COLUMNS):
            if (row + column) % 2 == 1:
                position_and_size = (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(window, DARK_BG, position_and_size)
    if red_field:
        row, column = red_field
        position_and_size = (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(window, RED, position_and_size)


def variable_depth(all_valid_moves):
    num_moves = len(all_valid_moves)
    if num_moves <= 4:
        return 7
    elif num_moves <= 8:
        return 6
    elif num_moves <= 12:
        return 5
    else:
        return 4


def select_piece(row, column, matrix):
    piece = matrix[row][column]
    if piece in [WHITE_PIECE, WHITE_QUEEN]:
        return row, column
    return None


def smothered(all_valid_moves):
    if all_valid_moves:
        return False
    return True


def check_if_game_over(board, move_counter):
    if move_counter >= 150:
        return True, "NERESENO!!!"
    elif board.white_count <= 0:
        return True, "IZGUBILI STE!!!"
    elif board.black_count <= 0:
        return True, "POBEDILI STE!!!"
    else:
        return False, None


"""
------------------------------------------------------------------------------------------------------------------------
                                                    BOARD CLASS:
------------------------------------------------------------------------------------------------------------------------
"""


class Board(object):
    def __init__(self, window):
        self.matrix = self.initialize_matrix_setup()
        self.white_count = self.black_count = 12
        self.draw_board(window, red_field=None)

    @staticmethod
    def initialize_matrix_setup():
        matrix = []
        for original_row in range(ROWS):
            current_row = []
            for original_column in range(COLUMNS):
                if (original_row + original_column) % 2 == 1:
                    if original_row < 3:
                        current_row.append(BLACK_PIECE)
                        continue
                    elif original_row > 4:
                        current_row.append(WHITE_PIECE)
                        continue
                current_row.append(EMPTY)
            matrix.append(current_row)
        return matrix

    def get_all_valid_moves(self, piece_type, mandatory_jumps):
        all_valid_moves = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.matrix[row][column]
                directions = self._get_directions(piece)
                if piece in [piece_type.lower(), piece_type.upper()]:
                    move = self._get_piece_moves(row, column, directions, piece_type)
                    if move:
                        all_valid_moves += move

        if mandatory_jumps:
            jumping_moves = []
            for move in all_valid_moves:
                if move[2]:
                    jumping_moves.append(move)
            if jumping_moves:
                return jumping_moves

        return all_valid_moves

    def move_piece(self, move):
        curent_position, new_position, captured = move
        current_row, current_column = curent_position
        new_row, new_column = new_position
        self.matrix[new_row][new_column] = self.matrix[current_row][current_column]
        self.matrix[current_row][current_column] = EMPTY

        if captured:
            self.remove_piece(captured)

        if new_row == 0 and self.matrix[new_row][new_column] == WHITE_PIECE:
            self.matrix[new_row][new_column] = WHITE_QUEEN

        if new_row == 7 and self.matrix[new_row][new_column] == BLACK_PIECE:
            self.matrix[new_row][new_column] = BLACK_QUEEN

    def remove_piece(self, pieces_cords):
        for piece_cords in pieces_cords:
            row, column = piece_cords
            self.matrix[row][column] = EMPTY

            piece = self.matrix[row][column]
            if piece in [WHITE_PIECE, WHITE_QUEEN]:
                self.white_count -= 1
            if piece in [BLACK_PIECE, BLACK_QUEEN]:
                self.black_count -= 1

    def calculate_heuristics(self):
        white_score = 0
        black_score = 0

        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.matrix[row][column]
                if piece != EMPTY:
                    if piece == WHITE_PIECE:
                        white_score += PIECE_VALUE + PIECE_DISTANCE_VALUE * (ROWS - row - 1)
                        if 2 <= row <= 5 and 2 <= column <= 5:
                            white_score += CENTER_CONTROL_VALUE
                    elif piece == WHITE_QUEEN:
                        white_score += QUEEN_VALUE
                        if 2 <= row <= 5 and 2 <= column <= 5:
                            white_score += CENTER_CONTROL_VALUE

                    elif piece == BLACK_PIECE:
                        black_score += PIECE_VALUE + PIECE_DISTANCE_VALUE * row
                        if 2 <= row <= 5 and 2 <= column <= 5:
                            black_score += CENTER_CONTROL_VALUE
                    elif piece == BLACK_QUEEN:
                        black_score += QUEEN_VALUE
                        if 2 <= row <= 5 and 2 <= column <= 5:
                            black_score += CENTER_CONTROL_VALUE

        return black_score - white_score

    """
    -------------------------------------------------------------------------------------------------------------------
                                                    HELPER METHODS:
    -------------------------------------------------------------------------------------------------------------------
    """

    def _get_piece_moves(self, row, column, directions, piece):
        moves = []
        for d in directions:
            new_row, new_column = row + d[0], column + d[1]
            if self._is_within_bounds(new_row, new_column):
                if self.matrix[new_row][new_column] == EMPTY:
                    moves.append(((row, column), (new_row, new_column), []))
                elif self.matrix[new_row][new_column] not in [piece.lower(), piece.upper()]:
                    jump_row, jump_column = new_row + d[0], new_column + d[1]
                    if self._is_within_bounds(jump_row, jump_column) and self.matrix[jump_row][jump_column] == EMPTY:
                        moves.append(((row, column), (jump_row, jump_column), [(new_row, new_column)]))
                        self._get_jump_moves(row, column, jump_row, jump_column,
                                             moves, piece, [(new_row, new_column)], directions)
        return moves

    def _get_jump_moves(self, original_row, original_column, row, column, moves, piece, captured, directions):
        for d in directions:
            new_row, new_column = row + d[0], column + d[1]
            if self._is_within_bounds(new_row, new_column):
                if (self.matrix[new_row][new_column] not in [piece.lower(), piece.upper()]
                        and self.matrix[new_row][new_column] != EMPTY):
                    jump_row, jump_column = new_row + d[0], new_column + d[1]
                    if self._is_within_bounds(jump_row, jump_column) and self.matrix[jump_row][jump_column] == EMPTY:
                        new_captured = captured + [(new_row, new_column)]
                        if (jump_row, jump_column) not in [move[1] for move in moves]:
                            moves.append(((original_row, original_column), (jump_row, jump_column), new_captured))
                            self._get_jump_moves(original_row, original_column, jump_row,
                                                 jump_column, moves, piece, new_captured, directions)

    @staticmethod
    def _get_center_coordinates(row, column):
        return column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2

    @staticmethod
    def _get_directions(piece):
        vertical = []
        if piece == WHITE_PIECE:
            vertical.append(UP)
        elif piece == BLACK_PIECE:
            vertical.append(DOWN)
        else:
            vertical.append(UP)
            vertical.append(DOWN)
        directions = []
        for h in HORIZONTAL:
            for v in vertical:
                directions.append([v, h])
        return directions

    @staticmethod
    def _is_within_bounds(row, column):
        return 0 <= row < ROWS and 0 <= column < COLUMNS

    """
    -------------------------------------------------------------------------------------------------------------------
                                                        GUI:
    -------------------------------------------------------------------------------------------------------------------
    """

    def draw_board(self, window, red_field):
        draw_fields(window, red_field)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.matrix[row][column]
                if piece != EMPTY:
                    color = BLACK if piece in [BLACK_QUEEN, BLACK_PIECE] else WHITE
                    pygame.draw.circle(window, color, self._get_center_coordinates(row, column), PIECE_RADIUS)
                    if piece in [BLACK_QUEEN, WHITE_QUEEN]:
                        crown_color = GOLD_CROWN if piece == BLACK_QUEEN else SILVER_CROWN
                        pygame.draw.circle(window, crown_color, self._get_center_coordinates(row, column), SMALL_RADIUS)

    def draw_valid_moves(self, moves, window):
        for move in moves:
            destination = move[1]
            pygame.draw.circle(window, BLUE, self._get_center_coordinates(destination[0], destination[1]), SMALL_RADIUS)

    """
    -------------------------------------------------------------------------------------------------------------------
                                                    GETERS AND SETERS:
    -------------------------------------------------------------------------------------------------------------------
    """

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, new_board):
        self._matrix = new_board
