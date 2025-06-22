import cv2

def draw_queens_on_solution(image_path, cells_info, solution, queen_path="../queen.png", output_path="output/grid_with_queens.png"):
	img = cv2.imread(image_path)
	queen_img = cv2.imread(queen_path, cv2.IMREAD_UNCHANGED)  # Charge avec alpha si dispo

	n = len(solution)
	rows = {}
	threshold = 15
	for cell in cells_info:
		x, y, w, h, cx, cy, num = cell
		found = False
		for y_ref in rows:
			if abs(y - y_ref) < threshold:
				rows[y_ref].append(cell)
				found = True
				break
		if not found:
			rows[y] = [cell]
	sorted_rows = [sorted(rows[y], key=lambda c: c[0]) for y in sorted(rows)]
	for i, row in enumerate(sorted_rows):
		col = solution[i]
		x, y, w, h, cx, cy, num = row[col]
		# Redimensionner l'image de la reine à la taille de la case
		queen_resized = cv2.resize(queen_img, (w, h))
		# Gérer la transparence si présente
		if queen_resized.shape[2] == 4:
			alpha_s = queen_resized[:, :, 3] / 255.0
			alpha_l = 1.0 - alpha_s
			for c in range(0, 3):
				img[y:y+h, x:x+w, c] = (alpha_s * queen_resized[:, :, c] +
										alpha_l * img[y:y+h, x:x+w, c])
		else:
			img[y:y+h, x:x+w] = queen_resized
	cv2.imwrite(output_path, img)
