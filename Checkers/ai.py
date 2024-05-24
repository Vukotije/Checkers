from copy import deepcopy
from board import *
import os
import json


def load_hashmap():
    if os.path.exists(HASHMAP_FILE):
        with open(HASHMAP_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_hashmap(hashmap):
    with open(HASHMAP_FILE, 'w') as file:
        json.dump(hashmap, file)


def minimax(hashmap, board, depth, alpha, beta, maximizing_player, all_possible_moves, mandatory_jumps):
    board_key = ''.join(''.join(row) for row in board.matrix)

    if board_key in hashmap:
        return hashmap[board_key]

    if depth == 0 or (check_if_game_over(board, move_counter=0))[0] or smothered(board):
        vl = board.calculate_heuristics()
        return vl, None

    optimal_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in all_possible_moves:
            board_copy = deepcopy(board)
            board_copy.move_piece(move)
            value, _ = minimax(hashmap, board_copy, depth - 1, alpha, beta, False,
                               board_copy.get_all_valid_moves(WHITE_PIECE, mandatory_jumps), mandatory_jumps)
            if value > max_eval:
                max_eval = value
                optimal_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        hashmap[board_key] = (max_eval, optimal_move)
        return max_eval, optimal_move

    else:
        min_eval = float('inf')
        all_possible_moves = board.get_all_valid_moves(WHITE_PIECE, mandatory_jumps)
        for move in all_possible_moves:
            board_copy = deepcopy(board)
            board_copy.move_piece(move)
            value, _ = minimax(hashmap, board_copy, depth - 1, alpha, beta, True,
                               board_copy.get_all_valid_moves(BLACK_PIECE, mandatory_jumps), mandatory_jumps)
            if value < min_eval:
                min_eval = value
                optimal_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        hashmap[board_key] = (min_eval, optimal_move)
        return min_eval, optimal_move
