import random as rd
import pygame
import time
import os

pygame.init()


while True:
    N = int(input("Rozmiar szachownicy: ")) #size of the board
    if N > 3 or N == 1:
        break
    else:
        print("Nieprawidłowy rozmiar.")

        
#N = 15 #size of the board
LENGTH = 500//N #length of tile
time.sleep(1)
WIN = pygame.display.set_mode((LENGTH*N ,LENGTH*N)) #main window
Qwhite = pygame.transform.scale(pygame.image.load("queenW.png"),(LENGTH,LENGTH))
Qblack = pygame.transform.scale(pygame.image.load("queenB.png"),(LENGTH,LENGTH))

pygame.display.set_caption("Evoulutionary algorithm")


class Queen:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.r = LENGTH/2

    def draw(self,win):
        #pygame.draw.circle(win,(255,0,0),(self.x,self.y),self.r)
        if ((self.x + self.y - 2*self.r) // LENGTH) % 2:
            win.blit(Qwhite,(self.x-self.r,self.y-self.r))
        else:
            win.blit(Qblack,(self.x-self.r,self.y-self.r))

class Tile:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.length = LENGTH

    def draw(self,win):
        pygame.draw.rect(win,(75,75,75),(self.x,self.y,self.length,self.length))

class Board:
    def draw(self,win):
        for row in range(N):
            for col in range(row%2,N,2):
                tile = Tile(row*LENGTH,col*LENGTH)
                tile.draw(win)

board = Board()
queens = [Queen(x=(LENGTH*(i)+ LENGTH/2)) for i in range(N)]
run = True


#fitness function
def fitness(s):
    res = len(s) - len(set(s)) #calculating how many queens meets horizontically

    #calculating how many queens meets diagonally
    for i in range(len(s)):
        for j in range(i+1,len(s)):
            if abs(s[i]-s[j]) == j-i:
                res += 1 

    return res


solutions = []
for s in range(1000):
    solutions.append(rd.choices(range(1,N+1), k=N))


for i in range(1000):
    rankedSolutions = []
    for s in solutions:
        rankedSolutions.append([fitness(s),s])
        
    rankedSolutions.sort()

    print(f"=== Gen {i} best solutions ===")
    WIN.fill((255,255,255))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    board.draw(WIN)
    for i,queen in enumerate(queens):
        queen.y = LENGTH*rankedSolutions[0][1][i] - LENGTH/2
        queen.draw(WIN)
    
    pygame.display.update()
    print(rankedSolutions[0])


    if rankedSolutions[0][0] == 0:
        break

    bestsolutions = rankedSolutions[:100]

    elements = []
    for s in bestsolutions:
        elements.append(s[1])

    newGen = []
    for _ in range(1000):
        
        s1 = rd.choice(elements)
        s2 = rd.choice(elements)
        
        #crossover
        q = rd.randint(0,N-1)
        news1 = s1[:q]+s2[q:]
        news2 = s1[q:]+s2[:q]

        #mutation
        news1[rd.randint(0,N-1)] = rd.randint(1,N)
        news1[rd.randint(0,N-1)] = rd.randint(1,N)

        newGen.append((news1))
        newGen.append((news2))

    solutions = newGen    

WIN.fill((255,255,255))

run = True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    board.draw(WIN)
    for i,queen in enumerate(queens):
        queen.y = LENGTH*rankedSolutions[0][1][i] - LENGTH/2
        queen.draw(WIN)
    
    pygame.display.update()

