#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy

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
            velocidade_saida.publish(velocidade)
            print("x {} y {} z {}".format(x, y, z))
            rospy.sleep(0.1)

    except rospy.ROSInterruptException:
        velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
        velocidade_saida.publish(velocidade)
        rospy.sleep(1.0)