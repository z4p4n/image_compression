#!/usr/bin/python3.4

# Creation et ouverture d'image
# z4p4n, NexMat

from PIL import Image
import numpy as np

def create_image (img_name, width, height, X, Y, Z, yuv):
	# Creation de l'image
	img = Image.new ("RGB", (width, height), "black")

	if yuv == True :
		# On retrouve les valeurs RGB a partir des couleurs YUV
		for i in range (width * height) :
			R, G, B = YUV_to_RGB((X[i], Y[i], Z[i]))
			img.putpixel((int (i/height), i%height), (int(R), int(G), int(B)))
	else :
		for i in range (width * height) :
			img.putpixel((int (i/height), i%height), (int(X[i]), int(Y[i]), int(Z[i])))

	# Sauvegarde de l'image
	img.save(img_name + ".bmp", "bmp")
        
def read_image(img_name, yuv):

	# Ouverture de l'image 
	try:
		img = Image.open (img_name).convert ('RGB')
		width  = img.size[0]
		height = img.size[1]
	except:
		print ("Cannot open this image...")
		exit ()

	pix = img.load();

	matriceX = [0 for i in range (width * height)]
	matriceY = [0 for i in range (width * height)]
	matriceZ = [0 for i in range (width * height)]

	if yuv == True :
		for i in range (width) :
			for j in range (height) :
				X, Y, Z = RGB_to_YUV(pix[i,j])
				matriceX[i*height + j] = X
				matriceY[i*height + j] = Y
				matriceZ[i*height + j] = Z
	else :
		for i in range (width) :
			for j in range (height) :
				X, Y, Z = pix[i,j]
				matriceX[i*height + j] = X
				matriceY[i*height + j] = Y
				matriceZ[i*height + j] = Z

	return ((width, height), matriceX, matriceY, matriceZ);

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
