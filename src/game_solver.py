from grid_acquisition import *


def initialize_dic_placed(n):
	dic_placed = {}
	for i in range(1, n + 1):
		dic_placed[i] = 0
	return dic_placed


def is_color_placed(i, j, grid, dic_placed):
	return dic_placed[grid[i][j]] == 1


def are_color_respected(grid, solution):
	dic_placed = initialize_dic_placed(len(grid))
	# if solution == [3, 1, 4, 2, 6, 8, 5, 0, 7]:
	# 	print(grid)
	for i in range(len(solution)):
		# if solution == [3, 1, 4, 2, 6, 8, 5, 0, 7]:
		# 	print(f" i : {i} | solution = {solution[i]}")
		# 	print(f" color : {grid[solution[i]][i]} | placed = {dic_placed}")
		if dic_placed[grid[solution[i]][i]] == 1:
			return False
		else:
			dic_placed[grid[solution[i]][i]] = 1
	return True


def solve_n_queens_no_adjacent_diagonals(n, grid):
	solutions = []
	board = [-1] * n  # board[i] = colonne de la reine placée à la ligne i
	dic_placed = initialize_dic_placed(n)
	def is_safe(row, col):
		for prev_row in range(row):
			# Interdit même colonne
			if board[prev_row] == col:
				return False
			# Interdit cases voisines sur diagonale
			if abs(prev_row - row) == 1 and abs(board[prev_row] - col) == 1:
				return False

			if dic_placed[grid[row][col]] == 1:
				return False
		return True

	def backtrack(row=0):
		if row == n:
			solutions.append(board[:])
			return
		for col in range(n):
			if is_safe(row, col):
				board[row] = col
				backtrack(row + 1)
				board[row] = -1

	backtrack()
	return solutions


def get_solution(image_path):
	grid = analyze_grid(image_path)
	n = len(grid)
	solutions = solve_n_queens_no_adjacent_diagonals(n, grid)
	for sol in solutions:
		if are_color_respected(grid, sol):
			return sol


if __name__ == "__main__":
	get_solution("input/grid-2.png")

