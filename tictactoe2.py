from typing import List, Tuple, Union
from collections import deque
from time import sleep
import os
import sys
import numpy as np

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_progress(current_step: int, total_steps: int):
    completed_blocks = int((current_step / total_steps) * 50)
    percentage = round((current_step / total_steps) * 100, 1)
    bar = 'Progress: ' + f'{percentage}%' + ' [\033[32m' + \
          '#' * completed_blocks + ' ' * (50 - completed_blocks) + '\033[0m]'
    
    sys.stdout.write("\033[0;0H")
    sys.stdout.write(bar)
    sys.stdout.write('\n')
    sys.stdout.flush()

def display_board(board: List[List[int]], column_offset=0):
    RED, GREEN, RESET = "\033[31m", "\033[32m", "\033[0m"
    
    formatted_board = [[' ' if cell is None else RED + str(cell) + RESET if cell == 'X' else GREEN + str(cell) + RESET for cell in row] for row in board]

    board_view = f' {formatted_board[0][0]} | {formatted_board[0][1]} | {formatted_board[0][2]}\n'
    board_view += '-----------\n'
    board_view += f' {formatted_board[1][0]} | {formatted_board[1][1]} | {formatted_board[1][2]}\n'
    board_view += '-----------\n'
    board_view += f' {formatted_board[2][0]} | {formatted_board[2][1]} | {formatted_board[2][2]}\n'

    sys.stdout.write(f"\033[{column_offset};0H")
    sys.stdout.write(board_view)
    sys.stdout.flush()

def play_sequence(moves: list, column_offset=0, initial_state=None):
    if initial_state is None:
        initial_state = [[None for _ in range(3)] for _ in range(3)]
        
    for row, col, player in moves:
        initial_state[row][col] = player
        display_board(initial_state, column_offset)
        sleep(0.5)

def check_win(player: str, board: List[List[str]]) -> bool:
    win_conditions = [0, 0, 0, 0]  # row, column, forward diagonal, backward diagonal

    for i in range(3):
        for j in range(3):
            win_conditions[0] += 1 if board[i][j] == player else 0
            win_conditions[1] += 1 if board[j][i] == player else 0
        
        if win_conditions[0] == 3 or win_conditions[1] == 3:
            return True
        win_conditions[0], win_conditions[1] = 0, 0
        
        win_conditions[2] += 1 if board[i][2 - i] == player else 0
        win_conditions[3] += 1 if board[i][i] == player else 0

    return any(count == 3 for count in win_conditions)

def bfs_search(starting_player: str, winning_player: str, initial_state=None) -> list:
    if initial_state is None:
        initial_state = [[None for _ in range(3)] for _ in range(3)]
    
    current_player = starting_player
    moves_queue = deque()
    state_queue = deque()
    steps_explored = 0
    
    change_player = lambda p: 'X' if p == 'O' else 'O'

    for pos in range(9):
        row, col = divmod(pos, 3)
        steps_explored += 1
        if initial_state[row][col] is not None:
            continue
        new_state = [row.copy() for row in initial_state]
        new_state[row][col] = current_player

        path = moves_queue.copy()
        path.append((row, col, current_player))
        state_queue.append((path, new_state))

    while state_queue:
        path, state = state_queue.popleft()
        current_player = change_player(path[-1][2])
        steps_explored += 1

        random_positions = np.arange(9)
        np.random.shuffle(random_positions)

        for pos in random_positions:
            row, col = divmod(pos, 3)
            if state[row][col] is not None:
                continue
            new_state = [r.copy() for r in state]
            new_state[row][col] = current_player

            path = path.copy()
            path.append((row, col, current_player))

            display_board(new_state)
            if current_player != winning_player and check_win(current_player, new_state):
                continue
            if current_player == winning_player and check_win(current_player, new_state):
                return path, steps_explored

            state_queue.append((path, new_state))

    return None, None

def depth_first_search(starting_player: str, winning_player: str, initial_state=None, max_depth=9, use_iterative_deepening=False) -> list:
    if initial_state is None:
        initial_state = [[None for _ in range(3)] for _ in range(3)]
    
    def dfs_helper(depth, move_path, state):
        current_player = 'X' if move_path[-1][2] == 'O' else 'O'
        random_positions = np.arange(9)
        np.random.shuffle(random_positions)

        nonlocal steps_explored
        steps_explored += 1
        
        for pos in random_positions:
            row, col = divmod(pos, 3)
            if state[row][col] is not None:
                continue

            new_state = [r.copy() for r in state]
            new_path = move_path.copy()
            new_state[row][col] = current_player
            new_path.append((row, col, current_player))

            display_board(new_state, 15 if use_iterative_deepening else 8)
            if current_player != winning_player and check_win(current_player, new_state):
                return None
            if current_player == winning_player and check_win(current_player, new_state):
                return new_path

            if depth < max_depth:
                result = dfs_helper(depth + 1, new_path, new_state)
                if result is not None:
                    return result

        return None

    steps_explored = 0
    random_positions = np.arange(9)
    np.random.shuffle(random_positions)

    for pos in random_positions:
        row, col = divmod(pos, 3)
        if initial_state[row][col] is not None:
            continue
        steps_explored += 1

        new_state = [r.copy() for r in initial_state]
        new_state[row][col] = starting_player
        move_path = deque([(row, col, starting_player)])
        found_path = dfs_helper(1, move_path, new_state)
        if found_path:
            return found_path, steps_explored

    return None, None

def iterative_deepening_search(starting_player: str, winning_player: str, initial_state=None) -> list:
    if initial_state is None:
        initial_state = [[None for _ in range(3)] for _ in range(3)]

    for depth in range(2, 10):
        found_path, steps_explored = depth_first_search(starting_player, winning_player, initial_state, depth, True)
        if found_path:
            return found_path, steps_explored

def main():
    starting_player = input('Choose the starting player (X/O): ')
    winning_player = input('Choose the player to win (X/O): ')

    print('Enter the initial board state (- for empty):')
    initial_state = [list(map(lambda cell: None if cell == '-' else cell, input().split())) for _ in range(3)]

    if starting_player not in ['X', 'O'] or winning_player not in ['X', 'O'] or any(len(row) < 3 for row in initial_state):
        raise ValueError('Invalid input')

    node_counts = [0] * 3
    print('Running BFS...')
    sleep(1)
    clear_screen()

    path, node_counts[0] = bfs_search(starting_player, winning_player, [r.copy() for r in initial_state])

    if not path:
        print('No solution found using BFS')
        sleep(1)
    else:
        print('Replaying BFS...')
        sleep(1)
        play_sequence(path, initial_state=[r.copy() for r in initial_state])

    print('Running DFS...')
    sleep(0.5)

    path, node_counts[1] = depth_first_search(starting_player, winning_player, [r.copy() for r in initial_state])

    if not path:
        print('No solution found using DFS')
        sleep(0.5)
    else:
        print('Replaying DFS...')
        sleep(1)
        play_sequence(path, 8, [r.copy() for r in initial_state])

    print('Running IDS...')
    sleep(0.5)

    path, node_counts[2] = iterative_deepening_search(starting_player, winning_player, [r.copy() for r in initial_state])

    if not path:
        print('No solution found using IDS')
        sleep(0.5)
    else:
        print('Replaying IDS...')
        sleep(1)
        play_sequence(path, 15, [r.copy() for r in initial_state])

    show_progress(node_counts[1], sum(node_counts))

if __name__ == '__main__':
    main()
