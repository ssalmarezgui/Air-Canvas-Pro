import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.8,
    min_tracking_confidence = 0.5
)

def get_landmarks(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb) # analyse de l'image pour chercher des mains 
    lm_list = [] # pour ranger les cordonnées des points de la main

    if results.multi_hand_landmarks: # verification de detction de au mois une main 
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS) # pour dessiner la squelette virtuel
            
            for id, lm in enumerate(hand_lms.landmark): #on boucle sur les points de la main
                h, w, _ = img.shape
                lm_list.append((id, int(lm.x * w), int(lm.y * h)))

            
    return lm_list


######## Implemantation des fingers ##############

FINGER_TIPS = [8, 12, 16, 20]

def fingers_up(lm_list):
    if len(lm_list) == 0:
        return []
    
    fingers = []

    #pouce 
    fingers.append(1 if lm_list[4][1] > lm_list[3][1] else 0)

    #index, majeur, annulaire, auriculaire
    for tip in FINGER_TIPS:
        fingers.append(1 if lm_list[tip][2] < lm_list[tip-2][2] else 0)

    return fingers
    # [0,1,0,0,0] => mode dessin
    # [1,1,1,1,1] => mode effacement

    


