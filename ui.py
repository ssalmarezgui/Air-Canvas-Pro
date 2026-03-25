############# Barre de couleurs #############

import cv2
import numpy as np


COLOR_BOXES = [
    {"label": "Rouge", "color": (0,0, 255), "x": 20},
    {"label": "Vert", "color": (0, 255, 0), "x": 100},
    {"label": "Bleu", "color": (255, 0, 0), "x": 180},
    {"label": "Jaune", "color": (0, 255, 255), "x": 260},
    {"label": "Effacer", "color": (255, 255, 255), "x": 360},
]

def draw_header(img, active_color):
    cv2.rectangle(img, (0,0), (1280, 80), (30, 30, 30), -1) 
                #Haut-gauche,  Bas-droit   couleur BGR   pour remplir le contour
    for box in COLOR_BOXES:
        x = box['x']

        cv2.rectangle(img, (x,10), (x+60, 70), box['color'], -1) 

        if box['color'] == active_color:
            cv2.rectangle(img, (x-3,7), (x+63, 73), (255, 255, 255), 2)

    return img 