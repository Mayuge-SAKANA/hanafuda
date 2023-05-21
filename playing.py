from playingdata import Deck,Player,Field,YakuManager
import random 
import argparse

def addCardToField(card,field,player):     
    candidates = field.addCardFromPlayer(card)
    if len(candidates)==3 or len(candidates)==1:
        player.addCardFromField([card,*candidates])
    elif len(candidates)==2:
        # here requires player selection of card
        print("card month is overlapped in the field. please select")
        pickCard = player.selectCardFromList(candidates)
        player.addCardFromField([card,pickCard])
        candidates.remove(pickCard)
        field.removeCard(pickCard)

def showGame(player1,player2,field):
    players = []
    if player1.isAuto==False:
        players = [player2,player1]
    else:
        players = [player1,player2]
    print(f"{players[0].playerName}: ",players[0].to_str())
    print()
    print("field: ",field.to_str())
    print()
    print(f"{players[1].playerName} ",players[1].to_str())   

def playGame(player1,player2,seed):
    # initial card
    deck = Deck(seed)
    field = Field()
    yakuMng = YakuManager()

    fieldInitialNumber = 8
    playerInitialNumber = 8

    while True:
        for i in range(fieldInitialNumber):
            card = deck.drawCard()
            field.addCard(card)
        if field.isIniFour():
            print(f"field contains 4 cards {seed}")
            seed = random.randint(0,10000)
            deck = Deck(seed)
            field = Field()
            continue
        break
    
    print(f"deck seed is {seed}")
    print("==============================")
    print()

    players = [player1,player2]
    for player in players:
        for i in range(playerInitialNumber):
            card = deck.drawCard()
            player.addCardToHand(card)
        iniYaku = yakuMng.isInitialYaku(player)
        if iniYaku is not None:
            print(f"{player.playerName} iniYaku {iniYaku.name}")
            return yakuMng.YakuPointDict[iniYaku], player

    onGame = True
    winner = None
    winyaku = {}

    # start game
    while onGame and (not (player1.isEmpty() and player2.isEmpty())):
        for pIdx, player in enumerate(players):
            
            if player.isAuto is False:
                print("==============================")
                showGame(player1,player2,field) 
                print("==============================")

            # here requires player selection of card

            disc = player.selectCardFromList(player.hand)    

            card = player.playCard(disc)
            addCardToField(card,field,player)

            newcard = deck.drawCard()
            addCardToField(newcard,field,player)

            yakuDict = yakuMng.isYaku(player)
            if yakuMng.isNewYaku(yakuDict, player):
                print("==============================")
                showGame(player1,player2,field) 
                print("==============================")     

                print(f"player{pIdx+1} achieved")
                for yaku in yakuDict:
                    print(f"{yaku.name} ")

                # here requires player selection koikoi or not
                isKoikoi = player.selectKoikoi(yakuDict)
                if not isKoikoi: 
                    onGame = False
                    winyaku = yakuDict
                    winner = player
                    break
            
    point = 0
    if winner is None:
        print("hikiwake")
        return point, winner

    yakustr = ""
    point = 0
    for yaku in winyaku.keys():
        yakustr += yaku.name
        yakustr += " " 
        point += yakuMng.YakuPointDict[yaku] * winyaku[yaku]
    print("==============================")
    print(f"winner {winner.playerName}{'(you)' if not winner.isAuto else '(cpu)'}, {yakustr} {point} points") 
    print("==============================")
    print()  
    return point,winner        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--playnum', type=int, default=1)
    args = parser.parse_args()
    playnum = args.playnum
    total = 0
    playerName = "you"
    playerOrder = random.randint(0,1)
    print("==============================")
    print(f"you are {playerOrder+1} th player")
    print("==============================")
    print()
    total = 0
    cputotal = 0
    for i in range(playnum):
        print(f"play {i}th game")
        seed = random.randint(0,10000)
        player1 = Player(playerName if playerOrder==0 else "player1",isAuto=(playerOrder==1))
        player2 = Player(playerName if playerOrder==1 else "player2",isAuto=(playerOrder==0))
        sc,winner = playGame(player1,player2,seed)
        if sc>=7:
            sc*=2
        if winner.playerName == playerName:
            total += sc
            playerOrder = 0
        elif winner is not None:
            playerOrder = 1 
            cputotal += sc
    
    print("==============================")
    if total>cputotal:
        print(f"you win !!! {total}/{cputotal}")
    elif total<cputotal:
        print(f"you lose ... {cputotal}/{total}")
    else:
        print(f"draw")
    print("==============================")
    
if __name__ == "__main__":
    main()

