import cv2
import numpy as np

def detect_cells(img):
	"""
	Detects all grid cells in the image using black lines as separators.

	Args:
		img (np.ndarray): Input BGR image.

	Returns:
		list: List of tuples (x, y, w, h) for each detected cell.
	"""
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
	kernel = np.ones((3,3), np.uint8)
	thresh = cv2.dilate(thresh, kernel, iterations=1)
	contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cells = []
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		if w < 20 or h < 20 or w > img.shape[1]//2 or h > img.shape[0]//2:
			continue
		cells.append((x, y, w, h))
	return cells

def number_colors(img, cells):
	"""
	Assigns a unique number to each color found at the center of the cells.

	Args:
		img (np.ndarray): Input BGR image.
		cells (list): List of cell bounding boxes.

	Returns:
		tuple: (list of cell info with color number, dict mapping BGR to color number)
	"""
	color_dict = {}
	color_num = 1
	cells_info = []
	for x, y, w, h in cells:
		cx, cy = x + w//2, y + h//2
		bgr = tuple(int(v) for v in img[cy, cx])
		if bgr not in color_dict:
			color_dict[bgr] = color_num
			color_num += 1
		num = color_dict[bgr]
		cells_info.append((x, y, w, h, cx, cy, num))
	return cells_info, color_dict

def annotate_image(img, cells_info):
	"""
	Draws a red rectangle and the color number on each cell.

	Args:
		img (np.ndarray): Input BGR image.
		cells_info (list): List of cell info with color number.

	Returns:
		np.ndarray: Annotated image.
	"""
	output = img.copy()
	for x, y, w, h, cx, cy, num in cells_info:
		cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.putText(output, str(num), (cx-10, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
	return output

def build_2d_grid(cells_info):
	"""
	Groups cells by rows and columns to build a 2D grid of color numbers.

	Args:
		cells_info (list): List of cell info with color number.

	Returns:
		list: 2D list (grid) of color numbers.
	"""
	rows = {}
	threshold = 15
	for x, y, w, h, cx, cy, num in cells_info:
		found = False
		for y_ref in rows:
			if abs(y - y_ref) < threshold:
				rows[y_ref].append((x, num))
				found = True
				break
		if not found:
			rows[y] = [(x, num)]
	grid = []
	for y in sorted(rows):
		row = [num for x, num in sorted(rows[y])]
		grid.append(row)
	return grid

def analyze_grid(image_path):
	"""
	Main function to analyze the grid in the image.

	Args:
		image_path (str): Path to the input image.

	Returns:
		list: 2D grid of color numbers.
	"""
	img = cv2.imread(image_path)
	cells = detect_cells(img)
	cells_info, color_dict = number_colors(img, cells)
	annotated_img = annotate_image(img, cells_info)
	cv2.imwrite('output/grid_with_numbers_and_rectangles.png', annotated_img)
	grid_2d = build_2d_grid(cells_info)
	return grid_2d

if __name__ == "__main__":
	grid = analyze_grid("input/grid-2.png")
