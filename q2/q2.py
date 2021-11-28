#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

import object_detection_webcam as odw

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())


# Funcao que calcula distancia
def calcula_dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

# Arquivos necessários
video = "dogtraining.mp4"

if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)


    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    ponto_ini_anterior = None
    distancia_cb_anterior = None

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            #cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break
            

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar o cao e pegar o ponto inicial do bounding box
        img_res, resultados =  odw.detect(frame)
        ponto_ini = None
        for resultado in resultados:
            if resultado[0] == 'dog':
                ponto_ini = resultado[2]
                ponto_fim = resultado[3]
        
        # Checar se eh o primeiro frame
        if ponto_ini_anterior is None:
            distancia_total = 0
        else:
            distancia_total += calcula_dist(ponto_ini, ponto_ini_anterior)

        ponto_ini_anterior = ponto_ini

        print("Distancia: ", distancia_total)

        cv2.putText(img_res, f"Distancia: {distancia_total}", (50,50), cv2.FONT_HERSHEY_PLAIN, 2.0, (0,0,255), 2)

        # Enconttrar a bola
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cor_min = (196/2, 30, 30)
        cor_max = (270/2, 255, 255)
        mask = cv2.inRange(hsv, cor_min, cor_max)

        # Operacoes morfologicas para limpar a mascara
        kernel = np.ones((5,5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Encontrar o contorno da bola
        contours, tree = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(img_res,contours,0,(255,0,0),3)

        bbox = cv2.boundingRect(contours[0])
        cv2.line(img_res,(bbox[0], bbox[1]),(bbox[0], bbox[1]+bbox[3]),(255,0,0), 3) 
        print(bbox)

        # Encontrar a distancia entre o cachorro e a bola
        ponto_cao =( int((ponto_ini[0]+ponto_fim[0])//2), int((ponto_ini[1]+ponto_fim[1])//2) )
        ponto_bola = ( (bbox[0]+bbox[2]//2), (bbox[1]+bbox[3]//2) ) 
        distancia_cb = calcula_dist(ponto_cao, ponto_bola)

        if distancia_cb_anterior is not None:
            if distancia_cb > distancia_cb_anterior:
                cv2.putText(img_res, f"REX CORRE!!", (50,100), cv2.FONT_HERSHEY_PLAIN, 2.0, (0,0,255), 2)
                print("REC, CORRE!!")

        distancia_cb_anterior = distancia_cb

        # Encontrar a menor distancia entre cachorro e bola
        ponto_cao_direita = ( ponto_fim[0], ponto_cao[1] )
        ponto_bola_esquerda = ( bbox[0], ponto_bola[1] )
        #distancia_cb_min = calcula_dist(ponto_cao_direita, ponto_bola_esquerda)
        
        cv2.circle(img_res, ponto_cao_direita, 5, (0,225,0),-1)
        cv2.circle(img_res, ponto_bola_esquerda, 5, (0,225,0),-1)

       # print(" Dist cao bola min: ", distancia_cb_min)
        
        if abs(ponto_cao_direita[0] - ponto_bola_esquerda[0]) < 20:
            print("PEGOU!!!")
            cv2.putText(img_res, f"PEGOU!!", (100,300), cv2.FONT_HERSHEY_PLAIN, 5.0, (0,0,255), 2)


        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', img_res)
        cv2.imshow('bola', mask)

        # Pressione 'q' para interromper o video
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

