#!/usr/bin/env python3
"""A Kakurasu solver.

Represents a Kakurasu board as a 2D list of bools with lists of ints for the target values.

Usage:
    Put the dimensions and target values of your puzzle in `conf.json`.

    Then run the program.
    `python3 kakarasu.py`
"""

from copy import deepcopy #copies boards in recursive solve
from json import load #reads conf.json
from ast import literal_eval #reads arrays in json

def main():
    """Reads board configuration from conf.json and solves the board."""
    with open('conf.json') as f:
        conf = load(f)
        board = [[False]*conf['dim'] for _ in range(conf['dim'])]
        hor = literal_eval(conf['hor'])
        ver = literal_eval(conf['ver'])
        solution = solve(board, hor, ver, 0)
        if solution is None:
            print('No solution.')
            print_board(board, hor, ver)
        else:
            print('Solved.')
            print_board(solution, hor, ver)

def naturals(target, depth):
    """Finds natural number expansions for target from 1 to depth.

    Args:
        target (int): The sum to expand.
        depth (int): The maximum natural to use in expansion.

    Returns:
        bool[][]: A list of valid natural number expansions for target in board form.
    """
    terms = []
    truth = 2**depth
    for i in range(target, truth):
        binary = format(i, '{}b'.format(depth))
        sum = 0
        for j in range(len(binary)):
            if binary[j] == '1':
                sum += depth - j
        if sum == target:
            terms.append([x == '1' for x in binary[::-1]])
    return terms

def state(board, hor, ver):
    """Checks if a board is solved, invalid, or unfinished.

    Args:
        board (bool[][]): Kakurasu board.
        hor (int[]): Horizontal target values.
        ver (int[]): Vertical target values.

    Returns:
        int: zero = solved, positive = invalid, negative = unfinished
    """
    if board is not None:
        for i in range(len(board)):
            vers = 0
            for j in range(len(board[i])):
                if board[j][i]:
                    vers += j + 1
            if vers != ver[i]:
                return vers - ver[i]
        return 0

def solve(board, hor, ver, row):
    """Recursively solves a Kakurasu board.

    Args:
        board (bool[][]): Kakurasu board.
        hor (int[]): Horizontal target values.
        ver (int[]): Vertical target values.
        row (int): Current row being worked on.

    Returns:
        bool[][]: Solved board or None if no solution.
    """
    if board is not None:
        curstate = state(board, hor, ver)
        if curstate > 0: #Skips paths with bad colums
            return None
        if curstate == 0: #Returns solved puzzle
            return board
        choices = naturals(hor[row], len(board[row]))
        for i in choices:
            newboard = deepcopy(board)
            newboard[row] = i
            if row < len(board) - 1: #Stops when out of rows
                newboard = solve(newboard, hor, ver, row+1) #Recursive call
            if state(newboard, hor, ver) == 0: #Returns solved puzzle
                return newboard

def print_board(board, hor, ver):
    """Prints a graphical representation of a Kakurasu board to the command line.

    Args:
        board (bool[][]): Kakurasu board
        hor (int[]): Horizontal target values
        ver (int[]): Vertical target values
    """
    print('  ', end='')
    for i in range(len(board)):
        print(i+1, end=' ')
    print()
    for i in range(len(board)):
        print(i+1, end=' ')
        for j in range(len(board[i])):
            if board[i][j]:
                print('+', end=' ')
            else:
                print('-', end=' ')
        print(hor[i])
    print('  ', end='')
    for i in range(len(board)):
        print(ver[i], end=' ')
    print()

if __name__ == '__main__':
    main()