from typing import List, Tuple, Union
from collections import deque
from time import sleep
import sys
import os
import numpy as np

def clr(): 
    if os.name == 'nt':  os.system('cls') 
    else: os.system('clear')

def progress(current: int, total: int): 
    num_done = int((current / total) * 50) 
    percent = round((current / total) * 100, 1)
    progress = 'Progress: ' + str(percent) + ' [\033[32m' + \
         ''.join('#' for _ in range(num_done)) + ''.join(' ' for _ in range(50 - num_done)) + '\033[0m]'
        

    sys.stdout.write("\033[0;0H")
    sys.stdout.write(progress)
    sys.stdout.write('\n')
    sys.stdout.flush()

    

def print_state(state: List[List[int]], col = 0):
    RED = "\033[31m"
    GREEN = "\033[32m" 
    RESET = "\033[0m" 
    s = [[' ' if j is None else RED + str(j) + RESET if j == 'X' else GREEN + str(j) + RESET for j in i] for i in state]

    string = f' {s[0][0]} | {s[0][1]} | {s[0][2]}\n'
    string += '-----------\n'
    string += f' {s[1][0]} | {s[1][1]} | {s[1][2]}\n'
    string += '-----------\n'
    string += f' {s[2][0]} | {s[2][1]} | {s[2][2]}\n'

    sys.stdout.write(f"\033[{col};0H")
    sys.stdout.write(string)
    sys.stdout.flush()

def replay(path: list, col = 0, initial_state = [[None for _ in range(3)] for _ in range(3)]): 

    for i, j, p in path: 
        initial_state[i][j] = p
        print_state(initial_state, col)
        sleep(0.5)
    


#goal state
def is_winning(player: str, board: List[List[str]]) -> bool: 
    win = [0, 0, 0, 0] #x-axis, y-axis, forward diagonal, backward diagonal

    for i in range(3): 
        for j in range(3): 
            win[0] += 1 if board[i][j] == player else 0 
            win[1] += 1 if board[j][i] == player else 0
        
        if win[0] == 3 or win[1] == 3: return True
        win[0], win[1] = 0, 0

        win[2] += 1 if board[i][2 - i] == player else 0 
        win[3] += 1 if board[i][i] == player else 0 

    return any(w == 3 for w in win) 



def bfs(starting_player: str,  winning_player: str, initial_state = [[None for _ in range(3)] for _ in range(3)]) -> list: 
    
    player = starting_player
    path = deque() 
    q = deque() 
    current_path = None
    complexity = 0
    
    switch_player = lambda p : 'X' if p == 'O' else 'O'

    for x in range(9): 
        i, j = x // 3, x % 3
        complexity += 1
        if initial_state[i][j] is not None: continue
        new_state = [r.copy() for r in initial_state]
        new_state[i][j] = player

        current_path = path.copy()
        current_path.append((i, j, player))
        q.append((current_path, new_state))


    while q: 
        path, state = q.popleft()
        player = switch_player(path[-1][2])
        complexity += 1

        # progress(num_done, len(q) + num_done)
        random = np.arange(9)
        np.random.shuffle(random)

        for x in random: 
            i, j = x // 3, x % 3

            if state[i][j] is not None: continue
            new_state = [r.copy() for r in state]
            new_state[i][j] = player


            current_path = path.copy()
            current_path.append((i, j, player))


            print_state(new_state)
            if player != winning_player and is_winning(player, new_state): 
                continue
            
            if player == winning_player and is_winning(player, new_state): 
                return (list(current_path), complexity)

        
            q.append((current_path, new_state))

    return (None, None)


def dfs(starting_player: str, winning_player: str, initial_state =  [[None for _ in range(3)] for _ in range(3)], max_depth = 9, ids = False) -> list: 
    switch_player = lambda p : 'X' if p == 'O' else 'O'
    complexity = 0



    def _dfs(depth, path:deque, state: List[List[int]]) -> Union[list, None]: 
        player = switch_player(path[-1][2])
        random = np.arange(9)
        np.random.shuffle(random)

        nonlocal complexity; complexity += 1
        for x in random: 
            i, j = x // 3, x % 3
            if state[i][j] is not None: continue

            new_state = [s.copy() for s in state]
            new_path = path.copy()

            new_state[i][j] = player
            new_path.append((i, j, player)) 

            print_state(new_state, 15 if ids else 8 )
            if player != winning_player and is_winning(player, new_state): 
                return None
                
            if player == winning_player and is_winning(player, new_state): 
                return list(new_path)

            if depth < max_depth:  
                dfs_path = _dfs(depth + 1, new_path, new_state)
                if dfs_path is not None: 
                    return dfs_path
            
        return None

    random = np.arange(9)
    np.random.shuffle(random)

    for x in random: 
        i, j = x // 3, x % 3
        if initial_state[i][j] is not None: continue
        complexity += 1        

        new_state = [s.copy() for s in initial_state]
        new_state[i][j] = starting_player
        new_path = deque()
        new_path.append((i, j, starting_player))
        dfs_path = _dfs(1, new_path, new_state)
        if dfs_path is not None: 
            return dfs_path, complexity 
        
    return (None, None)


def ids(starting_player: str, winning_player: str, initial_state =  [[None for _ in range(3)] for _ in range(3)]) -> list:
    for i in range(2, 10): 
        path, complexity = dfs(starting_player, winning_player, initial_state, i, True)
        if path is not None: 
            return path, complexity
    



def main(): 
    starting_player = input('Select your starting player (X/O): ')
    winning_player = input('Select the player you want to win (X/O): ')

    print('Enter the initial state (- for empty space):')
    initial_state = [list(map(lambda x: None if x == '-' else x, input().split())) for _ in range(3)]

    breakpoint()
    if starting_player not in ['X', 'O'] or winning_player not in ['X', 'O'] or any(len(r) < 3 for r in initial_state): 
        raise ValueError('Incorrect Inputs')
    
    
    complexity = [0 for _ in range(3)]
    print('Running bfs...')
    sleep(1)
    clr()

    path, complexity[0]= bfs(starting_player, winning_player, [r.copy() for r in initial_state])


    if not path: 
        print('Could not find path with bfs')
        sleep(1)
    else: 
        print('Replaying....')
        sleep(1)
        replay(path, initial_state=[r.copy() for r in initial_state])


    print('Running dfs...')
    sleep(0.5)

    path, complexity[1]= dfs(starting_player,  winning_player, [r.copy() for r in initial_state])

    if not path: 
        print('Could not find path with dfs')
        sleep(0.5)
    else: 
        print('Replaying....')
        sleep(1)
        replay(path, 8, [r.copy() for r in initial_state])


    print('Running ids...')
    sleep(0.5)

    path, complexity[2]= ids(starting_player, winning_player, [r.copy() for r in initial_state])

    if not path: 
        print('Could not find path with ids')
        sleep(0.5)

    else: 
        print('Replaying....')
        sleep(0.5)
        replay(path, 15, [r.copy() for r in initial_state])
    
    print(f'Total Nodes Explored: \nBFS: {complexity[0]}\nDFS: {complexity[1]}\nIDS: {complexity[2]}')

if __name__ == '__main__': 
    main()






    

