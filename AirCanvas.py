import cv2
import numpy as np
from ui import COLOR_BOXES, draw_header
from HandTrackingModule import get_landmarks, fingers_up
from canvas import draw_on_canvas, overlay, erase

######### CONFIGURATION ##########
WIDTH, HEIGHT = 1280, 720
BRUSH_THICKNESS = 15
ERASER_THICKNESS = 80 # Plus gros pour effacer vite

COLORS = {
    "Rouge": (0,0,255),
    "Vert": (0,255,0),
    "Bleu": (255,0,0),
    "Jaune": (0,255,255),
}

CURRENT_COLOR = COLORS['Rouge']
canvas = np.zeros((HEIGHT, WIDTH, 3), dtype = np.uint8)
prev_point = None


def get_selected_color(lm_list, current_color):
    if len(lm_list) == 0: return current_color
    x_index, y_index = lm_list[8][1], lm_list[8][2]

    if y_index < 80:
        for i, box in enumerate(COLOR_BOXES):
            if box['x'] < x_index < box['x'] + 60:
                if i == 4: return (0, 0, 0) 
                return box['color']
    return current_color

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)

    lm_list = get_landmarks(img)

    if len(lm_list) != 0: 
        fingers = fingers_up(lm_list)

        # 1. MODE SÉLECTION (2 doigts : Index + Majeur)
        if fingers[1] == 1 and fingers[2] == 1:
            prev_point = None 
            CURRENT_COLOR = get_selected_color(lm_list, CURRENT_COLOR)
            
            # Feedback visuel : Cercle blanc entre les doigts
            cx, cy = (lm_list[8][1] + lm_list[12][1]) // 2, (lm_list[8][2] + lm_list[12][2]) // 2
            cv2.circle(img, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

        # 2. MODE DESSIN OU GOMME (1 doigt : Index seul)
        elif fingers[1] == 1 and fingers[2] == 0:
            curr_point = (lm_list[8][1], lm_list[8][2])
            if prev_point is None: prev_point = curr_point

            if CURRENT_COLOR == (0, 0, 0): 
               
                cv2.line(canvas, prev_point, curr_point, (0,0,0), ERASER_THICKNESS)
                
                cv2.circle(img, curr_point, ERASER_THICKNESS // 2, (255, 255, 255), 2)
            else:
                cv2.line(canvas, prev_point, curr_point, CURRENT_COLOR, BRUSH_THICKNESS)
                # On dessine un point plein sur le doigt
                cv2.circle(img, curr_point, 10, CURRENT_COLOR, cv2.FILLED)
            
            prev_point = curr_point
        
        else:
            prev_point = None 


    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)
    img[mask > 0] = canvas[mask > 0]


    draw_header(img, CURRENT_COLOR)
    
    cv2.imshow("Air Canvas Pro - Salma", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()