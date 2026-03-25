import cv2
cap = cv2.VideoCapture(0) # c le numéro de la caméra, 0 pour la première caméra, 1 pour la deuxième, etc.
# le while est une boucle infinie pourque la fenêtre reste ouverte jusqu'à
# ce que l'utilisateur appuie sur une touche
while cv2.waitKey(1) < 0 :  # <0 signifie que la boucle continue tant qu'aucune touche n'est appuyée
    cv2.imshow("Test Webcam (Appuez sue une touche)", 
    cap.read()[1]) # cap.read() retourne un tuple (ret, frame), on prend le deuxième élément qui est l'image capturée
