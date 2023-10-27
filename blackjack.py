
##___________________________MAIN______________________________________________
import pygame
##____________________________IMPLEMENTATION OF BLACK JACK____________________________
import random
class card :
    def __init__(self, suit, value):
        self.suit = suit
        if value==0:
            self.value = "Ace"
            self.imgF = "./cards/A" + self.suit + ".png"
        elif value==1:
            self.value = "Two"
            self.b_val = 2
            self.imgF = "./cards/2" + self.suit + ".png"
        elif value==2:
            self.value = "Three"
            self.b_val = 3
            self.imgF = "./cards/3" + self.suit + ".png"
        elif value==3:
            self.value = "Four"
            self.b_val = 4
            self.imgF = "./cards/4" + self.suit + ".png"
        elif value==4:
            self.value = "Five"
            self.b_val = 5
            self.imgF = "./cards/5" + self.suit + ".png"
        elif value==5:
            self.value = "Six"
            self.b_val = 6
            self.imgF = "./cards/6" + self.suit + ".png"
        elif value==6:
            self.value = "Seven"
            self.b_val = 7
            self.imgF = "./cards/7" + self.suit + ".png"
        elif value==7:
            self.value = "Eight"   
            self.b_val = 8
            self.imgF = "./cards/8" + self.suit + ".png"
        elif value==8:
            self.value = "Nine"
            self.b_val = 8
            self.imgF = "./cards/9" + self.suit + ".png"
        elif value==9:
            self.value = "Ten"
            self.b_val = 10
            self.imgF = "./cards/10" + self.suit + ".png"
        elif value==10:
            self.value = "Jack"
            self.b_val = 10
            self.imgF = "./cards/J" + self.suit + ".png"
        elif value==11:
            self.value = "Queen"  
            self.b_val = 10
            self.imgF = "./cards/Q" + self.suit + ".png"
        elif value==12:
            self.value = "King"  
            self.b_val = 10    
            self.imgF = "./cards/K" + self.suit + ".png"                                    
    def get_suit(self):
        return self.suit
    def get_value(self):
        return self.value
    def print(self):
        return self.get_value() + " of " + self.get_suit()
class deck :
    def __init__(self, deckNum):
        curSuit = "S"
        self.deckNum = deckNum
        self.deck = []
        for i in range(4):

            if i==1:
                curSuit = "C"
            elif i==2:
                curSuit = "D"
            elif i==3:
                curSuit = "H"
            for j in range(13):
                self.deck.append(card(curSuit, j))
            

    def showDeck(self):
        print("Start of Deck #" + str(self.deckNum))
        for i in range(len(self.deck)):
             print(self.deck[i].show())
        print("End Of Deck #" + str(self.deckNum))

class drawPile:
    def __init__(self, numDecks):
        self.pile = []
        self.numDecks = numDecks
        for i in range(numDecks):
            self.pile.extend(deck(i).deck)
    def draw(self):
       i = random.randint(0,len(self.pile) - 1)
       out = self.pile[i]
       del self.pile[i]
       return out
    
    def showDrawPile(self):
        print("Start of Drawpile:")
        for i in range(len(self.pile)):
            print(self.pile[i].show())
        print("End Of Drawpile with " + str(self.numDecks) + " Decks")


class hand:
    def __init__(self, drawpile):
        self.cards = []
        for i in range(2):
            self.cards.append(drawpile.draw())
    def get_score(self):
        out = [0]
        for i in self.cards:
            if i.value != "Ace":
                for j in range(len(out)):
                    out[j] += i.b_val
            else:
                for j in range(len(out)):
                    out.append(out[j] + 11)
                    out[j] += 1
        return out
    def hitHand(self, drawpile):
        self.cards.append(drawpile.draw())
    def printHand(self):
        for i in range(len(self.cards)):
            print(self.cards[i].print())

pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
my_font = pygame.font.SysFont(None, 32)
gameDeck = None
playerHand = None
dealerHand = None


##__________________SCREEN SETUP____________________________________
def drawScreen():
    pygame.draw.rect(screen, 'brown', (0,600,1280,180))
    pygame.draw.rect(screen, 'dark green', (20,20,1240,560))
    for i in range(2):
        pygame.draw.rect(screen, 'black', ((i)*125 + 400, 400, 100, 150), 5 )
    for i in range(2):
        pygame.draw.rect(screen, 'black', ((i)*125 + 600, 50, 100, 150), 5 )

    pygame.draw.rect(screen,"blue", (1120,620,120,80))
    btnLbl = my_font.render("DEAL",False, 'Black')
    screen.blit(btnLbl,(1150, 650))

    pygame.draw.rect(screen,"red", (60,620,120,80))
    btnLbl = my_font.render("HIT ME",False, 'Black')
    screen.blit(btnLbl,(80, 650))

def drawCards():
    for i in range(len(playerHand.cards)):
        img = pygame.image.load(playerHand.cards[i].imgF)
        img = pygame.transform.scale(img, (100,150))
        screen.blit(img, (i*125 +400,400))
    for i in range(len(dealerHand.cards)):
        img = pygame.image.load(dealerHand.cards[i].imgF)
        img = pygame.transform.scale(img, (100,150))
        img = pygame.transform.rotate(img, 180)
        screen.blit(img, (i*125 +600,50))

def updateScores():
    p_score = playerHand.get_score()
    d_score = dealerHand.get_score()
    p_scoretxt = my_font.render("Player: " + str(p_score),False, 'Black')
    d_scoretxt = my_font.render("Dealer: " + str(d_score),False, 'Black')
    screen.blit(p_scoretxt,(200, 450))
    screen.blit(d_scoretxt,(860, 120))
drawScreen()

##game vars
running = True
dealt = False



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            c_pos = pygame.mouse.get_pos()
##____________________BUTTON FUNCTIONALITY________________________________
            ##Deal Button
            if c_pos[0] >= 1120 and c_pos[1] <= 700 and c_pos[1] >= 620 and c_pos[0] <= 1240:
                dealt = True
                gameDeck = drawPile(4)
                playerHand = hand(gameDeck)
                dealerHand = hand(gameDeck)
                drawScreen()
                drawCards()
                updateScores()
            ##Hit button
            if c_pos[0] >= 60 and c_pos[1] <= 700 and c_pos[1] >= 620 and c_pos[0] <= 180 and dealt and len(playerHand.cards) < 7:
                playerHand.hitHand(gameDeck)
                drawScreen()
                drawCards()
                updateScores()
    pygame.display.flip()
pygame.quit()


