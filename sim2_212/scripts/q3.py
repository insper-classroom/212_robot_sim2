#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy

import math

from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty
from nav_msgs.msg import Odometry

topico_odom = "/odom"

# Apenas valores para inicializar
x = -1000
y = -1000
z = -1000

def recebeu_leitura(dado):
    """
        Grava nas variáveis x,y,z a posição extraída da odometria
    """
    global x
    global y 
    global z 

    x = dado.pose.pose.position.x
    y = dado.pose.pose.position.y
    z = dado.pose.pose.position.z

if __name__=="__main__":

    rospy.init_node("q3")

    # Cria um subscriber que chama recebeu_leitura sempre que houver nova odometria
    recebe_scan = rospy.Subscriber(topico_odom, Odometry , recebeu_leitura)
    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size=3)

    try:
        while not rospy.is_shutdown():
            velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
            rospy.sleep(2.0)

            # 1 - Mandar o robo virar 30 graus antihorario
            print("x {} y {} z {}".format(x, y, z))

            velocidade = Twist(Vector3(0.05, 0, 0), Vector3(0, 0, math.radians(15)))         
            velocidade_saida.publish(velocidade)
            velocidade_saida.publish(velocidade) # Publica 2x para evitrar o bug do primeiro comando
            rospy.sleep(2.0)

            # 2 - Mandar o robo andar 2m
            print("x {} y {} z {}".format(x, y, z))
            vertice = (x, y, z)
            
            velocidade = Twist(Vector3(0.25, 0, 0), Vector3(0, 0, 0))
            velocidade_saida.publish(velocidade)
            
            distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5
            while distancia < 2:
                rospy.sleep(0.1)
                distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5

            # 3 - Mandar o robo virar 120 graus antihorario
            print("x {} y {} z {}".format(x, y, z))
            
            velocidade = Twist(Vector3(0.05, 0, 0), Vector3(0, 0, math.radians(15)))
            velocidade_saida.publish(velocidade)
            velocidade_saida.publish(velocidade) # Publica 2x para evitrar o bug do primeiro comando
            rospy.sleep(8.0)

            # 4 - Mandar o robo andar 2m
            print("x {} y {} z {}".format(x, y, z))
            vertice = (x, y, z)
            
            velocidade = Twist(Vector3(0.25, 0, 0), Vector3(0, 0, 0))
            velocidade_saida.publish(velocidade)
            
            distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5
            while distancia < 2:
                rospy.sleep(0.01)
                distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5

            # 5 - Mandar o robo virar 60 graus antihorario
            print("x {} y {} z {}".format(x, y, z))
            
            velocidade = Twist(Vector3(0.05, 0, 0), Vector3(0, 0, math.radians(15)))
            velocidade_saida.publish(velocidade)
            velocidade_saida.publish(velocidade) # Publica 2x para evitrar o bug do primeiro comando
            rospy.sleep(4.0)

            # 6 - Mandar o robo andar 2m
            print("x {} y {} z {}".format(x, y, z))
            vertice = (x, y, z)
            
            velocidade = Twist(Vector3(0.25, 0, 0), Vector3(0, 0, 0))
            velocidade_saida.publish(velocidade)
            
            distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5
            while distancia < 2:
                rospy.sleep(0.01)
                distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5

            # 7 - Mandar o robo virar 120 graus antihorario
            print("x {} y {} z {}".format(x, y, z))
            
            velocidade = Twist(Vector3(0.05, 0, 0), Vector3(0, 0, math.radians(15)))
            velocidade_saida.publish(velocidade)
            velocidade_saida.publish(velocidade) # Publica 2x para evitrar o bug do primeiro comando
            rospy.sleep(8.0)

            # 8 - Mandar o robo andar 2m
            print("x {} y {} z {}".format(x, y, z))
            vertice = (x, y, z)
            
            velocidade = Twist(Vector3(0.25, 0, 0), Vector3(0, 0, 0))
            velocidade_saida.publish(velocidade)
            
            distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5
            while distancia < 2:
                rospy.sleep(0.01)
                distancia = ((x-vertice[0])**2 + (y-vertice[1])**2)**0.5

    except rospy.ROSInterruptException:
        velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        velocidade_saida.publish(velocidade)
        rospy.sleep(1.0)