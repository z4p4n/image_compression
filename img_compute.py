#!/usr/bin/python3.4

# Creation et ouverture d'image
# z4p4n, NexMat

from PIL import Image
import numpy as np

def create_image (img_name, width, height, Y, U, V):
    # Creation de l'image
    img = Image.new ("RGB", (width, height))

    # On retrouve les valeurs RGB a partir des couleurs YUV
    for i in range (width * height) :
        R, G, B = YUV_to_RGB(Y[i], U[i], V[i])
        img.putpixel ((i/height, i%width), (R, G, B))

    # Sauvegarde de l'image
    img.save (img_name + ".bmp")
        
def read_image(img_name):
    # Ouverture de l'image 
    try:
        img = Image.open (img_name).convert ('RGB')
        width  = img.size[0]
        height = img.size[1]
        print(width, height);
    except:
        print ("Cannot open this image...")
        exit ()

    pix = img.load();
    print(pix);

    matriceY = [0 for i in range (width * height)]
    matriceU = [0 for i in range (width * height)]
    matriceV = [0 for i in range (width * height)]
    for i in range (width) :
        for j in range (height) :
            Y, U, V = RGB_to_YUV(pix[i,j])
            matriceY[i*height + j] = Y
            matriceU[i*height + j] = U
            matriceV[i*height + j] = V
     #matriceY = [[RGB_to_YUV(pix[i,j])[0] for j in range(height)] for i in range(width)]
    return ((width, height), matriceY, matriceU, matriceV);

def RGB_to_YUV(triplet):
    vect = np.array([triplet[0], triplet[1], triplet[2]], float);
    matrice = np.array([
            [ 0.299  ,  0.587  , 0.114   ],
            [-0.14713, -0.28886, 0.436   ],
            [ 0.615  , -0.51498, -0.10001]]);
    res = np.dot(matrice, vect);
    return (res[0], res[1], res[2]);

def YUV_to_RGB(triplet):
    vect = np.array([triplet[0], triplet[1], triplet[2]], float);
    matrice = np.array([
            [ 1,  0      ,  1.13983],
            [ 1, -0.39465, -0.58060],
            [ 1,  2.03211,  0      ]]);
    res = np.dot(matrice, vect);
    return (res[0], res[1], res[2]);


