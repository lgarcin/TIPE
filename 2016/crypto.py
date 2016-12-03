from random import randint
from string import ascii_lowercase
from math import log
from numpy import argmax

alphabet = ascii_lowercase

frequencies = {
    'a': 0.0942,
    'b': 0.0102,
    'c': 0.0264,
    'd': 0.0339,
    'e': 0.1587,
    'f': 0.0095,
    'g': 0.0104,
    'h': 0.0077,
    'i': 0.0841,
    'j': 0.0089,
    'k': 1e-6,
    'l': 0.0534,
    'm': 0.0324,
    'n': 0.0715,
    'o': 0.0514,
    'p': 0.0286,
    'q': 0.0106,
    'r': 0.0646,
    's': 0.0790,
    't': 0.0726,
    'u': 0.0624,
    'v': 0.0215,
    'w': 1e-6,
    'x': 0.0030,
    'y': 0.0024,
    'z': 0.0032
}


def caesar(s, shift):
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    return s.translate(str.maketrans(alphabet, shifted_alphabet))


def energy(s):
    return sum([s.count(c) * log(frequencies[c]) for c in alphabet if frequencies[c] > 0])


#message = 'comment allez vous moi je vais bien et vous merci de toute facon je m en vais que me dites vous la mais c est incroyable saperlipopette ca ne marche pas tres bien enfin je vais encore essayer mais bon j ai des doutes'
message = "ce qui se concoit bien s'enonce clairement et les mots pour le dire arrivent aisement"
shift = randint(0, 25)
code = caesar(message, shift)
print(code)

prob = []
for k in range(26):
    s = caesar(code, -k)
    prob.append(energy(s))
ind = argmax(prob)
print(caesar(code, -ind))
