#%%

from cards_and_players import Deck,Player,Field
import random 


def addCardToField(card,field,player):     
    candidates = field.addCardFromPlayer(card)
    if len(candidates)==3 or len(candidates)==1:
        for cand in candidates:
            player.addCardFromField([card,*candidates])
    elif len(candidates)==2:
        # here requires player selection of card
        print("card month is overlapped in the field. please select")
        pickCard = player.selectCardFromList(candidates)
        player.addCardFromField([card,pickCard])
        candidates.remove(pickCard)
        field.removeCard(candidates[0])

def showGame(player1,player2,field):
    print(f"{player2.playerName}: ",player2.to_str())
    print()
    print("field: ",field.to_str())
    print()
    print(f"{player1.playerName} ",player1.to_str())   

def playGame():
    # initial card
    seed = random.randint(0,10000)
    playerOrder = random.randint(0,1)
    deck = Deck(seed)
    field = Field()

    player1 = Player("player1",isAuto=(playerOrder==1))
    player2 = Player("player2",isAuto=(playerOrder==0))

    print("==============================")
    print(f"you are player {playerOrder+1}")
    print("==============================")
    print()

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


    for i in range(playerInitialNumber):
        card = deck.drawCard()
        player1.addCardToHand(card)
    iniYaku = player1.isInitialYaku()
    if iniYaku is not None:
        print(f"player1 iniYaku {iniYaku.name}")
        return

    for i in range(playerInitialNumber):
        card = deck.drawCard()
        player2.addCardToHand(card)
    if iniYaku is not None:
        print(f"player2 iniYaku {iniYaku.name}")
        return

    players = [player1,player2]

    onGame = True
    winner = ""
    winyaku = {}

    # start game
    while onGame and (not (player1.isEmpty() and player2.isEmpty())):
        for pIdx, player in enumerate(players):
            
            print("==============================")
            if playerOrder==0:
                showGame(player1,player2,field) 
            else:
                showGame(player2,player1,field) 
            print("==============================")

            # here requires player selection of card

            disc = player.selectCardFromList(player.hand)    

            card = player.playCard(disc)
            addCardToField(card,field,player)

            newcard = deck.drawCard()
            addCardToField(newcard,field,player)

            yakuDict = player.isYaku()
            if player.isNewYaku(yakuDict):
                print(f"player{pIdx+1} achieved")
                for yaku in yakuDict:
                    print(f"{yaku.name} ")
                winyaku = yakuDict
                winner = f"player{pIdx+1}"

                # here requires player selection koikoi or not
                isKoikoi = False
                if isKoikoi: 
                    player.koikoi(yakuDict)
                else:
                    onGame = False
                    break
            
    print("==============================")
    if playerOrder==0:
        showGame(player1,player2,field) 
    else:
        showGame(player2,player1,field) 
    print("==============================")


    if winner == "":
        print("hikiwake")
    else:
        yakustr = ""
        for yaku in winyaku.keys():
            yakustr += yaku.name
            yakustr += " " 
        print(f"winner {winner}, {yakustr}")        



if __name__ == "__main__": 
    playGame()




# %%
