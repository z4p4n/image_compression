#!/usr/bin/python3.4

# Creation et ouverture d'image
# z4p4n, NexMat

from PIL import Image
import numpy as np

def create_image (img_name, width, height, Y, U, V):
	# Creation de l'image
	img = Image.new ("RGB", (width, height), "white")

	# On retrouve les valeurs RGB a partir des couleurs YUV
	for i in range (width * height) :
		R, G, B = YUV_to_RGB((Y[i], U[i], V[i]))
		img.putpixel((int (i/height), i%height), (int(R), int(G), int(B)))

	# Sauvegarde de l'image
	img.save(img_name + ".bmp", "bmp")
        
def read_image(img_name):
	# Ouverture de l'image 
	try:
		img = Image.open (img_name).convert ('RGB')
		width  = img.size[0]
		height = img.size[1]
	except:
		print ("Cannot open this image...")
		exit ()

	pix = img.load();

	matriceY = [0 for i in range (width * height)]
	matriceU = [0 for i in range (width * height)]
	matriceV = [0 for i in range (width * height)]
	for i in range (width) :
		for j in range (height) :
			Y, U, V = RGB_to_YUV(pix[i,j])
			matriceY[i*height + j] = Y
			matriceU[i*height + j] = U
			matriceV[i*height + j] = V
	return ((width, height), matriceY, matriceU, matriceV);

def YUV_to_byte (Y, U, V) :
	return (((int(Y)) >> 8) + 16,((int(U)) >> 8) + 128, ((int(V)) >> 8) + 128)

def byte_to_YUV (Y, U, V) :
	return (((Y - 16) << 8), int ((U - 128) << 8), int ((V - 128) << 8))

def RGB_to_YUV(triplet):
	vect = np.array([triplet[0], triplet[1], triplet[2]], float);
	matrice = np.array([
		[ 66 ,  129,  25 ],
		[-38 , -74 ,  112],
		[ 112, -94 , -18 ]]);
	res = np.dot(matrice, vect);
	return (res[0], res[1], res[2]);

def YUV_to_RGB(triplet):
	vect = np.array([triplet[0], triplet[1], triplet[2]], float);
	matrice = np.array([
		[ 66 ,  129,  25 ],
		[-38 , -74 ,  112],
		[ 112, -94 , -18 ]]);
	matrice = np.linalg.inv(matrice);
	res = np.dot(matrice, vect);
	return (res[0], res[1], res[2]);
