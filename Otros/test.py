import pygame
pygame.init()

class keymanager:
    def __init__(self, one, two):
        self.one = one
        self.two = two
        
    def leer(self):
        while 1:
            for key in pygame.event.get():
            
                if key.type == pygame.quit:
                    print "Salir"
                
                if one.count(key.tipe) > 0:
                     print "tecla de 1 jugador"
                
                elif two.count(key.tipe) > 0:
                    print "tecla de 2 jugador"
                    
                else:
                    print "no es la tecla de ningun jugador"
            


one = [True, False, "hsahs"]
two = [pygame.K_LEFT]

manager = keymanager(one, two)

manager.leer()
