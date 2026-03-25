import cv2
import numpy as np

def draw_on_canvas(canvas, prev_pt, curr_pt, color, thickness=15):
    if prev_pt and curr_pt:
        cv2.line(canvas, prev_pt, curr_pt, color, thickness)

    return canvas

def erase(canvas, point, size=80):
    if point:
        cv2.circle(canvas, point, size, (0, 0, 0), -1)
    return canvas


def clear_canvas(canvas):
    canvas[:] = 0
    return canvas

# frame : l'img en temps reel de ma webcam , ma main 
# canvas : l'img noire sur laquelle je dessines mes traits de couleur
def overlay(frame, canvas):
    mask = canvas.astype(bool)
    result = frame.copy()
    result[mask] = canvas[mask] # Regarde mon masque. Partout où c'est True (là où j'ai dessiné), prends le pixel coloré du canvas et colle-le exactement au même endroit sur mon image result


    return result # ce que affiche le cam avec le dessin