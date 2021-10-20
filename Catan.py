import random
class Player(object):
   def __init__(self,color,number):
       self.color=color
       self.number=number
       self.deck=[1,2,3,4,1,2,3,4,2,4,2,4]
       self.devCards=[]
       self.knights=0
       self.VP=0
       self.roads=[]
       self.numOfRoads=0
       self.settlements=[]
       self.cities=[]
       self.longRoad=False
       self.largeArmy=False
       self.total=0
  
   def addDevCard(self,card):
       self.devCards.append(card)
       self.deck.remove(0)
       self.deck.remove(1)
       self.deck.remove(3)
       if card==1: #if the card is a victory point (value 1)
           self.VP+=1
           self.victoryCount()
 
   def useKnight(self):
       self.knights+=1
       self.devCards.remove(0) #remove 1 knight from dev card bank
   
   def useMonopoly(self):
       self.devCards.remove(2)

   def useRoadBuilding(self):
       self.deck.append(2)
       self.deck.append(4)
       self.deck.append(2)
       self.deck.append(4)
       self.devCards.remove(3)
       print("Use for road only")

   def useYOP(self):
       self.deck.append(random.randint(0,4))
       self.deck.append(random.randint(0,4))
       self.devCards.remove(4)
  
   def addRoad(self,road):
       self.roads.append(road)
       self.numOfRoads+=1   
       self.deck.remove(2)
       self.deck.remove(4)
  
   def addSettlement(self,settlement):
       self.settlements.append(settlement)
       self.deck.remove(1)
       self.deck.remove(2)
       self.deck.remove(3)
       self.deck.remove(4)
       self.victoryCount()
   
   def bankTrade(self, tradingResource, resourceWanted):
       self.deck.remove(tradingResource[0])
       self.deck.remove(tradingResource[0])
       self.deck.remove(tradingResource[0])
       self.deck.remove(tradingResource[0])
       self.deck.append(resourceWanted[0])
    
   def playerTrade(self, tradingResources, resourcesWanted):
       for item in tradingResources:
           self.deck.remove(item)
       for resource in resourcesWanted:
           self.deck.append(resource)

   def addCity(self,city):
       self.settlements.remove(city)
       self.cities.append(city)
       self.deck.remove(0)
       self.deck.remove(0)
       self.deck.remove(0)
       self.deck.remove(1)
       self.deck.remove(1)
       self.victoryCount()
  
   def victoryCount(self): #score calculation
       if self.longRoad==True:
           self.VP+=2
       if self.largeArmy==True:
           self.VP+=2
       self.total=len(self.settlements)+(2*len(self.cities))+self.VP
 
from cmu_112_graphics import *
import random
#appStarted
def appStarted(app):
    app.rows = 5
    app.cx = 300
    app.cy = (app.height) / 2
    app.dots = []
    app.productionAliases = [ ([0]*6) for row in range(19) ]
    app.boardNumbers = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
    random.shuffle(app.boardNumbers)
    app.selectedSettlement = []
    board(app)
    app.boardLayout = list() #
    makeBoard(app)
    app.robberCenter=app.boardLayout[app.robberIndex]
    app.startRC = app.robberCenter
    players(app)
    bank(app)
    mousePressedFunctions(app)
    makeSettlementSpots(app)
    app.selectedSettlements = []
    app.tempRoad=[]
    app.selectedRoads = []
    productionAlias(app)
    app.die = "Click roll die to roll!"
    app.rolled = True
    app.resourceProduction = ""
    app.built = False
    for i in range(len(app.board)):
        if app.board[i] == 5:
            app.boardNumbers.insert(i, 0)
    app.gameStart = True
    app.r2gameStart = False
    app.round2Done=False
    app.tradingMode = False
    app.currPlayerOffer = []
    app.oppPlayerOffer = []
    app.oppPlayer = app.bluePlayer
    app.oppPlayerNum = app.bluePlayer.number
    app.currPlayerHide = True
    app.oppPlayerHide = True
    app.makeTrade = False
    app.gameOver=False
    app.winner=None
  
def mousePressedFunctions(app):
    app.settlementMode=False
    app.cityMode=False
    app.roadMode=False
    app.robberMode=False

def keyPressed(app,event):
    if app.gameOver==True:
        if event.key=="r":
            appStarted(app)
    else:
        if event.key == 't':
            app.tradingMode = not app.tradingMode
        elif event.key == 'o':
            app.oppPlayerHide = not app.oppPlayerHide
        elif event.key == 'c':
            app.currPlayerHide = not app.currPlayerHide
        elif event.key == 'a':
            app.makeTrade = not app.makeTrade
        elif event.key=="d":
            app.currPlayerOffer=[]
            app.oppPlayerOffer=[]
            app.makeTrade=False
        elif event.key=="b":
            if len(app.currPlayerOffer)>=4:
                app.currPlayer.bankTrade(app.currPlayerOffer,app.oppPlayerOffer)
            else:
                print("Not enough resources")
                
def mousePressed(app,event):
 if app.gameOver==True:
     return
 else:
    if app.robberMode==True:
        robberMode(app,event)
        return
    elif app.settlementMode==True:
         settlementMode(app,event)
    elif app.roadMode==True:
         roadMode(app,event)
    elif app.cityMode==True:
         cityMode(app,event)
    if app.tradingMode==True:
        tradeMode(app,event)
        tradingBlock(app,event)
    if 625 <= event.x <= 685 and 65 <= event.y <= 85 and app.rolled == False:
        rollDie(app)
        if app.die==7:
            app.robberMode=True
            app.roadMode=False
            app.settlementMode=False
            app.cityMode=False
        app.rolled = True
    elif  ((3*app.width/4 - 135) <= event.x <= (3*app.width/4 - 99)) and (215 <= event.y <= 235) and (app.rolled == True) and (app.built == False):
    # for building roads
        if app.currPlayer.deck.count(2)>=1 and app.currPlayer.deck.count(4)>=1:
           app.roadMode=True
           app.settlementMode=False
           app.cityMode=False
           app.robberMode=False
           print("build road")
        else:
           print("Not enough resources")
        pass
    elif 3*app.width/4 - 75 <= event.x <= 3*app.width/4 - 5 and 215 <= event.y <= 235 and app.rolled == True and app.built == False:
    # for building settlements
        if (app.currPlayer.deck.count(2)>=1 and app.currPlayer.deck.count(4)>=1 and
           app.currPlayer.deck.count(1)>=1 and app.currPlayer.deck.count(3)>=1):
           app.roadMode=False
           app.settlementMode=True
           app.cityMode=False
           app.robberMode=False
           print("build settlement")
        else:
            print("Not enough resources")
        pass
    elif 3*app.width/4 + 20 <= event.x <= 3*app.width/4 + 48 and 215 <= event.y <= 235 and app.rolled == True and app.built == False:
    # for building cities
        if app.currPlayer.deck.count(0)>=3 and app.currPlayer.deck.count(1)>=2:
           app.roadMode=False
           app.settlementMode=False
           app.cityMode=True
           app.robberMode=False
           print("build city")
        else:
           print("Not enough resources")
        pass
    elif 3*app.width/4 + 72 <= event.x <= 3*app.width/4 + 134 and 215 <= event.y <= 235:
    # for buying a dev card
        if (app.currPlayer.deck.count(0)>=1 and app.currPlayer.deck.count(1)>=1 and
           app.currPlayer.deck.count(3)>=1):
           app.roadMode=False
           app.settlementMode=False
           app.cityMode=False
           app.robberMode=False
           buyDevCard(app)
           print("buy dev card")
        else:
           print("Not enough resources")
        pass
    elif app.width - 100 <= event.x <= app.width - 50 and 215 <= event.y <= 235 and app.rolled == True:
        app.built = True
        app.roadMode=False
        app.settlementMode=False
        app.cityMode=False
        app.robberMode=False
   # finishes building turn
    elif 850 <= event.x <= 950 and 475 <= event.y <= 525 and app.built == True:
        if app.gameStart==True:
            if app.currPlayerNum==3:
                app.gameStart=False
                app.r2gameStart=True
            app.rolled = True
        elif app.r2gameStart==True:
            if app.currPlayerNum==0:
                app.r2gameStart=False
                app.rolled = False
            elif app.currPlayerNum==3:
                app.round2Done=True
                startingResources(app)
            else:
                app.rolled=True
        else:
            app.rolled=False
        app.built = False
        app.die = "Click roll die to roll!"
        if app.currPlayerNum == 3:
            if app.r2gameStart==True and app.round2Done==False:
                app.currPlayerNum=3
            elif app.r2gameStart==True and app.round2Done==True:
                app.currPlayerNum-=1
            else:
                app.currPlayerNum = 0
            app.currPlayer=app.players[app.currPlayerNum]
        else:
            if app.r2gameStart==True:
                app.currPlayerNum -= 1
            else:
                app.currPlayerNum+=1
            app.currPlayer=app.players[app.currPlayerNum]
    elif 1035<= event.x <=1125 and 365 <= event.y <= 385:
       playYOP(app)
    elif 825<= event.x <=900 and 365 <= event.y <= 385:
       playMonopoly(app)
    elif 750<= event.x <=800 and 365 <= event.y <= 385:
       playKnight(app)
    elif 925<= event.x <=1010 and 365 <= event.y <= 385:
       playRoadBuilding(app)

def startingResources(app):
    for n in range(len(app.boardNumbers)):
        for vertex in app.productionAliases[n]:
            for player in app.players:
                if((vertex[0] == app.dots[player.settlements[0]][0]) and (vertex[1] == app.dots[player.settlements[0]][1])):
                    player.deck.append(app.board[n])

def checkGameOver(app):
    for player in app.players:
        total=player.total
        if total>=10:
            app.gameOver=True
            app.winner=player
            return

def playKnight(app):
    if 0 in app.currPlayer.devCards:
        app.currPlayer.useKnight()
        app.robberMode=True
    largestArmy(app)
    checkGameOver(app)

def playYOP(app):
    if 4 in app.currPlayer.devCards:
        app.currPlayer.useYOP()
    checkGameOver(app)

def playMonopoly(app):
    if 2 in app.currPlayer.devCards:
        app.currPlayer.useMonopoly()
        card=random.randint(0,4)
        for player in app.players:
            for number in player.deck:
                if number==card:
                    player.deck.remove(number)
                    app.currPlayer.deck.append(card)
    checkGameOver(app)

def playRoadBuilding(app):
    if 3 in app.currPlayer.devCards:
        app.currPlayer.useRoadBuilding()
    checkGameOver(app)

def largestArmy(app):   
    best = 0
    bestPlayer = 0
    for player in app.players:
        if(player.knights > 3 and best < player.knights):
            best = player.knights
            bestPlayer = player
    for player in app.players:
        if(bestPlayer == player):
            bestPlayer.largestArmy = True
        else:
            player.largestArmy = False
 
def longestRoad(app):   
    best = 0
    bestPlayer = 0
    for player in app.players:
        if(player.numOfRoads > 5 and best < player.numOfRoads):
            best = player.numOfRoads
            bestPlayer = player
    for player in app.players:
        if(bestPlayer == player):
            bestPlayer.longestRoad = True
        else:
            player.longestRoad = False
    checkGameOver(app)

def buyDevCard(app):
   card=app.devCardDeck[0]
   app.currPlayer.addDevCard(card)
   app.devCardDeck=app.devCardDeck[1:]
   checkGameOver(app)
 
def robberMode(app,event):
    for center in app.boardLayout:
        cx=center[0]
        cy=center[1]
        if abs(event.x-cx)<=30 and abs(event.y-cy)<=30:
            app.robberCenter=[cx,cy] 
            stealableSettlements = []
            stealing = ''
            for player in app.players:
                if(player != app.currPlayer):
                    for settlements in player.settlements:
                        if(dist(cx, cy, app.dots[settlements][0], app.dots[settlements][1]) < 60):
                            stealableSettlements.append(player)
                    for cities in player.cities:
                        if(dist(cx, cy, app.dots[cities][0], app.dots[cities][1]) < 60):
                            stealableSettlements.append(player)
            if(len(stealableSettlements)>0):
                stealing = stealableSettlements[random.randint(0, len(stealableSettlements)-1)]
                if(len(stealing.deck) > 0):
                    stolen = stealing.deck.pop(random.randint(0, len(stealing.deck)-1))
                    app.currPlayer.deck.append(stolen)
            app.robberMode = False
 
def settlementMode(app,event):
   for index in range(len(app.dots)):
     cx=app.dots[index][0]
     cy=app.dots[index][1]
     if abs(event.x-cx)<=10 and abs(event.y-cy)<=10:
         if index not in app.selectedSettlements:
             if app.gameStart==True:
                 if app.currPlayer.settlements==[]:
                    for i in app.selectedSettlements:
                        cx1=app.dots[i][0]
                        cy1=app.dots[i][1]
                        d=distanceFormula(cx,cy,cx1,cy1)
                        if abs(d-(100/(3**0.5)))<=10:
                            return
                    app.currPlayer.addSettlement(index)
                    app.selectedSettlements.append(index)
                    checkGameOver(app)
             elif app.r2gameStart==True:
                 if len(app.currPlayer.settlements)==1:
                     for j in app.selectedSettlements:
                        cx2=app.dots[j][0]
                        cy2=app.dots[j][1]
                        d=distanceFormula(cx,cy,cx2,cy2)
                        if abs(d-(100/(3**0.5)))<=10:
                            return
                     app.currPlayer.addSettlement(index)
                     app.selectedSettlements.append(index)
                     checkGameOver(app)
             else:
                 for k in app.selectedSettlements:
                     cx3=app.dots[k][0]
                     cy3=app.dots[k][1]
                     d=distanceFormula(cx,cy,cx3,cy3)
                     if abs(d-(100/(3**0.5)))<=10:
                         return
                 for road in app.currPlayer.roads:
                     if road[0]==index or road[1]==index:
                        app.currPlayer.addSettlement(index)
                        app.selectedSettlements.append(index)
                        checkGameOver(app)

def tradingBlock(app,event):
    if 805 <= event.x <= 840 and 115 <= event.y <= 135:
        app.currPlayerOffer.append(0)
    elif 850 <= event.x <= 895 and 115 <= event.y <= 135:
        app.currPlayerOffer.append(1)
    elif 900 <= event.x <= 950 and 115 <= event.y <= 135:
        app.currPlayerOffer.append(2)
    elif 960 <= event.x <= 1000 and 115 <= event.y <= 135:
        app.currPlayerOffer.append(3)
    elif 1015 <= event.x <= 1055 and 115 <= event.y <= 135:
        app.currPlayerOffer.append(4)
    
    if 805 <= event.x <= 840 and 340 <= event.y <= 360:
        app.oppPlayerOffer.append(0)
    elif 850 <= event.x <= 895 and 340 <= event.y <= 360:
        app.oppPlayerOffer.append(1)
    elif 900 <= event.x <= 950 and 340 <= event.y <= 360:
        app.oppPlayerOffer.append(2)
    elif 960 <= event.x <= 1000 and 340 <= event.y <= 360:
        app.oppPlayerOffer.append(3)
    elif 1015 <= event.x <= 1055 and 340 <= event.y <= 360:
        app.oppPlayerOffer.append(4)

def tradeMode(app, event):
    if event.x <= 100 and event.x > 0 and event.y <= 100 and event.y >= 0:
        app.oppPlayer = app.bluePlayer
        app.oppPlayerNum = app.bluePlayer.number
        if app.makeTrade == True:
            app.currPlayer.playerTrade(app.currPlayerOffer, app.oppPlayerOffer)
            app.oppPlayer.playerTrade(app.oppPlayerOffer, app.currPlayerOffer)
            app.currPlayerOffer=[]
            app.oppPlayerOffer=[]
    if event.x <= 100 and event.x >= 0 and event.y <= 600 and event.y >= 500:
        app.oppPlayer = app.redPlayer
        app.oppPlayerNum = app.redPlayer.number
        if app.makeTrade == True:
            app.currPlayer.playerTrade(app.currPlayerOffer, app.oppPlayerOffer)
            app.oppPlayer.playerTrade(app.oppPlayerOffer, app.currPlayerOffer)
            app.currPlayerOffer=[]
            app.oppPlayerOffer=[]
    if event.x <= 600 and event.x >= 500 and event.y <= 600 and event.y >= 500:
        app.oppPlayer = app.orangePlayer
        app.oppPlayerNum = app.orangePlayer.number
        if app.makeTrade == True:
            app.currPlayer.playerTrade(app.currPlayerOffer, app.oppPlayerOffer)
            app.oppPlayer.playerTrade(app.oppPlayerOffer, app.currPlayerOffer)
            app.currPlayerOffer=[]
            app.oppPlayerOffer=[]
    if event.x <= 600 and event.x >= 500 and event.y <= 100 and event.y >= 0:
        app.oppPlayer = app.purplePlayer
        app.oppPlayerNum = app.purplePlayer.number
        if app.makeTrade == True:
            app.currPlayer.playerTrade(app.currPlayerOffer, app.oppPlayerOffer)
            app.oppPlayer.playerTrade(app.oppPlayerOffer, app.currPlayerOffer)
            app.currPlayerOffer=[]
            app.oppPlayerOffer=[]

def cityMode(app,event):
  for index in range(len(app.dots)):
      cx=app.dots[index][0]
      cy=app.dots[index][1]
      if abs(event.x-cx)<=10 and abs(event.y-cy)<=10:
          if index in app.currPlayer.settlements:
              app.currPlayer.addCity(index)
  checkGameOver(app)
 
def distanceFormula(x0,y0,x1,y1):
  d=((x1-x0)**2+(y1-y0)**2)**0.5
  return d
 
def roadMode(app,event):
 for index in range(len(app.dots)):
     cx=app.dots[index][0]
     cy=app.dots[index][1]
     if abs(event.x-cx)<=10 and abs(event.y-cy)<=10:
         if app.tempRoad==[]:
             if index in app.currPlayer.settlements:
                 app.tempRoad.append(index)
                 return
             for road in app.currPlayer.roads:
                 if index == road[0] or index==road[1]:
                     if index not in app.tempRoad:
                       app.tempRoad.append(index)
         else:
             cx1=app.dots[app.tempRoad[0]][0]
             cy1=app.dots[app.tempRoad[0]][1]
             d=distanceFormula(cx,cy,cx1,cy1)
             if abs(d-(100/(3**0.5)))<=10:
                 app.tempRoad.append(index)
                 if app.tempRoad not in app.selectedRoads:
                     if app.gameStart==True:
                         if app.currPlayer.roads==[]:
                             app.selectedRoads.append(app.tempRoad)
                             app.currPlayer.addRoad(app.tempRoad)
                             app.tempRoad=[]
                     elif app.r2gameStart==True:
                         if len(app.currPlayer.roads)==1:
                             app.selectedRoads.append(app.tempRoad)
                             app.currPlayer.addRoad(app.tempRoad)
                             app.tempRoad=[]
                     else:
                         app.selectedRoads.append(app.tempRoad)
                         app.currPlayer.addRoad(app.tempRoad)
                         app.tempRoad=[]
                 else:
                     app.tempRoad=[]
             else:
                 app.tempRoad=[]
     longestRoad(app)
 
def dist(x0, y0, x1, y1):
    return ((y1-y0)**2+(x1-x0)**2)**.5
 
def productionAlias(app):
    counter = 0
    for center in app.boardLayout:
        cx=center[0]
        cy=center[1]
        counter1 = 0
        for dotC in app.dots:
            dotX= dotC[0]
            dotY= dotC[1]
            if(58>dist(cx, cy, dotX, dotY)):
                app.productionAliases[counter][counter1] = dotC
                counter1 +=1
        counter +=1
 
def production(app):
    counter = 0
    for n in app.boardNumbers:
        if(app.die == n) and (app.boardLayout[counter]!=app.robberCenter):
            for vertex in app.productionAliases[counter]:
                for player in app.players:
                    for v in player.settlements:
                        if((vertex[0] == app.dots[v][0]) and (vertex[1] == app.dots[v][1])):
                            player.deck.append(app.board[counter])
                    for v in player.cities:
                        if(vertex[0] == app.dots[v][0] and vertex[1] == app.dots[v][1]):
                            player.deck.append(app.board[counter])
                            player.deck.append(app.board[counter])
        counter +=1     
 
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen
 
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).rjust(fieldWidth), end='')
        print(' ]')
    print(']')
 
def bank(app):
  app.oarCount=20
  app.wheatCount=20
  app.woodCount=20
  app.sheepCount=20
  app.brickCount=20
  app.devCardDeck = [0]*14 + [1]*5 + [2]*2 + [3]*2 + [4]*2
  random.shuffle(app.devCardDeck)
 
def players(app):
   app.bluePlayer=Player("blue",0)
   app.redPlayer=Player("red",1)
   app.orangePlayer=Player("orange",2)
   app.purplePlayer=Player("purple",3)
   app.players=[app.bluePlayer,app.redPlayer,app.orangePlayer,app.purplePlayer]
   app.currPlayer=app.bluePlayer
   app.currPlayerNum=app.bluePlayer.number
  
def board(app):
  app.oar=0
  app.wheat=1
  app.wood=2
  app.sheep=3
  app.brick=4
  app.desert=5
  app.board=[]
  app.colors = [PhotoImage(file = "mountain.png"), 
  PhotoImage(file = "wheat.png"), 
  PhotoImage(file = "wood.png"), PhotoImage(file = "sheep.png"),
  PhotoImage(file = "brick.png"), PhotoImage(file = "desert.png")]
  tempBoard=(([app.oar]*3)+([app.wheat]*4)+([app.wood]*4)+
     ([app.sheep]*4)+([app.brick]*3)+([app.desert]))
  while len(app.board)<19 and len(tempBoard)>0:
       index=random.randint(0,len(tempBoard)-1)
       tempBlock=tempBoard[index]
       if tempBlock==5:
           app.robberIndex=len(app.board)
       app.board.append(tempBlock)
       tempBoard.remove(tempBlock)
 
def makeBoard(app):
   for i in range(app.rows):
       if i < 2:
           multiplier = -1
       else:
           multiplier = 1
       if i == 0 or i == 4:
           counter = -app.cx / 3
           for j in range(3):
               app.boardLayout.append([app.cx + counter, app.cy -
                                            ((3 * app.cy) / 6) * multiplier])
               counter += app.cx / 3
       if i == 1 or i == 3:
           counter = -app.cx / 3 - app.cx / 6
           for j in range(4):
               app.boardLayout.append([app.cx + counter, app.cy -
                                            ((1.5 * app.cy) / 6) * multiplier])
               counter += app.cx / 3
       if i == 2:
           counter = -app.cx / 3 - app.cx / 3
           for j in range(5):
               app.boardLayout.append([app.cx + counter,
                                            app.cy])
               counter += app.cx / 3
 
def makeSettlementSpots(app):
    for spot in app.boardLayout:
        xSpot, ySpot = spot[0], spot[1]
        for i in range(3):
            if i == 0:
                if [xSpot - app.cx / 6, ySpot - app.cy / 12] not in app.dots:
                    app.dots.append([xSpot - app.cx / 6, ySpot - app.cy / 12])
                if [xSpot - app.cx / 6, ySpot + app.cy / 12] not in app.dots:
                    app.dots.append([xSpot - app.cx / 6, ySpot + app.cy / 12])
            if i == 1:
                if [xSpot + app.cx / 6, ySpot - app.cy / 12] not in app.dots:
                    app.dots.append([xSpot + app.cx / 6, ySpot - app.cy / 12])
                if [xSpot + app.cx / 6, ySpot + app.cy / 12] not in app.dots:
                    app.dots.append([xSpot + app.cx / 6, ySpot + app.cy / 12])
            if i == 2:
                if [xSpot, ySpot - app.cy / 6] not in app.dots:
                    app.dots.append([xSpot, ySpot - app.cy / 6])
                if [xSpot, ySpot + app.cy / 6] not in app.dots:
                    app.dots.append([xSpot, ySpot + app.cy / 6])
 
def drawCenterPoint(app, canvas, cx, cy, color, counter):
    canvas.create_image(cx,cy, image = color)
    canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill = 'tan')
    canvas.create_text(cx, cy, text = f'{app.boardNumbers[counter]}')
 
def drawStartingSpots(app, canvas):
    counter = 0
    for item in range(len(app.boardLayout)):
        color = app.colors[app.board[item]]
        drawCenterPoint(app, canvas, app.boardLayout[item][0],
                                    app.boardLayout[item][1], color, counter)
        counter += 1
 
def drawBox(app,canvas,player,index):
   if index in [0,1]:
       left=0
       right=left+100
   else:
       right=600
       left=right-100
   if index in [0,3]:
       top=0
       bottom=top+100
   else:
       bottom=app.height
       top=bottom-100
   canvas.create_rectangle(left,top,right,bottom,fill=player.color)
   canvas.create_text((left+right)//2,(top+bottom)//2,text=f"P{index+1}",
                       font="Arial 20 bold",fill="white")
 
def drawFourCorners(app,canvas):
   for index in range(len(app.players)):
       player=app.players[index]
       drawBox(app,canvas,player,index)       
 
def drawDots(app, canvas):
  for item in app.dots:
      xValue = item[0]
      yValue = item[1]
      canvas.create_oval(xValue - 10, yValue - 10, xValue + 10, yValue + 10,
                              fill = 'white')
  for player in app.players: #draw Settlements
      for settlement in player.settlements:
          xValue=app.dots[settlement][0]
          yValue=app.dots[settlement][1]
          canvas.create_rectangle(xValue - 5, yValue - 5, xValue + 5,
                  yValue + 5,fill = player.color)
  for player in app.players:
      for city in player.cities:
          xValue=app.dots[city][0]
          yValue=app.dots[city][1]
          canvas.create_oval(xValue - 10, yValue - 10, xValue + 10,
                      yValue + 10, fill = player.color)
          canvas.create_text(xValue,yValue,text="C",fill="white")
  for player in app.players:
      for road in player.roads:
          x0=app.dots[road[0]][0]
          y0=app.dots[road[0]][1]
          x1=app.dots[road[1]][0]
          y1=app.dots[road[1]][1]
          canvas.create_line(x0,y0,x1,y1,fill=player.color,width=3)
 
def rollDie(app):
 app.die = random.randint(1,6) + random.randint(1,6)
 if app.die==7:
     for player in app.players:
         if len(player.deck)>7:
             half=len(player.deck)//2
             player.deck=player.deck[0:half]
 production(app)
 
def drawPlayerInterface(app, canvas):
    canvas.create_text(3*app.width/4, 25, text = f'Current Player: {app.players[app.currPlayerNum].color}',
                    font = "Arial 30 bold", fill = f'{app.players[app.currPlayerNum].color}')
    canvas.create_text(625, 75, text = "1) Roll die:", fill=f'{app.players[app.currPlayerNum].color}', anchor = "w")
    if app.gameStart == False and app.r2gameStart == False:
        canvas.create_text(3*app.width/4, 75, text = f'Die Result = {app.die}')
    elif app.gameStart == True:
        canvas.create_text(3*app.width/4, 75, text = "Place one road and one settlement to begin")
    elif app.r2gameStart == True:
        canvas.create_text(3*app.width/4, 75, text = "Place one more road and settlement to begin")
    canvas.create_text(625, 125, text = f"2) Resource Production: {app.resourceProduction}", fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    canvas.create_text(625, 175, text = "3) Trade:", fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    canvas.create_text(3*app.width/4, 225, text = "Road        Settlement        City        Dev Card")
    #canvas.create_rectangle(3*app.width/4 - 135, 215, 3*app.width/4 - 99, 235)
    #canvas.create_rectangle(3*app.width/4 - 75, 215, 3*app.width/4 - 5, 235)
    #canvas.create_rectangle(3*app.width/4 + 20, 215, 3*app.width/4 + 48, 235)
    #canvas.create_rectangle(3*app.width/4 + 72, 215, 3*app.width/4 + 134, 235)
    canvas.create_rectangle(app.width - 100, 215, app.width - 50, 235, fill = "green")
    canvas.create_text(app.width - 75, 225, text = "Done", fill = "white")
    canvas.create_text(625, 225, text = "4) Build/Buy:", fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    canvas.create_text(3*app.width/4, 275, text = "Current Player Hand", fill = f'{app.players[app.currPlayerNum].color}')
    canvas.create_text(625, 325, text = f'Resources: Ore - {app.currPlayer.deck.count(0)}, Wheat - {app.currPlayer.deck.count(1)}, Wood - {app.currPlayer.deck.count(2)}, Sheep - {app.currPlayer.deck.count(3)}, Brick - {app.currPlayer.deck.count(4)}', fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    canvas.create_text(625, 375, text = f'Development Cards: Knights - {app.currPlayer.devCards.count(0)}, Monopolies - {app.currPlayer.devCards.count(2)}, Road Building - {app.currPlayer.devCards.count(3)}, Year of Plenty - {app.currPlayer.devCards.count(4)}', fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    canvas.create_text(625, 425, text = f'Played Development Cards: Knights - {app.currPlayer.knights}, VPs - {app.currPlayer.VP}', fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    #canvas.create_text(625, 325, text = "Resources:", fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    #canvas.create_text(625, 375, text = "Development Cards:", fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    #canvas.create_text(625, 425, text = "Played Development Cards:", fill = f'{app.players[app.currPlayerNum].color}', anchor = "w")
    #canvas.create_rectangle(850, 475, 950, 525, fill = "green")
    canvas.create_text(3*app.width/4, 500, text = "Submit", fill = "green", font = "Arial 20 bold")
    l = []
    for i in range(len(app.players)):
        if i != app.currPlayerNum:
            l.append(app.players[i].color)
    l.append("Bank")
    canvas.create_text(3*app.width/4, 175, text = f'{l[0]}        {l[1]}        {l[2]}        {l[3]}')
 
def drawRobber(app,canvas):
   canvas.create_text(app.robberCenter[0],app.robberCenter[1],text="R",
   font = 'Arial 20 bold')

def drawScores(app, canvas):
   l = []
   for i in range(len(app.players)):
       total = app.players[i].total
       player = app.players[i].color
       l.append((total, player))
   sortedList = sorted(l, key=lambda player: player[0])
   sortedList.reverse()  
   canvas.create_text(3*app.width/4, 550, text = f'Standings:   1) {sortedList[0][1]} - {sortedList[0][0]}    2) {sortedList[1][1]} - {sortedList[1][0]}    3) {sortedList[2][1]} - {sortedList[2][0]}    4) {sortedList[3][1]} - {sortedList[3][0]}', fill = "black", font = "Arial 15 bold") 

def drawTrading(app, canvas):
    if app.tradingMode == True:
        canvas.create_text(3*app.width/4, 25, text = "Trading Mode!", font = "Arial 30 bold")
        canvas.create_text(3*app.width/4, 75, text = "Current Player Hand", fill = f'{app.players[app.currPlayerNum].color}')
        canvas.create_text(3*app.width/4, 125, text = f'Resources: Ore - {app.currPlayer.deck.count(0)}, Wheat - {app.currPlayer.deck.count(1)}, Wood - {app.currPlayer.deck.count(2)}, Sheep - {app.currPlayer.deck.count(3)}, Brick - {app.currPlayer.deck.count(4)}', fill = f'{app.players[app.currPlayerNum].color}')
        if app.currPlayerHide == True:
            canvas.create_rectangle(3*app.width/4 - 200 , 115, 3*app.width/4 + 200, 135, fill = "black")
            canvas.create_text(3*app.width/4, 125, text = "Press 'c' to display hand", fill="white")
        
        canvas.create_text(3*app.width/4, 175, text = f'Current Player Offer: Ore - {app.currPlayerOffer.count(0)}, Wheat - {app.currPlayerOffer.count(1)}, Wood - {app.currPlayerOffer.count(2)}, Sheep - {app.currPlayerOffer.count(3)}, Brick - {app.currPlayerOffer.count(4)}')
        canvas.create_text(3*app.width/4, 250, text = f'Opposing Player Offer: Ore - {app.oppPlayerOffer.count(0)}, Wheat - {app.oppPlayerOffer.count(1)}, Wood - {app.oppPlayerOffer.count(2)}, Sheep - {app.oppPlayerOffer.count(3)}, Brick - {app.oppPlayerOffer.count(4)}')
        canvas.create_text(3*app.width/4, 300, text = 'Opposing Player Hand', fill='black')
        canvas.create_text(3*app.width/4, 350, text = f'Resources: Ore - {app.oppPlayer.deck.count(0)}, Wheat - {app.oppPlayer.deck.count(1)}, Wood - {app.oppPlayer.deck.count(2)}, Sheep - {app.oppPlayer.deck.count(3)}, Brick - {app.oppPlayer.deck.count(4)}', fill = f'{app.players[app.oppPlayerNum].color}')
        if app.oppPlayerHide == True:
            canvas.create_rectangle(3*app.width/4 - 200, 340, 3*app.width/4 + 200, 360, fill = "black")
            canvas.create_text(3*app.width/4, 350, text = "Press 'o' to display hand", fill="white")
        canvas.create_text(3*app.width/4, 450, text = "Press 'a', then click on opposing player to accept", fill = "green")
        canvas.create_text(3*app.width/4, 500, text = "Press 'd' to decline", fill = "red")
        canvas.create_text(3*app.width/4, 550, text = "Press 'b' to make bank trade", fill = "black")

def drawGameOver(app,canvas):
    canvas.create_text(app.width//2,app.height//2,text=f"GAME OVER \n  {app.winner.color} WINS!", fill=app.winner.color,font="Arial 60 bold")

def redrawAll(app, canvas):
   canvas.create_rectangle(0,0,600,app.height,
                           fill="light sky blue")
   canvas.create_rectangle(600,0,app.width,app.height,fill="beige")
   drawStartingSpots(app,canvas)
   drawRobber(app,canvas)
   drawFourCorners(app,canvas)
   drawDots(app, canvas)
   if app.tradingMode==True:
       drawTrading(app,canvas)
   else:
       drawPlayerInterface(app, canvas)
       drawScores(app, canvas)
   if app.gameOver==True:
       drawGameOver(app,canvas)

def runCatan():
   print('Running Catan!')
   runApp(width=1200, height=600)
  
runCatan()
