
##___________________________MAIN______________________________________________
import pygame
##____________________________IMPLEMENTATION OF BLACK JACK____________________________
import random
class card :
    def __init__(self, suit, value):
        self.suit = suit
        if value==0:
            self.value = "Ace"
            self.b_val = 1
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
    #returns possible score for all cards in hand
    def get_score(self):
        vals = [0]
        #gen all possible scores
        for i in self.cards:
            if i.value != "Ace":
                for j in range(len(vals)):
                    vals[j] += i.b_val

            else:
                for j in range(len(vals)):
                    vals.append(vals[j] + 11)
                    vals[j] += 1
        #elim busts if result is empty list then hand is a bust
        out = []
        for i in range(len(vals)):
            if vals[i] <= 21:
                out.append(vals[i])

        return out
    #returns possible dealer score for shown card only (score of first card in hand)
    def get_dScore(self):
        out = [0]
        if self.cards[0].value != "Ace":
            out[0] = self.cards[0].b_val
        else:
            out[0] = 1
            out.append(11)
        return out
    def hitHand(self, drawpile):
        self.cards.append(drawpile.draw())
    def getMaxScore(self, list):
        if(len(list) > 1):
            best = list[0]
            for i in range(1, len(list)):
                if(list[i] > best):
                    best = list[i]
            return best
        else:
            return list
        
    def getBust_score(self):
        out = 0
        for i in self.cards:
            out += i.b_val
        return out
        
    def dealerStop(self):
        init = self.get_score()
        if init == []:
            return -1
        out = []
        for i in range(len(init)):
            if init[i] > 16:
                out.append(init)
        
        return self.getMaxScore(out)

   
        
    def scoresToTextList(self):
        if len(self.get_score()) > 0:   
            out = str(self.get_score()[0])
        else:
            return str(self.getBust_score())
        for i in range(1, len(self.get_score())):
            out += ", " + str(self.get_score()[i])
        return out

class player:
    def __init__(self):
        self.money = 1000
        self.wins = 0
        self.losses = 0
        self.blackjacks = 0

#game assets_____________________________________
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
my_font = pygame.font.SysFont(None, 32)
announcement = pygame.font.SysFont(None, 72)

cardBackI = pygame.image.load('./cards/B.png')
cardBackI = pygame.transform.scale(cardBackI, (100,150))
#game vars_________________________________
running = True
dealt = False
gameDeck = None
playerHand = None
dealerHand = None
dealerRound = 0
playerRound = 0
playerTurn = True

##__________________SCREEN SETUP____________________________________
def drawScreen(player):
    pygame.draw.rect(screen, 'brown', (0,600,1280,180))
    pygame.draw.rect(screen, 'dark green', (20,20,1240,560))

    #Buttons___________________________________________
    pygame.draw.rect(screen,"blue", (1120,620,120,80))
    btnLbl = my_font.render("DEAL",False, 'Black')
    screen.blit(btnLbl,(1150, 650))

    pygame.draw.rect(screen,"red", (60,620,120,80))
    btnLbl = my_font.render("HIT ME",False, 'Black')
    screen.blit(btnLbl,(80, 650))

    pygame.draw.rect(screen,"yellow", (200,620,120,80))
    btnLbl = my_font.render("STAND",False, 'Black')
    screen.blit(btnLbl,(220, 650))

    #stats/info________________________________________
    relx = 50
    rely = 50
    pygame.draw.rect(screen,"white", (relx, rely,200,80))
    wlLbl = my_font.render("W/L: " + str(player.wins) + "/" + str(player.losses), False, 'Black')
    screen.blit(wlLbl,(relx+20, rely+10))
    moneyLbl = my_font.render("Money: $" + str(player.money) ,False, 'Black')
    screen.blit(moneyLbl,(relx+20, rely+40))

    
    for i in range(2):
        pygame.draw.rect(screen, 'black', ((i)*125 + 400, 400, 100, 150), 5 )
    for i in range(2):
        pygame.draw.rect(screen, 'black', ((i)*125 + 600, 50, 100, 150), 5 )
    pygame.display.flip()


def drawCards_dh():
    #player cards
    print("drawing cards")
    for i in range(len(playerHand.cards)):
        img = pygame.image.load(playerHand.cards[i].imgF)
        img = pygame.transform.scale(img, (100,150))
        screen.blit(img, (i*125 +400,400))
    #dealer card one shown one hidden
    img = pygame.image.load(dealerHand.cards[0].imgF)
    img = pygame.transform.scale(img, (100,150))
    img = pygame.transform.rotate(img, 180)
    screen.blit(img, (600,50))
    screen.blit(cardBackI, (725,50))
    pygame.display.flip()

def drawCards_ds():
    #player cards
    for i in range(len(playerHand.cards)):
        img = pygame.image.load(playerHand.cards[i].imgF)
        img = pygame.transform.scale(img, (100,150))
        screen.blit(img, (i*125 +400,400))
    #player cards
    for i in range(len(dealerHand.cards)):
        img = pygame.image.load(dealerHand.cards[i].imgF)
        img = pygame.transform.scale(img, (100,150))
        img = pygame.transform.rotate(img, 180)
        screen.blit(img, (i*125 +600,50))
    pygame.display.flip()

def updateScores_dh():
    p_score = playerHand.get_score()
    d_score = dealerHand.get_dScore()
    p_scoretxt = my_font.render("Player: " + playerHand.scoresToTextList(),False, 'Black')
    d_scoretxt = my_font.render("Dealer: " + str(d_score[0]),False, 'Black')
    screen.blit(p_scoretxt,(200, 450))
    screen.blit(d_scoretxt,(460, 120))
    pygame.display.flip()

def updateScores_ds():
    p_score = playerHand.get_score()
    d_score = dealerHand.get_score()
    p_scoretxt = my_font.render("Player: " + playerHand.scoresToTextList(),False, 'Black')
    d_scoretxt = my_font.render("Dealer: " + dealerHand.scoresToTextList(),False, 'Black')
    screen.blit(p_scoretxt,(200, 450))
    screen.blit(d_scoretxt,(460, 120))
    pygame.display.flip()
def roundWon(player):
    pygame.draw.rect(screen, "dark green", (200,250,1000,150))
    wintxt = announcement.render("PLAYER WINS ROUND",False, 'Black')
    screen.blit(wintxt,(375, 275))
    pygame.display.flip()
    pygame.time.delay(2000)
    player.wins+=1

def roundLost(player):
    pygame.draw.rect(screen, "dark green", (200,250,1000,150))
    wintxt = announcement.render("DEALER WINS ROUND",False, 'Black')
    screen.blit(wintxt,(375, 275))
    pygame.display.flip()
    pygame.time.delay(2000)
    player.losses += 1

def pBlackjack():
    pygame.draw.rect(screen, "dark green", (200,250,1000,150))
    wintxt = announcement.render("PLAYER BLACKJACK",False, 'Black')
    screen.blit(wintxt, (375, 275))
    pygame.display.flip()
    pygame.time.delay(2000)

def dBlackjack():
    pygame.draw.rect(screen, "dark green", (200,250,1000,150))
    wintxt = announcement.render("DEALER BLACKJACK",False, 'Black')
    screen.blit(wintxt, (375, 275))
    pygame.display.flip()
    pygame.time.delay(2000)

def push():
    pygame.draw.rect(screen, "dark green", (200,250,1000,150))
    wintxt = announcement.render("PUSH",False, 'Black')
    screen.blit(wintxt, (375, 275))
    pygame.display.flip()
    pygame.time.delay(2000)

def pBust():
    pygame.draw.rect(screen, "dark green", (200,250,1000,150))
    wintxt = announcement.render("PLAYER BUSTS",False, 'Black')
    screen.blit(wintxt, (375, 275))
    pygame.display.flip()
    pygame.time.delay(2000)

def dBust():
    pygame.draw.rect(screen, "dark green", (200,250,1000,150))
    wintxt = announcement.render("DEALER BUSTS",False, 'Black')
    screen.blit(wintxt, (375, 275))
    pygame.display.flip()
    pygame.time.delay(2000)

def endstate(player):
    if playerRound == 21 and len(playerHand.cards) == 2:
        pBlackjack()
    if dealerRound == 21 and len(dealerHand.cards) == 2:
        dBlackjack()
    if playerRound == dealerRound:
        push()
    elif dealerRound == -1:
        dBust()
        roundWon(player)
    elif playerRound > dealerRound:
        roundWon(player)
    elif playerRound < dealerRound:
        roundLost(player)




#____________________________MAIN GAME LOOP_________________________________
p = player()
drawScreen(p)
gameDeck = drawPile(4)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            c_pos = pygame.mouse.get_pos()
            #____________________BUTTON FUNCTIONALITY________________________________
            #Deal Button
            if c_pos[0] >= 1120 and c_pos[1] <= 700 and c_pos[1] >= 620 and c_pos[0] <= 1240 and not dealt:
                print("deal_btn")
                dealt = True
                playerTurn = True
                playerHand = hand(gameDeck)
                dealerHand = hand(gameDeck)
                drawScreen(p)
                drawCards_dh()
                updateScores_dh()
            #Hit button
            if c_pos[0] >= 60 and c_pos[1] <= 700 and c_pos[1] >= 620 and c_pos[0] <= 180 and dealt and len(playerHand.cards) < 7 and playerTurn:
                playerHand.hitHand(gameDeck)
                drawCards_dh()
                pygame.display.flip()
                if playerHand.get_score() == []:
                    b_score = playerHand.getBust_score()
                    b_scoretxt = my_font.render("Player: " + str(b_score),False, 'Black')
                    pygame.draw.rect(screen, "dark green", (180,420,210,100))
                    screen.blit(b_scoretxt,(200, 450))
                    pygame.display.flip()
                    pBust()
                    roundLost(p)
                    dealt = False
                    drawScreen(p)
                else:
                    drawScreen(p)
                    drawCards_dh()
                    updateScores_dh()
            #Stand button
            if c_pos[0] >= 200 and c_pos[1] <= 700 and c_pos[1] >= 620 and c_pos[0] <= 320 and dealt and playerTurn:
                drawScreen(p)
                drawCards_ds()
                updateScores_ds()
                pygame.display.flip()
                pygame.time.delay(1000)
                playerRound = playerHand.get_score()[len(playerHand.get_score())-1]
                playerTurn = False
                dealerPlaying = True
                while dealerPlaying:
                    if dealerHand.dealerStop() == -1:
                        dealerRound = -1
                        dealerPlaying = False
                    elif dealerHand.dealerStop() == []:
                        dealerHand.hitHand(gameDeck)
                        drawScreen(p)
                        drawCards_ds()
                        updateScores_ds()
                        pygame.display.flip()
                        pygame.time.delay(1000)
                    else:
                        toInt = dealerHand.dealerStop()
                        while type(toInt) != int:
                            toInt = toInt[len(toInt) -1]
                        dealerRound = toInt
                        dealerPlaying = False
                endstate(p)
                dealt = False
                drawScreen(p)
                
                
pygame.quit()


