#%%

from cards_and_players import Deck,Player,Field


def addCardToField(card,field,player):     
    candidates = field.addCardFromPlayer(card)
    if len(candidates)==3 or len(candidates)==1:
        for cand in candidates:
            player.addCardFromField([card,*candidates])
    elif len(candidates)==2:
        # here requires player selection of card
        player.addCardFromField([card,candidates[0]])
        field.removeCard(candidates[1])

def showGame(player1,player2,field):
    print("player2: ",player2.to_str())
    print()
    print(field.to_str())
    print()
    print("player1: ",player1.to_str())   

# initial card
deck = Deck()
field = Field()
player1 = Player()
player2 = Player()

fieldInitialNumber = 8
playerInitialNumber = 8

while True:
    for i in range(fieldInitialNumber):
        card = deck.drawCard()
        field.addCard(card)
    if field.isIniFour():
        print("field contains 4 cards")
        deck = Deck()
        continue
    break


for i in range(playerInitialNumber):
    card = deck.drawCard()
    player1.addCardToHand(card)
iniYaku = player1.isInitialYaku()
if iniYaku is not None:
    print(f"player1 iniYaku {iniYaku.name}")

for i in range(playerInitialNumber):
    card = deck.drawCard()
    player2.addCardToHand(card)
if iniYaku is not None:
    print(f"player2 iniYaku {iniYaku.name}")

players = [player1,player2]

onGame = True
# start game
while onGame and (not (player1.isEmpty() and player2.isEmpty())):
    for pIdx, player in enumerate(players):
        
        print("==============================")
        showGame(player1,player2,field)  
        print("==============================")

        # here requires player selection of card
        vcands = player.validCards(field)
        if len(vcands)==0:
            disc = player.hand[0]
        else:
            disc = vcands[0]

        card = player.playCard(disc)
        addCardToField(card,field,player)

        newcard = deck.drawCard()
        addCardToField(newcard,field,player)

        yakuDict = player.isYaku()
        if player.isNewYaku(yakuDict):
            print(f"player{pIdx+1} achieved")
            for yaku in yakuDict:
                print(f"{yaku.name} ")
            print()
            # here requires player selection koikoi or not
            isKoikoi = False
            if isKoikoi: 
                player.koikoi(yakuDict)
            else:
                onGame = False
                break
        
print("==============================")
showGame(player1,player2,field)  
print("==============================")
        







# %%
