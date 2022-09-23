# -*- coding: utf-8 -*-
'''
Application du code de Hamming (7,4) aux chaînes de caractères et aux images
'''

from bitarray import bitarray
from scipy.stats import bernoulli
from pylab import imread, imshow, figure, array, resize, subplot, show, matrix, remainder, squeeze, asarray, fromfunction, gray, title

# Matrice de codage
G = matrix([[1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
# Matrice de correction
H = matrix([[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]])
# Matrice de décodage
R = matrix([[0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])
# Probabilité d'erreur
p = 0.01

# Transforme une image en une matrice de bits
def imageToBits(image):
    a = bitarray()
    a.frombytes(bytes(image.flatten()))
    m = matrix(a.tolist()) * 1
    m.resize((len(a) // 4, 4))
    return m.transpose()

# Transforme une matrice de bits en image
def bitsToImage(mat, shape):
    s = bitarray(squeeze(asarray(mat.transpose().flatten())).tolist()).tobytes()
    return resize(array(bytearray(s)).astype('uint8'), shape)

# Transforme une chaîne de caractères en matrice de bits
def stringToBits(byteString):
    a = bitarray()
    a.frombytes(byteString)
    m = matrix(a.tolist()) * 1
    m.resize((len(a) // 4, 4))
    return m.transpose()

# Transforme une matrice de bits en chaîne de caractères
def bitsToString(mat):
    return bitarray(squeeze(asarray(mat.transpose().flatten())).tolist()).tobytes()

# Ajoute une erreur suivant une loi de Bernoulli
def addError(mat, p):
    error = matrix(bernoulli.rvs(p, size=mat.size))
    error.resize(mat.shape)
    return mat + error

# Corrige les erreurs dans le signal codé
def correct(mat):
    S = remainder(H * mat, 2)
    pos = squeeze(asarray(matrix([4, 2, 1]) * S))
    cor = fromfunction(lambda i, j:i == pos - 1, mat.shape) * 1
    return mat + cor

# Affiche une image
def showimage(image):
    if image.ndim == 2:
        gray()
    imshow(image)

'''
Application du code de Hamming aux chaînes de caractères
'''

s = 'Ceci est un code de Hamming'
print ("Chaîne initiale :", s)
C = stringToBits(s.encode('latin-1'))  # Conversion chaîne->bits
E = addError(G * C, p)  # Codage et ajout d'une erreur
S = remainder(R * E, 2)  # Décodage sans correction
print ("Sans correction :", bitsToString(S).decode('latin-1'))
Z = remainder(R * correct(E), 2)  # Décodage avec correction
print ("Avec correction :", bitsToString(Z).decode('latin-1'))


'''
Application du code de Hamming aux images
'''

# Chargement de l'image        
image = imread("lena.jpg")

figure()

# Affichage de l'image initiale
subplot(131)
showimage(image)
title('Image initiale')

C = imageToBits(image)  # Conversion image->bits
E = addError(G * C, p)  # Codage et ajout d'une erreur
S = remainder(R * E, 2)  # Décodage sans correction
error = bitsToImage(S, image.shape)  # conversion bits->image

# Affichage de l'image sans correction 
subplot(132)
showimage(error)
title('Image sans correction')

Z = remainder(R * correct(E), 2)  # Décodage avec correction 
result = bitsToImage(Z, image.shape)  # conversion bits->image

# Affichage de l'image sans correction 
subplot(133)
showimage(result)
title('Image avec correction')

show()
