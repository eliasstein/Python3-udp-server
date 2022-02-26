import pygame               #Import Pygame if you don't have it "pip install pygame"
from pygame.locals import *
import socket

from OpenGL.GL import *     #Import OpenGL Library  "pip install PyOpenGL"
from OpenGL.GLU import *

localIP     = "192.168.0.2" #Your local ip you can see it typing in the cmd terminal "ipconfig" or in linux is "ifconfig" 
localPort   = 5000          #the port that you asign in the HyperIMU or your client
bufferSize  = 256           #Data Lenght

msgFromServer       = "Hello UDP Client"   
bytesToSend         = str.encode(msgFromServer)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  #This is the configuration to catch udp packets
UDPServerSocket.bind((localIP, localPort))



verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800,600)     #Resolution of pygame
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        data = message.decode("utf-8").split(",")
        address = bytesAddressPair[1]
        print(data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #glRotatef(0.05, float(data[0]), float(data[1]), float(data[2][:-1]))
        glRotatef(float(data[5]),0,float(data[2][:-1])/360,0)
        glRotatef(float(data[3]),float(data[0])/360,0,0)
        glRotatef(float(data[4]),0,0,-float(data[1])/360)

        glTranslate(-float(data[5])/30,float(data[3])/30,0)#float(data[4])/30)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()