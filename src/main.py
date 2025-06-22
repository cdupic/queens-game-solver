import cv2

from grid_acquisition import analyze_grid, number_colors, detect_cells
from game_solver import get_solution
from grid_output import draw_queens_on_solution


def get_solution_and_draw(image_path):
	grid = analyze_grid(image_path)
	n = len(grid)
	solution = get_solution(image_path)
	img = cv2.imread(image_path)
	cells = detect_cells(img)
	cells_info, _ = number_colors(img, cells)
	draw_queens_on_solution(image_path, cells_info, solution)
	return solution


if __name__ == "__main__":
	image_name = "grid-2.png"
	get_solution_and_draw("input/" + image_name)
