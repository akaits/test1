import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE=pygame.display.set_mode((400,300))
FPSCLOCK=pygame.time.Clock()
pygame.display.set_caption("just window")

def main():
    sysfont=pygame.font.SysFont(None,36)
    counter=0

    while True:
        
        SURFACE.fill((255,255,255))

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        counter+=1

        count_image=sysfont.render(
                "count is {}".format(counter),True,(0,0,0))
        SURFACE.blit(count_image,(50,50))
        pygame.display.update()
        FPSCLOCK.tick(10)
        print("a")


if __name__=="__main__":
    main()
