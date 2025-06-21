import cv2
import numpy as np

def detecter_cases(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
	kernel = np.ones((3,3), np.uint8)
	thresh = cv2.dilate(thresh, kernel, iterations=1)
	contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cases = []
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		if w < 20 or h < 20 or w > img.shape[1]//2 or h > img.shape[0]//2:
			continue
		cases.append((x, y, w, h))
	return cases

def numeroter_couleurs(img, cases):
	color_dict = {}
	color_num = 1
	cases_infos = []
	for x, y, w, h in cases:
		cx, cy = x + w//2, y + h//2
		bgr = tuple(int(v) for v in img[cy, cx])
		if bgr not in color_dict:
			color_dict[bgr] = color_num
			color_num += 1
		num = color_dict[bgr]
		cases_infos.append((x, y, w, h, cx, cy, num))
	return cases_infos, color_dict

def annoter_image(img, cases_infos):
	output = img.copy()
	for x, y, w, h, cx, cy, num in cases_infos:
		cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.putText(output, str(num), (cx-10, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
	return output

def construire_grille_2d(cases_infos):
	# On regroupe par lignes (ordonnée y)
	lignes = {}
	seuil = 15
	for x, y, w, h, cx, cy, num in cases_infos:
		trouve = False
		for y_ref in lignes:
			if abs(y - y_ref) < seuil:
				lignes[y_ref].append((x, num))
				trouve = True
				break
		if not trouve:
			lignes[y] = [(x, num)]
	grille = []
	for y in sorted(lignes):
		ligne = [num for x, num in sorted(lignes[y])]
		grille.append(ligne)
	return grille

def analyser_grille(path_image):
	img = cv2.imread(path_image)
	cases = detecter_cases(img)
	cases_infos, color_dict = numeroter_couleurs(img, cases)
	img_annotee = annoter_image(img, cases_infos)
	cv2.imwrite('grille_avec_numeros_et_rectangles.png', img_annotee)
	grille_2d = construire_grille_2d(cases_infos)
	print("Grille 2D des numéros de couleurs :")
	for ligne in grille_2d:
		print(ligne)
	return grille_2d

# Utilisation :
grille = analyser_grille('queens-game-grid.png')
